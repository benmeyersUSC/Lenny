
import sys
import torch
import numpy as np
import transformer_lens as tl
from transformer_lens import HookedTransformer
from typing import Dict, List, Tuple, Optional
import altPassages as A_P
from datastructs import AttentionProfile, TokenSpan, PromptMap
from viz import plot_layer_curves, plot_layer_heatmaps, plot_narrowed_bars, plot_single_layer_heads, plot_single_layer_heads_difference, plot_summary_bars, print_summary

# ===========================================================================
# CONFIG
# ===========================================================================

MODEL_NAME = "EleutherAI/pythia-1.4b"  

USER_PROMPT = f"""Here is a passage with three paragraphs on very different topics:

{A_P.PASSAGE_SET_1["passage"]}

Please analyze each paragraph in detail, one at a time. For each paragraph, discuss the key claims, any interesting implications, and connections you notice."""


# ===========================================================================
# MODEL
# ===========================================================================

def load_model(model_name: str = MODEL_NAME) -> HookedTransformer:
    print(f"Loading {model_name}...")
    model = HookedTransformer.from_pretrained(
        model_name,
        device="cuda" if torch.cuda.is_available() else "cpu",
    )
    print(f"  Device: {model.cfg.device} | Layers: {model.cfg.n_layers} | "
          f"Heads: {model.cfg.n_heads} | d_model: {model.cfg.d_model}")
    return model


# ===========================================================================
# TOKENIZATION AND POSITION TRACKING
# ===========================================================================

