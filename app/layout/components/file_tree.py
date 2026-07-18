import fasthtml.common as ft
from layout.components.icons import (
    ChevronRightIcon,
    FileIcon,
    FolderIcon,
    VideoFileIcon,
)

_META_KEYS = frozenset(
    {
        "type",
        "index",
        "size",
        "size_bytes",
    }
)
_VIDEO_EXTENSIONS = (
    ".mkv",
    ".mp4",
    ".avi",
    ".mov",
    ".wmv",
    ".flv",
    ".webm",
    ".m4v",
    ".mpg",
    ".mpeg",
)


def is_video_filename(name: str) -> bool:
    return name.lower().endswith(_VIDEO_EXTENSIONS)


def format_bytes(value: int | float | None) -> str:
    size = float(value or 0)

    units = ("B", "KB", "MB", "GB", "TB")
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"

    return f"{int(size)} {units[unit_index]}"


def is_file_node(value: object) -> bool:
    return isinstance(value, dict) and value.get("type") == "file"


def FileTreeEntry(
    name: str,
    value: object,
) -> ft.FT:
    if is_file_node(value):
        assert isinstance(value, dict)  # noqa

        size_label = format_bytes(value.get("size_bytes", 0))

        file_icon = (
            VideoFileIcon(cls="tree-file-icon is-video")
            if is_video_filename(name)
            else FileIcon(cls="tree-file-icon")
        )

        return ft.Div(
            file_icon,
            ft.Span(name),
            ft.Small(
                size_label,
                cls="file-tree-size",
            ),
            cls="file-tree-file",
        )

    if isinstance(value, dict):
        child_items = [
            (str(child_name), child_value)
            for child_name, child_value in value.items()
            if child_name not in _META_KEYS
        ]
        if not child_items:
            return ft.Div(
                ft.Span(name),
                ft.Small("Vazio"),
                cls="file-tree-empty",
            )

        return ft.Details(
            ft.Summary(
                ChevronRightIcon(cls="tree-chevron"),
                FolderIcon(cls="tree-folder-icon"),
                ft.Span(name),
            ),
            ft.Div(
                *(
                    FileTreeEntry(
                        child_name,
                        child_value,
                    )
                    for child_name, child_value in child_items
                ),
                cls="file-tree-branch",
            ),
            cls="file-tree-folder",
        )

    if isinstance(value, list):
        if not value:
            return ft.Div(
                ft.Span(name),
                ft.Small("Vazio"),
                cls="file-tree-empty",
            )

        return ft.Details(
            ft.Summary(
                ChevronRightIcon(cls="tree-chevron"),
                FolderIcon(cls="tree-folder-icon"),
                ft.Span(name),
            ),
            ft.Div(
                *(
                    FileTreeEntry(
                        child_name,
                        child_value,
                    )
                    for child_name, child_value in child_items
                ),
                cls="file-tree-branch",
            ),
            cls="file-tree-folder",
        )

    return ft.Div(
        FileIcon(cls="tree-file-icon"),
        ft.Span(name),
        ft.Small(
            size_label,
            cls="file-tree-size",
        ),
        cls="file-tree-file",
    )


def FileTree(files: dict[str, object] | None) -> ft.FT:
    if files is None:
        return ft.P(
            "Torrent ou lista de arquivos não encontrada",
            cls="files-message",
        )
    if not files:
        return ft.P(
            "Nenhum arquivo informado para este torrent.",
            cls="files-message",
        )
    return ft.Div(
        *(FileTreeEntry(str(name), value) for name, value in files.items()),
        cls="file-tree torrent files",
    )


def TorrentFilesResult(
    item_id: str, torrent_index: int, files: dict[str, object] | None
) -> ft.FT:
    return ft.Div(
        FileTree(files),
        id=f"torrent-files-{item_id}-{torrent_index}",
        cls="torrent-files",
    )
