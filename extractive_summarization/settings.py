import typing as t

from pydantic import BaseModel, Field


class SummarizerSettings(BaseModel):
    """Настройки экстрактивной суммаризации."""

    num_sentences: t.Optional[int] = Field(
        default=None,
        ge=1,
        description="Точное число предложений в саммари. Имеет приоритет над ratio.",
    )
    ratio: float = Field(
        default=0.3,
        gt=0.0,
        le=1.0,
        description="Доля предложений, оставляемых в саммари (если num_sentences не задан).",
    )
    min_sentence_length: int = Field(
        default=3,
        ge=1,
        description="Минимальная длина предложения в словах, чтобы попасть в кандидаты.",
    )
    max_sentences: int = Field(
        default=100,
        ge=1,
        description="Максимум предложений, обрабатываемых за один вызов.",
    )
