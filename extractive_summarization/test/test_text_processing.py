from extractive_summarization.utils.text_processing import TextProcessor


class TestTextProcessor:
    def setup_method(self) -> None:
        self.processor = TextProcessor()

    def test_split_sentences(self) -> None:
        text = "Привет, мир. Это тест! Работает ли это?"
        assert self.processor.split_sentences(text) == [
            "Привет, мир.",
            "Это тест!",
            "Работает ли это?",
        ]

    def test_split_ellipsis(self) -> None:
        text = "Он задумался… Потом ответил."
        assert self.processor.split_sentences(text) == [
            "Он задумался…",
            "Потом ответил.",
        ]

    def test_split_empty(self) -> None:
        assert self.processor.split_sentences("") == []

    def test_tokenize_lowercases_cyrillic(self) -> None:
        assert self.processor.tokenize("Привет МИР") == ["привет", "мир"]

    def test_tokenize_mixed_alphabet(self) -> None:
        assert self.processor.tokenize("Используем TCP/IP протокол") == [
            "используем",
            "tcp",
            "ip",
            "протокол",
        ]

    def test_content_tokens_drops_stopwords(self) -> None:
        tokens = self.processor.content_tokens("Это очень быстрый интернет")
        assert "это" not in tokens
        assert "очень" not in tokens
        assert "быстрый" in tokens
        assert "интернет" in tokens
