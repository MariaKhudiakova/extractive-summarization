import functools

from extractive_summarization.summarizer import ExtractiveSummarizer


@functools.lru_cache(maxsize=1)
def get_summarizer() -> ExtractiveSummarizer:
    """
    Provide a shared summarizer instance.

    :return: extractive summarizer
    """
    return ExtractiveSummarizer()
