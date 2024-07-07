from typing import TypedDict

from pydantic import BaseModel, Field


class HourMinute(BaseModel):
    hour: int = Field(default=0, ge=0, le=23)
    minute: int = Field(default=0, ge=0, le=59)


class ShipmentStatus(BaseModel):
    index: int
    status: str
    location: str
    date: str | None
    time: HourMinute


# TODO: not implemented yet
class ParcelInfo(TypedDict):
    key: str
    value: str


class TrackingResult(BaseModel):
    parcel_info: list[ParcelInfo] = []
    tracking_list: list[ShipmentStatus] = []
