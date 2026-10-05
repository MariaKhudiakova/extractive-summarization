import typing as t

from extractive_summarization.scorer import TermFrequencyScorer
from extractive_summarization.settings import SummarizerSettings
from extractive_summarization.utils.text_processing import TextProcessor


class ExtractiveSummarizer:
    """A class used to perform simple extractive summarization."""

    def __init__(
        self,
        text_processor: t.Optional[TextProcessor] = None,
        scorer: t.Optional[TermFrequencyScorer] = None,
    ) -> None:
        """
        Initialize extractive summarizer.

        :param text_processor: text processor instance
        :param scorer: sentence scorer instance
        """
        self.text_processor = text_processor or TextProcessor()
        self.scorer = scorer or TermFrequencyScorer(self.text_processor)

    def summarize(
        self,
        text: str,
        settings: t.Optional[SummarizerSettings] = None,
    ) -> str:
        """
        Produce an extractive summary of the given text.

        :param text: input text
        :param settings: summarization settings
        :return: summary as a string of sentences in original order
        """
        return " ".join(self.select_sentences(text, settings))

    def select_sentences(
        self,
        text: str,
        settings: t.Optional[SummarizerSettings] = None,
    ) -> t.List[str]:
        """
        Select the most important sentences preserving original order.

        :param text: input text
        :param settings: summarization settings
        :return: list of selected sentences
        """
        if settings is None:
            settings = SummarizerSettings()

        sentences = self.text_processor.split_sentences(text)[: settings.max_sentences]

        candidates = [
            s
            for s in sentences
            if len(self.text_processor.tokenize(s)) >= settings.min_sentence_length
        ]
        if not candidates:
            return []

        num_to_keep = self._resolve_num_sentences(len(candidates), settings)
        word_scores = self.scorer.build_word_scores(candidates)
        sentence_scores = self.scorer.score_sentences(candidates, word_scores)

        ranked_indices = sorted(
            range(len(candidates)),
            key=lambda i: sentence_scores[i],
            reverse=True,
        )
        selected_indices = sorted(ranked_indices[:num_to_keep])

        return [candidates[i] for i in selected_indices]

    def _resolve_num_sentences(
        self,
        total: int,
        settings: SummarizerSettings,
    ) -> int:
        """
        Determine how many sentences to keep.

        :param total: total number of candidate sentences
        :param settings: summarization settings
        :return: number of sentences to keep (>= 1, <= total)
        """
        if settings.num_sentences is not None:
            return max(1, min(settings.num_sentences, total))
        return max(1, min(int(round(total * settings.ratio)), total))
