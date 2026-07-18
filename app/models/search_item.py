from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TorrentOption:
    index: int
    title: str
    magnet: str
    size: int | float
    seeds: int
    peers: int
    leechers: int
    dead: bool


@dataclass(frozen=True, slots=True)
class SearchItem:
    id: str
    title: str
    link: str
    torrents: tuple[TorrentOption, ...]


@dataclass(frozen=True, slots=True)
class SearchPage:
    items: tuple[SearchItem, ...]
    page: int
    has_more: bool
