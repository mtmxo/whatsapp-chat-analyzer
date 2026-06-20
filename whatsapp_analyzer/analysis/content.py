"""Content analysis: word frequencies and emoji usage over text messages."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field

from ..models import Chat, MessageType
from .base import Analyzer

# Word tokens: runs of letters only (Unicode-aware), so digits, underscores and
# punctuation are dropped. \w would also match digits and "_", which we don't want.
_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)

# Emoji are matched by their main Unicode blocks rather than an exhaustive table:
# pictographs/supplemental/extended-A, misc symbols + dingbats, and regional
# indicators (flags). It is intentionally approximate but dependency-free.
_EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F1E6-\U0001F1FF]"
)


@dataclass(frozen=True)
class ContentReport:
    word_counts: Counter[str] = field(default_factory=Counter)
    emoji_counts: Counter[str] = field(default_factory=Counter)

    def top_words(self, n: int | None = None) -> list[tuple[str, int]]:
        return self.word_counts.most_common(n)

    def top_emojis(self, n: int | None = None) -> list[tuple[str, int]]:
        return self.emoji_counts.most_common(n)


class ContentAnalyzer(Analyzer):
    def __init__(self, stopwords: set[str] | None = None):
        # Stopwords are matched lowercased, consistently with the tokenizer.
        self.stopwords = {w.lower() for w in stopwords} if stopwords else set()

    def analyze(self, chat: Chat) -> ContentReport:
        word_counts: Counter[str] = Counter()
        emoji_counts: Counter[str] = Counter()
        for msg in chat:
            if msg.type != MessageType.TEXT:
                continue
            for word in _WORD.findall(msg.text.lower()):
                if word not in self.stopwords:
                    word_counts[word] += 1
            for emoji in _EMOJI.findall(msg.text):
                emoji_counts[emoji] += 1
        return ContentReport(word_counts=word_counts, emoji_counts=emoji_counts)
