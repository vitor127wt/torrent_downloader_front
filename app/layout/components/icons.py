import fasthtml.common as ft
import fasthtml.svg as svg


def _Icon(
    *children: ft.FT,
    cls: str = "icon",
) -> ft.FT:
    return svg.Svg(
        *children,
        viewBox="0 0 24 24",
        fill="none",
        stroke="currentColor",
        width="20",
        height="20",
        cls=cls,
        **{
            "aria-hidden": "true",
            "focusable": "false",
            "stroke-width": "2",
            "stroke-linecap": "round",
            "stroke-linejoin": "round",
        },
    )


def SearchIcon(cls: str = "icon") -> ft.FT:
    return _Icon(
        svg.Circle(cx=11, cy=11, r="7"),
        svg.Path(d="m20 20-3.5-3.5"),
        cls=cls,
    )


def MagnetIcon(cls: str = "icon") -> ft.FT:
    return _Icon(
        svg.Path(d="M6 3v9a6 6 0 0 0 12 0V3"),
        svg.Path(d="M6 7h4"),
        svg.Path(d="M14 7h4"),
        cls=cls,
    )


def ExternalLinkIcon(cls: str = "icon") -> ft.FT:
    return _Icon(
        svg.Path(d="M15 3h6v6"),
        svg.Path(d="M10 14 21 3"),
        svg.Path(
            d=("M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6")
        ),
        cls=cls,
    )


def FolderIcon(cls: str = "icon") -> ft.FT:
    return _Icon(
        svg.Path(
            d=(
                "M3 6a2 2 0 0 1 2-2h5"
                "l2 3h7a2 2 0 0 1 2 2v9"
                "a2 2 0 0 1-2 2H5"
                "a2 2 0 0 1-2-2Z"
            )
        ),
        cls=cls,
    )


def FileIcon(cls: str = "icon") -> ft.FT:
    return _Icon(
        svg.Path(
            d=("M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z")
        ),
        svg.Polyline(points="14 2 14 8 20 8"),
        cls=cls,
    )


def ChevronRightIcon(cls: str = "icon") -> ft.FT:
    return _Icon(
        svg.Polyline(points="9 18 15 12 9 6"),
        cls=cls,
    )


def CheckCircleIcon(cls: str = "icon") -> ft.FT:
    return _Icon(
        svg.Circle(cx=12, cy=12, r="9"),
        svg.Path(d="m8.5 12 2.2 2.2 4.8-5"),
        cls=cls,
    )


def XCircleIcon(cls: str = "icon") -> ft.FT:
    return _Icon(
        svg.Circle(cx=12, cy=12, r="9"),
        svg.Path(d="m9 9 6 6"),
        svg.Path(d="m15 9-6 6"),
        cls=cls,
    )


def DownloadIcon(cls: str = "icon") -> ft.FT:
    return _Icon(
        svg.Path(d="M12 3v11"),
        svg.Path(d="m7 11 5 5 5-5"),
        svg.Path(d="M5 21h14"),
        cls=cls,
    )


def VideoFileIcon(cls: str = "icon") -> ft.FT:
    return _Icon(
        svg.Path(
            d=("M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z")
        ),
        svg.Polyline(points="14 2 14 8 20 8"),
        svg.Path(d="m10 11 5 3-5 3z"),
        cls=cls,
    )
