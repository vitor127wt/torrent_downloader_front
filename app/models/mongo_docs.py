from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from bson import ObjectId


class RawTorrent(TypedDict, total=False):
    title: str
    magnet: str
    size: int | float
    seeds: int
    peers: int
    leechers: int
    dead: bool
    last_checked: float
    files: dict[str, object]


class RawTorrentPage(TypedDict, total=False):
    _id: ObjectId
    link: str
    title: str
    torrents: list[RawTorrent]
