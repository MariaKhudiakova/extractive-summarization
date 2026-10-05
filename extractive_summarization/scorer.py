import typing as t
from collections import Counter

from extractive_summarization.utils.text_processing import TextProcessor


class TermFrequencyScorer:
    """A class used to score sentences by normalized term frequency."""

    def __init__(self, text_processor: t.Optional[TextProcessor] = None) -> None:
        """
        Initialize scorer.

        :param text_processor: text processor instance
        """
        self.text_processor = text_processor or TextProcessor()

    def build_word_scores(self, sentences: t.List[str]) -> t.Dict[str, float]:
        """
        Compute normalized word frequency across all sentences.

        :param sentences: list of sentences
        :return: mapping from word to normalized frequency in [0, 1]
        """
        counter: Counter = Counter()
        for sentence in sentences:
            counter.update(self.text_processor.content_tokens(sentence))

        if not counter:
            return {}

        max_count = max(counter.values())
        return {word: count / max_count for word, count in counter.items()}

    def score_sentences(
        self,
        sentences: t.List[str],
        word_scores: t.Dict[str, float],
    ) -> t.List[float]:
        """
        Score each sentence as the average score of its content words.

        :param sentences: list of sentences
        :param word_scores: mapping from word to score
        :return: list of sentence scores in the same order
        """
        scores: t.List[float] = []
        for sentence in sentences:
            tokens = self.text_processor.content_tokens(sentence)
            if not tokens:
                scores.append(0.0)
                continue
            total = sum(word_scores.get(tok, 0.0) for tok in tokens)
            scores.append(total)
        return scores
