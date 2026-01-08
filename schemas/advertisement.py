from pydantic import BaseModel


class AdvertisementCreate(BaseModel):
    title: str
    image_url: str
    trip_id: str
