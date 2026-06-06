from pydantic import BaseModel, Field

from app.core.schemas import MetaInfo


class CreateArtistRequest(BaseModel):
    artist_name: str = Field(..., max_length=50, example="Leo/need")
    unit_name: str | None = Field(None, max_length=50, example="Leo/need")


class ArtistResponse(BaseModel):
    id: int
    artist_name: str
    unit_name: str | None
    meta_info: MetaInfo
