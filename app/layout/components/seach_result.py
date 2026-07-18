from collections.abc import Sequence  # noqa

import fasthtml.common as ft

from models.search_item import (  # noqa
    SearchItem,
    SearchPage,
    TorrentOption,
)

from layout.components.icons import (
    CheckCircleIcon,
    DownloadIcon,
    ExternalLinkIcon,
    FolderIcon,
    XCircleIcon,
)


def format_torrent_size(value: int | float) -> str:
    size = float(value or 0)
    units = ("MB", "GB", "TB")
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    if unit_index == 0:
        return f"{size:.0f} {units[unit_index]}"

    return f"{size:.2f} {units[unit_index]}"


def TorrentStatusChip(dead: bool) -> ft.FT:  # noqa
    icon = (
        XCircleIcon(cls="status-icon")
        if dead
        else CheckCircleIcon(cls="status-icon")
    )
    return ft.Span(
        icon,
        ft.Span("Inativo" if dead else "Ativo"),
        cls=(f"torrent-status-chip {'is-dead' if dead else 'is alive'}"),
    )


def ResultHeaderCard(item: SearchItem) -> ft.FT:
    best_torrent = item.torrents[0] if item.torrents else None

    actions: list[ft.FT] = []

    if best_torrent and best_torrent.magnet:
        actions.append(
            ft.A(
                DownloadIcon(cls="button-icon"),
                ft.Span("Magnet"),
                href=best_torrent.magnet,
                cls="magnet-link",
            )
        )

    if item.link:
        actions.append(
            ft.A(
                ExternalLinkIcon(cls="button-icon"),
                ft.Span("Pagina de origem"),
                href=item.link,
                target="_blank",
                rel="noopener noreferrer",
                cls="source-link",
            )
        )

    return ft.Div(
        ft.Div(
            ft.Strong(item.title, cls="result-card-title"),
            ft.Small(
                f"{len(item.torrents)} torrent(s) encontrado(s)",
                cls="result-card-subtitle",
            ),
            cls="result-card-copy",
        ),
        ft.Div(
            *actions,
            cls="result-card-actions",
        ),
        cls="result-card",
    )


def TorrentRow(
    item_id: str,
    torrent: TorrentOption,
) -> ft.FT:
    files_target_id = f"torrent-files-{item_id}-{torrent.index}"
    loading_id = f"torrent-files-loading-{item_id}-{torrent.index}"

    return ft.Div(
        ft.Strong(torrent.title),
        ft.Div(
            ft.Span(f"Tamanho: {format_torrent_size(torrent.size)}"),
            ft.Span(f"Seeds: {torrent.seeds}"),
            ft.Span(f"Peers: {torrent.peers}"),
            ft.Span(f"Leechers: {torrent.leechers}"),
            TorrentStatusChip(torrent.dead),
            cls="torrent-metadata",
        ),
        ft.Div(
            ft.Button(
                FolderIcon(cls="button-icon"),
                ft.Span("Arquivos"),
                type="button",
                hx_get=f"/torrent-files/{item_id}/{torrent.index}",
                hx_target=f"#{files_target_id}",
                hx_swap="innerHTML",
                hx_indicator=f"#{loading_id}",
                hx_disabled_elt="this",
                cls="files-button",
            ),
            ft.Span(
                "Carregando arquivos...",
                id=loading_id,
                cls="htmx-indicator",
            ),
            cls="torrent-actions",
        ),
        ft.Div(
            id=files_target_id,
            cls="torrent-files-slot",
        ),
        cls="torrent-row",
    )


def SearchResult(item: SearchItem) -> ft.FT:
    torrent_count = len(item.torrents)

    return ft.Details(
        ft.Summary(
            ft.Div(
                ft.Strong(item.title),
                ft.Small(
                    f"{torrent_count} torrent(s) encontrado(s)",
                ),
                cls="result-heading",
            ),
        ),
        ft.Div(
            ResultHeaderCard(item),
            *(TorrentRow(item.id, torrent) for torrent in item.torrents),
            cls="result-content",
        ),
        cls="search-result",
    )


def LoadMoreButton(
    load_more_url: str | None,
) -> ft.FT:
    if load_more_url is None:
        return ft.P(
            "Fim dos resultados.",
            id="load-more",
            cls="results-end",
        )

    return ft.Div(
        ft.Button(
            "Carregar mais",
            type="button",
            hx_get=load_more_url,
            hx_target="#load-more",
            hx_swap="outerHTML",
            hx_indicator="#load-more-loading",
            hx_disabled_elt="this",
            cls="load-more-button",
        ),
        ft.Span(
            "Carregando...",
            id="load-more-loading",
            cls="htmx-indicator",
        ),
        id="load-more",
        cls="load-more",
    )


def SearchResults(
    result: SearchPage,
    query: str,
    load_more_url: str | None,
) -> ft.FT:
    normalized_query = query.strip()

    if not normalized_query:
        return ft.Div()

    if len(normalized_query) < 2:
        return ft.P(
            "Digite pelo menos dois caracteres.",
            cls="search-message",
        )

    if not result.items:
        return ft.P(
            f'Nenhum resultado encontrado para "{normalized_query}".',
            cls="search-message",
        )

    return ft.Div(
        ft.P(
            "Resultados encontrados",
            cls="results-count",
        ),
        *(SearchResult(item) for item in result.items),
        LoadMoreButton(load_more_url),
        cls="results-list",
    )


def SearchResultsBatch(
    result: SearchPage,
    load_more_url: str | None,
) -> tuple[ft.FT, ...]:
    return (
        *(SearchResult(item) for item in result.items),
        LoadMoreButton(load_more_url),
    )
