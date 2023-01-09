from typing import List, Union

from pydantic import BaseModel


class Asset(BaseModel):
    name: str
    class Config:
        orm_mode = True

class AssetRes(Asset):
     customer_name: str

class Customer(BaseModel):
    name: str
    assets: Union[List[Asset], None]
    class Config:
        orm_mode = True

class CustomerUpdate(Customer):
    pass

class Datapoint(BaseModel):
    timeseries_label: str
    timestamp: str
    value: str
    class Config:
        orm_mode = True

class DatapointRes(Datapoint):
    timeseries_label: str
    datapoint : Datapoint
    class Config:
        orm_mode = True

class Timeseries(BaseModel):
    label: str
    datapoints: Union[List[Datapoint], None]
    class Config:
        orm_mode = True