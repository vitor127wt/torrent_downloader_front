from typing import TYPE_CHECKING

from bson import ObjectId
from bson.errors import InvalidId

from app.models.search_filters import SearchFilters  # noqa

if TYPE_CHECKING:
    from pymongo.collection import Collection

    from app.models.mongo_docs import RawTorrentPage


_REGEX_SPECIAL_CHARACTERS = frozenset(r"\.^$|?*+()[]{}")


def escape_mongo_regex(value: str) -> str:
    return "".join(
        f"\\{character}"
        if character in _REGEX_SPECIAL_CHARACTERS
        else character
        for character in value
    )


class TorrentRepository:
    def __init__(self, collection: Collection[RawTorrentPage]) -> None:
        self._collection = collection

    def search_by_title(
        self,
        filters: SearchFilters,
        page: int,
        page_size: int,
    ) -> tuple[tuple[RawTorrentPage, ...], bool]:

        if len(filters.query) < 2:
            return (), False

        safe_page = max(page, 1)
        safe_page_size = min(max(page_size, 1), 50)

        offset = (safe_page - 1) * safe_page_size

        pattern = escape_mongo_regex(filters.query)

        title_filter: dict[str, object] = {
            "$or": [
                {
                    "title": {
                        "$regex": pattern,
                        "$options": "i",
                    }
                },
                {
                    "torrents.title": {
                        "$regex": pattern,
                        "$options": "i",
                    }
                },
            ]
        }

        torrent_conditions: dict[str, object] = {}

        if filters.min_seeders > 0:
            torrent_conditions["seeds"] = {"$gte": filters.min_seeders}

        if not filters.show_dead:
            torrent_conditions["dead"] = {"$ne": True}

        if torrent_conditions:
            query_filter: dict[str, object] = {
                "$and": [
                    title_filter,
                    {
                        "torrents": {
                            "$elemMatch": torrent_conditions,
                        }
                    },
                ]
            }
        else:
            query_filter = title_filter

        cursor = (
            self._collection.find(
                query_filter,
                {"torrents.files": 0},
            )
            .sort([("title", 1), ("_id", 1)])
            .skip(offset)
            .limit(safe_page_size + 1)
        )

        documents = tuple(cursor)

        has_more = len(documents) > safe_page_size

        return documents[:safe_page_size], has_more

    def get_torrent_files(
        self,
        item_id: str,
        torrent_index: int,
    ) -> dict[str, object] | None:
        if torrent_index < 0:
            return None

        try:
            object_id = ObjectId(item_id)
        except InvalidId:
            return None

        document = self._collection.find_one(
            {"_id": object_id},
            {
                "_id": 0,
                "torrents": {
                    "$slice": [torrent_index, 1],
                },
            },
        )

        if document is None:
            return None

        torrents = document.get("torrents", [])

        if not torrents:
            return None

        files = torrents[0].get("files", {})

        if not isinstance(files, dict):
            return {}

        return files
