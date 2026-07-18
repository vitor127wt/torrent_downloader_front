import fasthtml.common as ft
from config import load_settings
from database.mongo import MongoDataBase
from repositories.torrent_repository import TorrentRepository
from routes.search import create_search_router
from services.search_service import SearchService

settings = load_settings()

mongo_database = MongoDataBase(settings)
mongo_database.ping()

collection = mongo_database.torrent_pages


torrent_repository = TorrentRepository(mongo_database.torrent_pages)
search_service = SearchService(torrent_repository)

SEARCH_PAGE_SIZE = 10
app, _ = ft.fast_app(
    pico=False,
    hdrs=(
        ft.Link(
            rel="stylesheet",
            href="/static/css/new_style.css",
        ),
    ),
    on_shutdown=[
        mongo_database.close,
    ],
)

search_router = create_search_router(search_service=search_service)

search_router.to_app(app)

ft.serve()
