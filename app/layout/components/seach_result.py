from collections.abc import Sequence  # noqa

import fasthtml.common as ft
from datetime import datetime, UTC
from models.search_item import (  # noqa
    SearchItem,
    SearchPage,
    TorrentOption,
)

from layout.components.icons import (
    DownloadIcon,
    ExternalLinkIcon,
    FolderIcon,
    ClockIcon,
    ActivityIcon,
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


def format_relative_time(
    timestamp: float | None,
) -> str:
    if timestamp is None:
        return "Não verificado"

    checked_at = datetime.fromtimestamp(
        timestamp,
        tz=UTC,
    )

    now = datetime.now(UTC)
    seconds = max(
        int((now - checked_at).total_seconds()),
        0,
    )

    if seconds < 15:
        return "Verificado agora"

    if seconds < 60:
        return f"Há {seconds} segundos"

    minutes = seconds // 60

    if minutes < 60:
        return "Há 1 minuto" if minutes == 1 else f"Há {minutes} minutos"

    hours = minutes // 60

    if hours < 24:
        return "Há 1 hora" if hours == 1 else f"Há {hours} horas"

    days = hours // 24

    if days < 30:
        return "Há 1 dia" if days == 1 else f"Há {days} dias"

    months = days // 30

    if months < 12:
        return "Há 1 mês" if months == 1 else f"Há {months} meses"

    years = days // 365

    return "Há 1 ano" if years == 1 else f"Há {years} anos"


def LastCheckedChip(
    timestamp: float | None,
) -> ft.FT:
    if timestamp is None:
        exact_time = "Sem data de verificação"
    else:
        checked_at = datetime.fromtimestamp(
            timestamp,
            tz=UTC,
        )

        exact_time = checked_at.strftime("Verificado em %d/%m/%Y às %H:%M UTC")

    return ft.Span(
        ClockIcon(cls="status-icon"),
        ft.Span(format_relative_time(timestamp)),
        title=exact_time,
        cls="last-checked-chip",
    )


def TorrentHealthChip(
    torrent: TorrentOption,
) -> ft.FT:
    if torrent.dead:
        label = "Inativo"
        modifier = "is-dead"
    elif torrent.seeds >= 20:
        label = "Excelente"
        modifier = "is-excellent"
    elif torrent.seeds >= 5:
        label = "Saudável"
        modifier = "is-healthy"
    elif torrent.seeds >= 1:
        label = "Disponível"
        modifier = "is-available"
    else:
        label = "Sem fontes"
        modifier = "is-no-seeds"

    return ft.Span(
        ActivityIcon(cls="status-icon"),
        ft.Span(label),
        title=(f"{torrent.seeds} seeds; dead={torrent.dead}"),
        cls=f"torrent-health-chip {modifier}",
    )


def BestTorrent(
    item: SearchItem,
) -> TorrentOption | None:
    if not item.torrents:
        return None

    # Os torrents já estão ordenados por seeds.
    # Preferimos o primeiro que não esteja morto.
    return next(
        (torrent for torrent in item.torrents if not torrent.dead),
        item.torrents[0],
    )


def ResultSummary(item: SearchItem) -> ft.FT:
    torrent_count = len(item.torrents)
    best_torrent = BestTorrent(item)

    count_label = (
        "1 torrent" if torrent_count == 1 else f"{torrent_count} torrents"
    )

    badges: list[ft.FT] = [
        ft.Span(
            count_label,
            cls="result-summary-badge",
        )
    ]

    if best_torrent is not None:
        badges.extend(
            (
                ft.Span(
                    f"{best_torrent.seeds} seeds",
                    cls="result-summary-badge is-seeds",
                ),
                ft.Span(
                    format_torrent_size(best_torrent.size),
                    cls="result-summary-badge is-size",
                ),
            )
        )

    return ft.Div(
        ft.Strong(
            item.title,
            cls="result-summary-title",
        ),
        ft.Div(
            *badges,
            cls="result-summary-badges",
        ),
        cls="result-summary",
    )


def ResultActionBar(item: SearchItem) -> ft.FT:
    best_torrent = BestTorrent(item)
    actions: list[ft.FT] = []

    if best_torrent is not None and best_torrent.magnet:
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
                ft.Span("Página de origem"),
                href=item.link,
                target="_blank",
                rel="noopener noreferrer",
                cls="source-link",
            )
        )

    if best_torrent is None:
        description = "Nenhuma opção de torrent encontrada."
    elif best_torrent.dead:
        description = "Melhor opção encontrada, mas marcada como inativa."
    else:
        description = (
            f"{best_torrent.seeds} seeds · "
            f"{format_torrent_size(best_torrent.size)}"
        )

    action_content = (
        ft.Div(
            *actions,
            cls="result-card-actions",
        )
        if actions
        else ft.Span(
            "Links indisponíveis",
            cls="result-links-unavailable",
        )
    )

    return ft.Div(
        ft.Div(
            ft.Strong("Melhor opção disponível"),
            ft.Small(description),
            cls="result-action-copy",
        ),
        action_content,
        cls="result-action-bar",
    )


def TorrentRow(
    item_id: str,
    torrent: TorrentOption,
) -> ft.FT:
    files_target_id = f"torrent-files-{item_id}-{torrent.index}"
    loading_id = f"torrent-files-loading-{item_id}-{torrent.index}"

    return ft.Div(
        ft.Div(
            ft.Span(f"Tamanho: {format_torrent_size(torrent.size)}"),
            ft.Span(f"Seeds: {torrent.seeds}"),
            ft.Span(f"Peers: {torrent.peers}"),
            ft.Span(f"Leechers: {torrent.leechers}"),
            LastCheckedChip(torrent.last_checked),
            TorrentHealthChip(torrent),
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
    return ft.Details(
        ft.Summary(
            ResultSummary(item),
        ),
        ft.Div(
            ResultActionBar(item),
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