def find_token_subsequence(
    haystack: List[str],
    needle_text: str,
    model: HookedTransformer,
    search_start: int = 0,
) -> Optional[Tuple[int, int]]:
    """
    Find where `needle_text` appears in the token list `haystack`.
    Returns (start, end) positions or None.

    Strategy: tokenize the needle, then search for a long interior
    subsequence to avoid boundary tokenization mismatches.
    """
    needle_tokens = model.to_str_tokens(needle_text)

    # Use interior tokens to avoid BPE boundary issues
    margin = min(3, len(needle_tokens) // 4)
    if len(needle_tokens) < 6:
        interior = needle_tokens[1:]
    else:
        interior = needle_tokens[margin:-margin]

    interior_len = len(interior)
    if interior_len == 0:
        return None

    for i in range(search_start, len(haystack) - interior_len):
        if haystack[i:i + interior_len] == interior:
            # Found interior match — expand to approximate full span
            start = max(0, i - margin)
            end = i + interior_len + margin
            return (start, min(end, len(haystack)))

    return None


def build_prompt_map(
    model: HookedTransformer,
    full_prompt: str,
    passage: str = A_P.PASSAGE_SET_1["passage"],
) -> PromptMap:
    """
    Tokenize the full prompt and locate each paragraph's token positions.
    """
    tokens = model.to_tokens(full_prompt)
    token_strs = model.to_str_tokens(full_prompt)

    para_texts = passage.strip().split("\n\n")
    assert len(para_texts) == 3, f"Expected 3 paragraphs, got {len(para_texts)}"

    pmap = PromptMap(tokens=tokens, token_strs=token_strs)

    for i, para in enumerate(para_texts, 1):
        result = find_token_subsequence(token_strs, para, model)
        if result:
            pmap.paragraph_spans[i] = TokenSpan(f"para_{i}", result[0], result[1])
        else:
            print(f"  WARNING: Could not locate paragraph {i}")

    return pmap


# ===========================================================================
# ATTENTION EXTRACTION
# ===========================================================================

def extract_attention_profile(
    model: HookedTransformer,
    full_prompt: str,
    query_positions: List[int],
    paragraph_spans: Dict[int, TokenSpan],
    label: str,
) -> AttentionProfile:
    """
    Run a forward pass, cache attention, and compute how much the
    query_positions attend to each paragraph.

    This is the core measurement function.
    """
    _, cache = model.run_with_cache(
        full_prompt,
        names_filter=lambda name: "pattern" in name,
    )

    n_layers = model.cfg.n_layers
    n_heads = model.cfg.n_heads

    to_para = {}
    for para_num, span in paragraph_spans.items():
        attn_matrix = np.zeros((n_layers, n_heads))
        para_pos = span.positions

        for layer in range(n_layers):
            pattern = cache["pattern", layer][0]  # [heads, seq, seq]
            for head in range(n_heads):
                # Mean over query positions of: total attention to paragraph
                attn = pattern[head][query_positions][:, para_pos].sum(dim=-1).mean()
                attn_matrix[layer, head] = attn.item()

        to_para[para_num] = attn_matrix

    # Free cache memory
    del cache
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return AttentionProfile(label=label, to_para=to_para)


# ===========================================================================
# EXPERIMENT 1: ABLATION
# ===========================================================================

def run_ablation_experiment(model: HookedTransformer) -> Dict:
    """
    1. Generate the model's natural analysis of the passage.
    2. Manually inspect output and identify retrieval language.
    3. Create ablated version with retrieval tokens replaced by neutral filler.
    4. Compare downstream attention in both versions.

    NOTE: Step 2 requires manual inspection. This function generates the
    natural output and provides a framework for the comparison. You will
    need to fill in the retrieval span boundaries after inspecting the output.
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 1: ABLATION")
    print("=" * 70)

    # --- Step 1: Generate natural output ---
    print("\nGenerating natural model output...")
    input_tokens = model.to_tokens(USER_PROMPT)
    natural_output = model.generate(
        input_tokens,
        max_new_tokens=500,
        temperature=0.7,
        top_p=0.9,
    )
    natural_text = model.to_string(natural_output[0])
    natural_token_strs = model.to_str_tokens(natural_output[0])

    print("\n--- NATURAL OUTPUT (with token indices) ---")
    # Print with token indices for easy span identification
    generated_start = input_tokens.shape[1]
    for i, tok in enumerate(natural_token_strs[generated_start:], start=generated_start):
        print(f"[{i:4d}] {repr(tok)}", end="  ")
        if (i - generated_start) % 8 == 7:
            print()
    print("\n--- END OUTPUT ---\n")

    print("MANUAL STEP REQUIRED:")
    print("  1. Inspect the output above for retrieval-like language")
    print("     (e.g., 'looking back at', 'rereading', 'returning to')")
    print("  2. Note the token indices of the retrieval span")
    print("  3. Note the token indices of the downstream analysis span")
    print("  4. Call run_ablation_comparison() with those indices")
    print()

    return {
        'natural_text': natural_text,
        'natural_tokens': natural_output,
        'generated_start': generated_start,
        'token_strs': natural_token_strs,
    }


def run_ablation_comparison(
    model: HookedTransformer,
    natural_text: str,
    retrieval_start: int,
    retrieval_end: int,
    analysis_start: int,
    analysis_end: int,
    filler: str = "\n\n",
) -> Tuple[AttentionProfile, AttentionProfile]:
    """
    Once you've identified the retrieval span, run the comparison.

    Args:
        natural_text:    The full natural generation (prompt + output)
        retrieval_start: Token index where retrieval language begins
        retrieval_end:   Token index where retrieval language ends (exclusive)
        analysis_start:  Token index where downstream analysis begins
        analysis_end:    Token index where downstream analysis ends
        filler:          What to replace retrieval tokens with (neutral text)
    """
    natural_token_strs = model.to_str_tokens(natural_text)

    # Build ablated version: replace retrieval span with filler
    retrieval_text = ''.join(natural_token_strs[retrieval_start:retrieval_end])
    ablated_text = natural_text.replace(retrieval_text, filler, 1)

    print(f"Retrieval span removed: \"{retrieval_text[:80]}...\"")
    print(f"Replaced with: \"{filler}\"")

    # Build prompt maps for both versions
    natural_map = build_prompt_map(model, natural_text)
    ablated_map = build_prompt_map(model, ablated_text)

    # The analysis span positions shift in the ablated version
    # Recompute based on the text content of the analysis span
    analysis_text = ''.join(natural_token_strs[analysis_start:analysis_end])
    ablated_token_strs = model.to_str_tokens(ablated_text)
    ablated_analysis = find_token_subsequence(ablated_token_strs, analysis_text, model)

    if ablated_analysis is None:
        print("ERROR: Could not locate analysis span in ablated text")
        return None, None

    natural_query_pos = list(range(analysis_start, analysis_end))
    ablated_query_pos = list(range(ablated_analysis[0], ablated_analysis[1]))

    print(f"\nNatural: analysis at [{analysis_start}:{analysis_end}], "
          f"{len(natural_query_pos)} tokens")
    print(f"Ablated: analysis at [{ablated_analysis[0]}:{ablated_analysis[1]}], "
          f"{len(ablated_query_pos)} tokens")

    # Extract attention profiles
    print("\nRunning natural version...")
    natural_profile = extract_attention_profile(
        model, natural_text, natural_query_pos,
        natural_map.paragraph_spans, "natural"
    )

    print("Running ablated version...")
    ablated_profile = extract_attention_profile(
        model, ablated_text, ablated_query_pos,
        ablated_map.paragraph_spans, "ablated"
    )

    return natural_profile, ablated_profile


# ===========================================================================
# EXPERIMENT 2: INJECTION
# ===========================================================================

def run_injection_with_passage_set(
    model: HookedTransformer,
    passage_set: Dict,
    set_name: str,
) -> Dict[str, AttentionProfile]:
    """
    Run the injection experiment with an alternate passage set.

    Usage:
        profiles = run_injection_with_passage_set(model, PASSAGE_SET_2, "set2")
    """
    passage = passage_set["passage"]
    shared_analysis = passage_set["shared_analysis"]
    forks = passage_set["forks"]
    shared_tail = passage_set["shared_tail"]

    user_prompt = f"""Here is a passage with three paragraphs on very different topics:

{passage}

Please analyze each paragraph in detail, one at a time. For each paragraph, discuss the key claims, any interesting implications, and connections you notice."""

    print(f"\n{'=' * 70}")
    print(f"INJECTION — {set_name}")
    print(f"{'=' * 70}")

    profiles = {}

    for fork_name, fork_text in forks.items():
        full_prompt = user_prompt + shared_analysis + fork_text

        print(f"\n--- Fork {fork_name} ---")
        pmap = build_prompt_map(model, full_prompt, passage)
        pmap.print_summary()

        tail_result = find_token_subsequence(
            pmap.token_strs, shared_tail, model,
            search_start=len(model.to_str_tokens(user_prompt + shared_analysis)) - 5
        )

        if tail_result is None:
            print(f"  WARNING: Could not locate analysis tail in fork {fork_name}")
            continue

        query_positions = list(range(tail_result[0], tail_result[1]))
        print(f"  Query positions (analysis tail): [{tail_result[0]}:{tail_result[1]}]")

        profile = extract_attention_profile(
            model, full_prompt, query_positions,
            pmap.paragraph_spans, fork_name,
        )
        profiles[fork_name] = profile

    return profiles



# ===========================================================================
# MAIN
# ===========================================================================

def RunInjectionSets(model, passage_sets, layers, paragraphs):
    for i, pset in enumerate(passage_sets):
        profiles = run_injection_with_passage_set(model, pset, f"set{i+1}")
        print_summary(profiles)
        for l in layers:
            for tp in paragraphs:
                plot_single_layer_heads(profiles, tp, l, f"Set {i+1}: -> P{tp}", f"set{i+1}/heads_p{tp}_L{l}.png")
                plot_single_layer_heads_difference(profiles, tp, l, "A_neutral",f"Set {i+1}: -> P{tp}", f"set{i+1}/heads_p{tp}_L{l}_diff.png")

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "both"
    mode = ""
    model = load_model()

    if mode in ("ablation", "both"):
        pass

        # ---------------------------------------------------------------
        # AFTER MANUAL INSPECTION: uncomment and fill in token indices
        # ---------------------------------------------------------------
        # natural_prof, ablated_prof = run_ablation_comparison(
        #     model,
        #     natural_text=ablation_output['natural_text'],
        #     retrieval_start=XXX,    # <-- token index where retrieval begins
        #     retrieval_end=XXX,      # <-- token index where retrieval ends
        #     analysis_start=XXX,     # <-- token index where analysis begins
        #     analysis_end=XXX,       # <-- token index where analysis ends
        # )
        # ablation_profiles = {"natural": natural_prof, "ablated": ablated_prof}
        # print_summary(ablation_profiles)
        # plot_summary_bars(ablation_profiles, "Ablation Study", "ablation_bars.png")
        # plot_layer_heatmaps(ablation_profiles, 3, "Ablation", "ablation_heatmaps_p3.png")
        # plot_layer_curves(ablation_profiles, 3, "Ablation: → P3 by Layer", "ablation_layers.png")

    if mode in ("injection", "both"):
        pass


    RunInjectionSets(model, [A_P.PASSAGE_SET_1,A_P.PASSAGE_SET_2,A_P.PASSAGE_SET_3,A_P.PASSAGE_SET_4,A_P.PASSAGE_SET_5], [10], [1, 3])

    print("\nDone.")


if __name__ == "__main__":
    main()