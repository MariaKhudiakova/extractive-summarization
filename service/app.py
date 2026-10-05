from fastapi import Depends, FastAPI
from typing_extensions import Annotated

from extractive_summarization import ExtractiveSummarizer, SummarizerSettings
from service.dependencies import get_summarizer
from service.schemas import SummarizeRequest, SummarizeResponse

app = FastAPI(
    title="Extractive Summarization Service",
    version="0.1.0",
    description="Simple extractive summarization over TF-based sentence scoring.",
)

SummarizerDep = Annotated[ExtractiveSummarizer, Depends(get_summarizer)]


@app.get("/health")
def health() -> dict:
    """Health-check endpoint."""
    return {"status": "ok"}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(
    payload: SummarizeRequest,
    summarizer: SummarizerDep,
) -> SummarizeResponse:
    """
    Summarize the given text extractively.

    :param payload: request body
    :param summarizer: summarizer dependency
    :return: summary response
    """
    settings = SummarizerSettings(
        num_sentences=payload.num_sentences,
        ratio=payload.ratio,
    )
    sentences = summarizer.select_sentences(payload.text, settings)
    return SummarizeResponse(
        summary=" ".join(sentences),
        num_sentences=len(sentences),
    )
