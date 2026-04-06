"""Token counting utility.

Tries to use ``tiktoken`` for accurate token counts (same tokenizer as
OpenAI's API).  Falls back to a simple whitespace split when ``tiktoken``
is not installed.
"""

from typing import Optional

_encoder = None
_tiktoken_available: Optional[bool] = None


def _get_encoder():
    global _encoder, _tiktoken_available
    if _tiktoken_available is None:
        try:
            import tiktoken

            _encoder = tiktoken.get_encoding("cl100k_base")
            _tiktoken_available = True
        except Exception:
            # ImportError if tiktoken is absent; OSError / ConnectionError if
            # the BPE file cannot be downloaded in offline environments.
            _tiktoken_available = False
    return _encoder


def count_tokens(text: str) -> int:
    """Return the number of tokens in *text*."""
    enc = _get_encoder()
    if enc is not None:
        return len(enc.encode(text))
    # Fallback: whitespace split approximation
    return len(text.split())
