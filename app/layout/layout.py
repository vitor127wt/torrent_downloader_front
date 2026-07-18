import fasthtml.common as ft

type Page = tuple[ft.FT, ...]


def BasePage(title: str, *components: ft.FT) -> Page:
    return (ft.Title(title), ft.Main(*components, cls="page-container"))
