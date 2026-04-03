from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import torch
import numpy as np
# ===========================================================================
# DATA STRUCTURES
# ===========================================================================

@dataclass
class TokenSpan:
    """A labeled span of token positions."""
    label: str
    start: int
    end: int  # exclusive

    @property
    def positions(self) -> List[int]:
        return list(range(self.start, self.end))

    def __len__(self):
        return self.end - self.start


@dataclass
class PromptMap:
    """
    Tracks which token positions correspond to which semantic regions.
    This is the central bookkeeping object — everything depends on
    getting these positions right.
    """
    tokens: torch.Tensor              # [1, seq_len]
    token_strs: List[str]             # human-readable
    paragraph_spans: Dict[int, TokenSpan] = field(default_factory=dict)  # 1,2,3 -> span
    retrieval_span: Optional[TokenSpan] = None   # the "let me reread..." tokens
    analysis_span: Optional[TokenSpan] = None    # downstream analytical tokens
    fork_start: Optional[int] = None             # where the fork begins

    @property
    def seq_len(self) -> int:
        return self.tokens.shape[1]

    def print_summary(self):
        print(f"  Total tokens: {self.seq_len}")
        for k, span in self.paragraph_spans.items():
            preview = ''.join(self.token_strs[span.start:span.start+8]) + "..."
            print(f"  Paragraph {k}: positions [{span.start}:{span.end}] "
                  f"({len(span)} tokens) — \"{preview}\"")
        if self.retrieval_span:
            preview = ''.join(self.token_strs[self.retrieval_span.start:self.retrieval_span.start+8])
            print(f"  Retrieval span: [{self.retrieval_span.start}:{self.retrieval_span.end}] "
                  f"({len(self.retrieval_span)} tokens) — \"{preview}...\"")
        if self.analysis_span:
            preview = ''.join(self.token_strs[self.analysis_span.start:self.analysis_span.start+8])
            print(f"  Analysis span: [{self.analysis_span.start}:{self.analysis_span.end}] "
                  f"({len(self.analysis_span)} tokens) — \"{preview}...\"")


@dataclass
class AttentionProfile:
    """
    Stores attention scores from a set of query positions to each paragraph.
    Shape of each array: [n_layers, n_heads]
    """
    label: str
    to_para: Dict[int, np.ndarray]  # paragraph number -> [layers, heads]

    def mean_to(self, para: int) -> float:
        return self.to_para[para].mean()

    def per_layer_to(self, para: int) -> np.ndarray:
        """Mean across heads for each layer. Shape: [n_layers]"""
        return self.to_para[para].mean(axis=1)
