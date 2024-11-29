"""Implementation of custom sets."""

from typing import Iterable, Optional


class StringSet(set):
    """Set that only allows adding str objects."""

    def __init__(
        self,
        iterable: Optional[Iterable[str]] = None,
        *,
        force_upper_case: bool = False,
    ) -> None:
        """Build an unordered collection of unique elements of type str.

        StringSet() -> new empty StringSet object
        StringSet(iterable) -> new StringSet object
        """
        self.upper_case = force_upper_case
        if iterable is not None:
            for item in iterable:
                self.add(item)
        else:
            super().__init__()

    def add(self, item: str) -> None:
        """Add an element to a set. Checks the element type to be a str."""
        if not isinstance(item, str):
            raise ValueError(f"Only strings are allowed. Invalid item: {item}")

        if self.upper_case:
            item = item.upper()

        return super().add(item)

    def __contains__(self, o: object) -> bool:
        """Overwrite the `in` operator.

        x.__contains__(y) <==> y in x.
        """
        if not isinstance(o, str):
            o = str(o)

        if self.upper_case:
            o = o.upper()

        return super().__contains__(o)
