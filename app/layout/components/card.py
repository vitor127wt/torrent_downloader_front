import fasthtml.common as ft


def Card(*components: ft.FT, cls: str = "card") -> ft.FT:
    return ft.Div(
        *components,
        cls=cls,
    )
