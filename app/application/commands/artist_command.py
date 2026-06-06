from dataclasses import dataclass


@dataclass(frozen=True)
class CreateArtistCommand:
    artist_name: str
    unit_name: str | None = None
