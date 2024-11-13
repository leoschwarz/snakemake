import bisect
from typing import Sequence, TypeVar, Generator

V = TypeVar("V")


class PrefixLookup:
    def __init__(self, entries: Sequence[tuple[str, V]]) -> None:
        self._entries = sorted(entries, key=lambda x: x[0])

    def match(self, key: str) -> set[V]:
        return set(self.match_iter(key))

    def match_iter(self, key: str) -> Generator[V, None, None]:
        """Returns all entries which are prefixes of the given key.

        E.g. if "abc" is the key then "abc", "ab", "a", and "" are considered valid prefixes.
        """
        stop_idx = bisect.bisect_right(self._entries, key, key=lambda x: x[0])
        for index in range(stop_idx - 1, -1, -1):
            k, entry = self._entries[index]
            if key.startswith(k):
                yield entry
            else:
                # TODO naive impl
                pass
