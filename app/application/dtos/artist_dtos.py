from dataclasses import dataclass

from app.application.dtos.base_dtos import MetaDto


@dataclass(frozen=True)
class ArtistDto:
    id: int
    artist_name: str
    meta_info: MetaDto
    unit_name: str | None = None
