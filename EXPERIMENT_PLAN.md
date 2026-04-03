# Self-Directed Attention Retrieval in Transformers

## The Core Observation

When an LLM generates tokens like "let me reread the part about X," it is not performing any special operation — there is no cursor, no rereading mechanism. And yet the statement is *functionally true*: emitting tokens semantically related to earlier context causes the attention mechanism to upweight those earlier positions, effectively retrieving that information into the model's active representation. The model has learned to use its own output as a query mechanism against its own context.

This project provides mechanistic evidence for this phenomenon through two complementary experiments.

---

## Experiment 1: Ablation Study (Primary)

### Design

1. Give a model a passage with 3 semantically distinct paragraphs and instruct it to analyze each one in sequence.
2. Let the model generate its full response naturally, including any self-directed retrieval language it spontaneously produces (e.g., "Looking back at the third paragraph," "Rereading the section on fermentation," etc.).
3. Identify spans of self-directed retrieval tokens in the natural generation.
4. Create an ablated version: remove (or replace with neutral filler) the retrieval token spans, preserving everything else — especially the downstream analytical tokens.
5. Run both versions through the model with activation caching.
6. **Compare attention patterns** of the *downstream analytical tokens* (the sentences doing actual analysis, which are identical in both conditions) to the relevant paragraph positions, with vs. without the upstream retrieval tokens.

### What We Measure

- **Attention shift**: Do the downstream analytical tokens attend more to the correct paragraph when retrieval tokens precede them?
- **Layer localization**: In which layers does this effect appear? (Prediction: mid-to-late layers where semantic matching occurs, not early positional/syntactic layers.)
- **Head specificity**: Is the effect concentrated in specific attention heads, possibly induction heads or known retrieval heads?
- **Behavioral consequence**: If we let the model *generate* from the ablated context, does output quality degrade? More hallucinations, factual errors about the passage, vague rather than specific claims?

### Why This Design Is Clean

- The query tokens (downstream analysis) are identical in both conditions.
- The only difference is whether retrieval tokens precede them.
- This is a proper causal ablation: we remove a specific component and measure the downstream effect.
- No injection of artificial text — we study the phenomenon as it naturally occurs.

---

## Experiment 2: Injection Study (Complementary)

### Design

1. Same passage setup: 3 paragraphs, model analyzes sequentially.
2. We write a shared prefix (analysis of paragraphs 1 and 2) and then fork into three conditions right before paragraph 3 analysis:
   - **Fork A (Neutral):** Transition directly into paragraph 3 analysis with no retrieval language.
   - **Fork B (Targeted Retrieval):** Insert "Let me reread the third paragraph about fermentation..." then continue to analysis.
   - **Fork C (Misdirected Retrieval):** Insert "Let me reread the first paragraph about the octopus..." then continue to paragraph 3 analysis.

3. Run all three forks with attention caching.
4. Compare attention from the fork region to each paragraph across conditions.

### Predictions

- **Fork B vs A:** Elevated attention to paragraph 3 in Fork B. Better factual fidelity in generated output.
- **Fork C vs A:** Elevated attention to paragraph 1 (the wrong paragraph) in Fork C. Possibly degraded analysis of paragraph 3 — the model may even bleed in octopus-related content.
- **Fork C** is the strongest evidence: misdirected retrieval tokens actively redirect attention to the wrong target.

---

## Passage Design Principles

The passage must have 3 paragraphs that are:

- **Semantically orthogonal**: Completely different topics with minimal vocabulary overlap, so attention to paragraph 1 vs 2 vs 3 is cleanly distinguishable in the attention maps.
- **Rich enough to analyze**: Each paragraph should contain 2-3 specific claims that the model can reference, so we can check factual fidelity in generated output.
- **Roughly equal length**: So baseline attention differences aren't driven by token count.

Current passage uses: (1) octopus neuroscience, (2) Renaissance Florentine economics, (3) fermentation biochemistry. These share almost zero vocabulary.

---

## Technical Approach

### Library: TransformerLens

- `HookedTransformer.from_pretrained()` loads a model with hooks on every internal activation.
- `model.run_with_cache(tokens, names_filter=...)` runs a forward pass and intercepts specified activations.
- `cache["pattern", layer_idx]` returns attention weights: shape `[batch, n_heads, seq_len, seq_len]`.
- `cache["pattern", L][0, H, i, j]` = how much token at position `i` attends to token at position `j`, in layer `L`, head `H`.

### Token Position Tracking

We need to know exactly which token indices correspond to:
- Paragraph 1, 2, 3 in the original passage
- The retrieval token span (for ablation)
- The downstream analytical tokens (the query side of our measurement)

This requires careful tokenization and subsequence matching. Boundary effects in tokenization (whitespace, BPE merges) mean we need to verify positions manually.

### Models

For proof of concept:
- `EleutherAI/pythia-1.4b` or `pythia-2.8b` (well-supported in TransformerLens, studied in prior interp work)
- `gpt2-medium` or `gpt2-large` (extremely well-studied)

For instruction-tuned behavior (more natural CoT generation):
- Check TransformerLens docs for currently supported chat/instruct models
- Alternatively, use a base model and prompt-engineer the analysis format

The phenomenon should be architecture-independent — it's a consequence of how dot-product attention works, not a learned quirk of any specific model.

### Analysis Pipeline

1. **Tokenize** all versions (natural, ablated, fork variants)
2. **Track positions** of each paragraph, retrieval spans, and analysis spans
3. **Forward pass with cache** on each version
4. **Extract attention matrices** at every layer/head
5. **Compute per-paragraph attention scores** from analysis tokens to paragraph tokens
6. **Aggregate**: mean across heads (and optionally identify standout heads), plot per-layer
7. **Compare** across conditions with clear summary statistics
8. **(Optional) Generate continuations** from each condition and score factual accuracy

---

## What Success Looks Like

**Strong positive result:**
- Ablation study shows statistically meaningful drop in attention to the target paragraph when retrieval tokens are removed.
- Injection study shows Fork B > Fork A on paragraph 3 attention, and Fork C shows elevated paragraph 1 attention (misdirection).
- Effect is concentrated in mid-to-late layers.
- Generated output from ablated/neutral conditions contains more factual errors about the passage.

**The narrative:**
Transformers trained on language have learned to exploit a feature of their own architecture: by emitting tokens semantically related to earlier context, they trigger the attention mechanism to retrieve that context into active computation. This is not an explicit retrieval system — it is an emergent behavior where the model's output serves as a self-directed query. We provide causal evidence through both ablation (removing natural retrieval language degrades downstream attention and output quality) and injection (adding retrieval language enhances attention; misdirecting it redirects attention to the wrong target).

---

## Iteration Plan

1. **Get the scaffold running** on Pythia-1.4b with a simple prompt. Verify that tokenization tracking works and attention caches are extractable.
2. **Natural generation**: Let the model generate its full analysis. Inspect whether it spontaneously produces retrieval-like language. (If it doesn't, we may need a different model or prompt format.)
3. **Ablation pass**: Identify retrieval spans, ablate, compare attention maps.
4. **Injection pass**: Run the three forks, compare.
5. **Visualization**: Summary bar charts, per-layer heatmaps, per-head analysis.
6. **Output quality**: Generate continuations and manually score factual accuracy.
7. **Robustness**: Try different passages, different models, different retrieval phrasings.
