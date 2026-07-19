from typing import TYPE_CHECKING, Any
from urllib.parse import urlencode

import fasthtml.common as ft

from app.layout.components.file_tree import FileTree
from app.layout.components.icons import SearchIcon
from app.layout.components.seach_result import (
    SearchResults,
    SearchResultsBatch,
)
from app.layout.components.search_form import SearchForm
from app.layout.layout import BasePage, Page
from app.models.search_filters import SearchFilters

if TYPE_CHECKING:
    from services.search_service import SearchService

SEARCH_PAGE_SIZE = 10


def create_search_router(  # noqa
    search_service: SearchService,
) -> ft.APIRouter:

    def make_filters(
        query: str, min_seeders: int, *, show_dead: bool
    ) -> SearchFilters:
        return SearchFilters.create(
            query=query,
            min_seeders=min_seeders,
            show_dead=show_dead,
        )

    def make_page_url(filters: SearchFilters) -> str:
        parameters: dict[str, str | int] = {}

        if filters.query:
            parameters["query"] = filters.query
        if filters.min_seeders > 0:
            parameters["min_seeders"] = filters.min_seeders
        if filters.show_dead:
            parameters["show_dead"] = filters.show_dead

        if not parameters:
            return "/"

        return f"/?{urlencode(parameters)}"

    def make_load_more_url(filters: SearchFilters, page: int) -> str:
        parameters: dict[str, str | int] = {
            "query": filters.query,
            "page": page,
        }

        if filters.min_seeders > 0:
            parameters["min_seeders"] = filters.min_seeders
        if filters.show_dead:
            parameters["show_dead"] = filters.show_dead

        return f"/search/more?{urlencode(parameters)}"

    router = ft.APIRouter()

    @router("/search/more")
    def search_more(
        query: str = "",
        page: int = 2,
        min_seeders: int = 0,
        *,
        show_dead: bool = False,
    ) -> tuple[ft.FT, ...]:
        safe_page = max(page, 2)

        filters = make_filters(
            query=query,
            min_seeders=min_seeders,
            show_dead=show_dead,
        )

        result = search_service.search(
            filters=filters,
            page=safe_page,
            page_size=SEARCH_PAGE_SIZE,
        )

        load_more_url = (
            make_load_more_url(  # type: ignore
                filters=filters,
                page=safe_page + 1,
            )
            if result.has_more
            else None
        )

        return SearchResultsBatch(result=result, load_more_url=load_more_url)

    @router("/search/")
    def search(
        query: str = "",
        min_seeders: int = 0,
        *,
        show_dead: bool = False,
    ) -> tuple[ft.FT, Any]:

        filters = make_filters(
            query=query, min_seeders=min_seeders, show_dead=show_dead
        )

        result = search_service.search(
            filters=filters,
            page=1,
            page_size=SEARCH_PAGE_SIZE,
        )

        load_more_url = (
            make_load_more_url(  # type: ignore
                filters=filters,
                page=2,
            )
            if result.has_more
            else None
        )

        return (
            SearchResults(
                result=result,
                query=filters.query,
                load_more_url=load_more_url,
            ),
            ft.HtmxResponseHeaders(replace_url=make_page_url(filters=filters)),
        )

    @router("/torrent-files/{item_id}/{torrent_index}")
    def torrent_files(
        item_id: str,
        torrent_index: int,
    ) -> ft.FT:
        files = search_service.get_torrent_files(
            item_id=item_id,
            torrent_index=torrent_index,
        )

        return FileTree(files)

    @router("/")
    def home(
        query: str = "", min_seeders: int = 0, *, show_dead: bool = False
    ) -> Page:

        filters = make_filters(
            query=query,
            min_seeders=min_seeders,
            show_dead=show_dead,
        )

        result = search_service.search(
            filters=filters,
            page=1,
            page_size=SEARCH_PAGE_SIZE,
        )

        load_more_url = (
            make_load_more_url(  # type: ignore
                filters=filters,
                page=2,
            )
            if result.has_more
            else None
        )

        return BasePage(
            "The Torrent DataBase",
            ft.Section(
                ft.Div(
                    ft.Div(
                        SearchIcon(cls="hero-kicker-icon"),
                        ft.Span("Busca de filmes e séries"),
                        cls="hero-kicker",
                    ),
                    ft.H1(
                        "Encontre torrents de forma ",
                        ft.Span(
                            "rápida e organizada",
                            cls="hero-highlight",
                        ),
                    ),
                    ft.P(
                        "Pesquise no catálogo, filtre por disponibilidade "
                        "e visualize os arquivos antes de abrir o magnet.",
                        cls="search-description",
                    ),
                    cls="hero-copy",
                ),
                SearchForm(
                    search_url=search.to(),  # type:ignore
                    filters=filters,
                ),
                cls="search-section search-hero",
            ),
            ft.Div(
                SearchResults(
                    result=result,
                    query=filters.query,
                    load_more_url=load_more_url,
                ),
                id="search-results",
            ),
        )

    return router
