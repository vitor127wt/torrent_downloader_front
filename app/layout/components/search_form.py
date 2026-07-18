import fasthtml.common as ft
from layout.components.icons import SearchIcon
from models.search_filters import SearchFilters  # noqa


def SearchForm(search_url: str, filters: SearchFilters) -> ft.FT:
    return ft.Form(
        ft.Div(
            ft.Input(
                id="search-query",
                type="search",
                name="query",
                value=filters.query,
                placeholder="Digiteo nome de um filme ou serie...",
                autocomplete="off",
                autofocus=True,
                spellcheck=False,
            ),
            ft.Button(
                SearchIcon(cls="button-icon"),
                ft.Span("Buscar"),
                type="submit",
            ),
            cls="search-main-fields",
        ),
        ft.Div(
            ft.Label(
                "Mínimo de seeds",
                ft.Input(
                    id="min-seeders",
                    type="number",
                    name="min_seeders",
                    value=str(filters.min_seeders),
                    min="0",
                    step="1",
                    cls="seed-input",
                ),
                cls="filter-field seed-filter",
            ),
            ft.Label(
                ft.Input(
                    id="show-dead",
                    type="checkbox",
                    name="show_dead",
                    value="true",
                    checked=filters.show_dead,
                    cls="dead-toggle-input",
                ),
                ft.Span("Incluir torrents inativos"),
                cls="filter-checkbox dead-toggle",
            ),
            cls="search-filters",
        ),
        ft.Span(
            "Buscando...",
            id="search-loading",
            cls="htmx-indicator",
        ),
        action="/",
        method="get",
        hx_get=search_url,
        hx_trigger=("submit, input changed delay:450ms"),
        hx_target="#search-results",
        hx_swap="innerHTML",
        hx_indicator="#search-loarding",
        hx_sync="this:replace",
        cls="search-form",
    )
