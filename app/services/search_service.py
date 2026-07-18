from typing import TYPE_CHECKING

from models.search_filters import SearchFilters  # noqa
from models.search_item import SearchItem, SearchPage, TorrentOption

if TYPE_CHECKING:
    from models.mongo_docs import RawTorrentPage
    from repositories.torrent_repository import TorrentRepository


class SearchService:
    def __init__(self, repository: TorrentRepository) -> None:
        self._repository = repository

    def search(
        self,
        filters: SearchFilters,
        page: int = 1,
        page_size: int = 10,
    ) -> SearchPage:
        documents, has_more = self._repository.search_by_title(
            filters=filters,
            page=page,
            page_size=page_size,
        )

        items = tuple(
            self._to_search_item(document=document, filters=filters)
            for document in documents
        )

        return SearchPage(
            items=items,
            page=max(page, 1),
            has_more=has_more,
        )

    @staticmethod
    def _to_search_item(
        document: RawTorrentPage, filters: SearchFilters
    ) -> SearchItem:

        torrents = tuple(
            sorted(
                (
                    TorrentOption(
                        index=torrent_index,
                        title=torrent.get(
                            "title",
                            "Torrent Sem titulo",
                        ),
                        magnet=torrent.get(
                            "magnet",
                            "",
                        ),
                        size=int(torrent.get("size", 0)),
                        seeds=int(torrent.get("seeds", 0) or 0),
                        peers=int(torrent.get("peers", 0) or 0),
                        leechers=int(torrent.get("leechers", 0) or 0),
                        dead=bool(torrent.get("dead", False)),
                    )
                    for torrent_index, torrent in enumerate(
                        document.get("torrents", [])
                    )
                    if int(torrent.get("seeds", 0) or 0) >= filters.min_seeders
                    if (
                        filters.show_dead
                        or not bool(torrent.get("dead", False))
                    )
                ),
                key=lambda torrent: torrent.seeds,
                reverse=True,
            )
        )

        document_id = document.get("_id")

        return SearchItem(
            id=str(document_id) if document_id else "",
            title=document.get(
                "title",
                "Resultado sem titulo",
            ),
            link=document.get("link", ""),
            torrents=torrents,
        )

    def get_torrent_files(
        self,
        item_id: str,
        torrent_index: int,
    ) -> dict[str, object] | None:
        return self._repository.get_torrent_files(
            item_id=item_id, torrent_index=torrent_index
        )
