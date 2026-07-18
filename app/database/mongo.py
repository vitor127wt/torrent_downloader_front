from typing import TYPE_CHECKING

from pymongo import MongoClient

if TYPE_CHECKING:
    from config import Settings
    from models.mongo_docs import RawTorrentPage
    from pymongo.collection import Collection
    from pymongo.database import Database


class MongoDataBase:
    def __init__(self, settings: Settings) -> None:
        self._client: MongoClient[RawTorrentPage] = MongoClient(
            settings.mongo_uri,
            serverselectiontimeoutms=30000,
        )

        self._database: Database[RawTorrentPage] = self._client[
            settings.mongo_database
        ]

        self.torrent_pages: Collection[RawTorrentPage] = self._database[
            settings.mongo_collection
        ]

    def ping(self) -> None:
        self._client.admin.command("ping")

    def close(self) -> None:
        self._client.close()
