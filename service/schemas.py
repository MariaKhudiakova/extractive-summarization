import typing as t

from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    """Тело запроса к /summarize."""

    text: str = Field(..., min_length=1, description="Текст для суммаризации.")
    num_sentences: t.Optional[int] = Field(
        default=None,
        ge=1,
        description="Точное число предложений в саммари. Приоритет над ratio.",
    )
    ratio: float = Field(
        default=0.3,
        gt=0.0,
        le=1.0,
        description="Доля предложений, если num_sentences не задан.",
    )


class SummarizeResponse(BaseModel):
    """Тело ответа /summarize."""

    summary: str = Field(..., description="Извлечённое саммари.")
    num_sentences: int = Field(..., description="Число предложений в саммари.")
