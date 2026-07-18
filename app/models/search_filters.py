from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SearchFilters:
    query: str = ""
    min_seeders: int = 0
    show_dead: bool = False

    @classmethod
    def create(
        cls,
        query: str,
        min_seeders: int,
        *,
        show_dead: bool,
    ) -> SearchFilters:
        return cls(
            query=query.strip(),
            min_seeders=max(min_seeders, 0),
            show_dead=show_dead,
        )
