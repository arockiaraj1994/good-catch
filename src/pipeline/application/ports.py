"""Outbound ports: what the use cases need from the outside world."""

from typing import Protocol

from pipeline.domain.posts import Change, Labels


class RawPost(Protocol):
    @property
    def filename(self) -> str: ...
    @property
    def front(self) -> dict[str, object]: ...
    @property
    def body(self) -> str: ...


class PostStore(Protocol):
    def labels(self) -> Labels: ...
    def changes(self) -> list[Change]: ...
    def read(self, filename: str) -> RawPost: ...
    def all_filenames(self) -> list[str]: ...


class UrlProbe(Protocol):
    def status(self, url: str) -> int | None:
        """HTTP status for the URL, or None if it could not be reached."""
        ...
