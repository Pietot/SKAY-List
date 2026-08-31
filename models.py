from pydantic import BaseModel, Field


class Record(BaseModel):
    user: str = Field(..., description="The name of the player who achieved the record.")
    link: str = Field(..., description="The URL of the video showcasing the record.")
    hz: int = Field(..., description="The refresh rate (Hz) at which the record was achieved.")


class ExtremeDemon(BaseModel):
    id: int = Field(..., description="The unique identifier for the extreme demon.")
    name: str = Field(..., description="The name of the extreme demon.")
    author: str = Field(..., description="The author of the extreme demon.")
    creators: list[str] = Field(..., description="The creators of the extreme demon.")
    verifier: str = Field(..., description="The verifier of the extreme demon.")
    aredl_points: int = Field(..., description="The AREDL points of the extreme demon.")


class Challenge(BaseModel):
    id: int = Field(..., description="The unique identifier for the challenge.")
    name: str = Field(..., description="The name of the challenge.")
    author: str = Field(..., description="The author of the challenge.")
    creators: list[str] = Field(..., description="The creators of the challenge.")
    verifier: str = Field(..., description="The verifier of the challenge.")
