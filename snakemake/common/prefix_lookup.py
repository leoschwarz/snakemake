import bisect
import math
from typing import Sequence, TypeVar, Generator

V = TypeVar("V")


class PrefixLookup:
    def __init__(self, entries: Sequence[tuple[str, V]]) -> None:
        self._entries = sorted(entries, key=lambda x: x[0])

    def match(self, key: str) -> set[V]:
        return set(self.match_iter(key))

    def match_iter(self, key: str) -> Generator[V, None, None]:
        hits = set()
        stop_idx = bisect.bisect_right(self._entries, key, key=lambda x: x[0])
        previous_len = math.inf
        for index in range(stop_idx - 1, -1, -1):
            k, entry = self._entries[index]
            if key.startswith(k):
                hits.add(entry)
            elif len(k) > previous_len:
                break
            previous_len = len(k)
        return hits
