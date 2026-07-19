import os

import fasthtml.common as ft

from app.config import load_settings
from app.database.mongo import MongoDataBase
from app.repositories.torrent_repository import TorrentRepository
from app.routes.search import create_search_router
from app.services.search_service import SearchService

settings = load_settings()

mongo_database = MongoDataBase(settings)
mongo_database.ping()

collection = mongo_database.torrent_pages


torrent_repository = TorrentRepository(mongo_database.torrent_pages)
search_service = SearchService(torrent_repository)


session_secret = os.environ["SESSION_SECRET"].strip()

if not session_secret:
    raise RuntimeError("SESSION_SECRET está vazia.")  # noqa: TRY003, EM101

SEARCH_PAGE_SIZE = 10
app, rt = ft.fast_app(
    pico=False,
    secret_key=session_secret,
    key_fname="/tmp/.sesskey",  # noqa: S108
    hdrs=(
        ft.Link(
            rel="stylesheet",
            href="/app/static/css/style.css",
        ),
    ),
    on_shutdown=[
        mongo_database.close,
    ],
)


@rt("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


search_router = create_search_router(search_service=search_service)

search_router.to_app(app)

if __name__ == "__main__":
    ft.serve(
        host="0.0.0.0",  # noqa: S104
        appname="app.main",
        port=int(os.getenv("PORT", "5001")),
        reload=False,
    )
