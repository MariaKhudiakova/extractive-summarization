from extractive_summarization import ExtractiveSummarizer, SummarizerSettings


class TestExtractiveSummarizer:
    def setup_method(self) -> None:
        self.summarizer = ExtractiveSummarizer()

    def test_summarize_returns_string(self) -> None:
        text = (
            "Python — это язык программирования. "
            "Python используется в машинном обучении. "
            "Многие разработчики любят Python. "
            "Бананы — жёлтые фрукты."
        )
        result = self.summarizer.summarize(text, SummarizerSettings(num_sentences=2))
        assert isinstance(result, str)
        assert result

    def test_num_sentences_is_respected(self) -> None:
        text = "Первое предложение здесь. Второе предложение здесь. Третье предложение здесь."
        result = self.summarizer.select_sentences(
            text, SummarizerSettings(num_sentences=2)
        )
        assert len(result) == 2

    def test_ratio_used_when_num_sentences_is_none(self) -> None:
        text = "Раз два три. Четыре пять шесть. Семь восемь девять. Десять раз ещё."
        result = self.summarizer.select_sentences(text, SummarizerSettings(ratio=0.5))
        assert len(result) == 2

    def test_empty_text(self) -> None:
        assert self.summarizer.summarize("") == ""

    def test_short_sentences_are_dropped(self) -> None:
        text = "Да. Это намного более длинное предложение с содержанием. Нет."
        result = self.summarizer.select_sentences(
            text,
            SummarizerSettings(num_sentences=5, min_sentence_length=3),
        )
        assert "Да." not in result
        assert "Нет." not in result

    def test_original_order_preserved(self) -> None:
        text = (
            "Кошки — прекрасные питомцы. "
            "Собаки — прекрасные питомцы. "
            "Кошки снова прекрасные питомцы."
        )
        result = self.summarizer.select_sentences(
            text, SummarizerSettings(num_sentences=2)
        )
        indices = [text.index(s) for s in result]
        assert indices == sorted(indices)
