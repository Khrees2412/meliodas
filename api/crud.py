from typing import List
from sqlalchemy.orm import Session

from . import models, schemas

def insert_timeseries(db: Session, asset_name: str, label: str):
    timeseries = models.Timeseries(asset_name = asset_name, label = label)
    d = get_timeseries(db, asset_name, label)
    if d is not None:
        return "already exists"
    db.add(timeseries)
    db.commit()
    db.refresh(timeseries)
    return "done"

def get_timeseries(db: Session, asset_name: str, label: str):
    return db.query(models.Timeseries).filter(models.Timeseries.asset_name == asset_name, models.Timeseries.label == label).first()

def get_timeseries_list(db: Session, asset_name: str):
    return db.query(models.Timeseries).filter(models.Timeseries.asset_name == asset_name).all()
    # return db.query(models.Timeseries, models.Datapoint).filter(models.Timeseries.asset_name == asset_name).outerjoin(models.Timeseries, models.Timeseries.label == models.Datapoint.timeseries_label).group_by(models.Timeseries.label).all()


def insert_datapoints(db: Session, asset_name: str, label:str, timeseries_id:str, timestamp: str, value: str):
    datapoint = models.Datapoint(asset_name = asset_name, timeseries_id = timeseries_id,  timeseries_label = label, timestamp = timestamp, value = value)
    db.add(datapoint)
    db.commit()
    db.refresh(datapoint)
    return "done"

def get_datapoint(db: Session, asset_name: str, timestamp: str):
    return db.query(models.Datapoint).filter(models.Datapoint.asset_name == asset_name, models.Datapoint.timestamp == timestamp).first()

def get_datapoint_list(db: Session, asset_name: str):
    return db.query(models.Datapoint).filter(models.Datapoint.asset_name == asset_name).all()

def create_tables(db: Session, customer: str, asset: str):
    db_customer = models.Customer(name = customer)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    db_asset = models.Asset(name = asset, customer_name = customer)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return "done"

def get_customer(db:Session, customer_name: str) -> str:
    return db.query(models.Customer).filter(models.Customer.name == customer_name).first()

def get_customer_list(db:Session) -> List[str]:
    return db.query(models.Customer).all()
    

def get_asset(db:Session, customer_name: str) -> str:
    a = db.query(models.Asset).filter(models.Asset.customer == customer_name).first()
    return a.name
   
