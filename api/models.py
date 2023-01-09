from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    name = Column(String, primary_key=True)

    assets = relationship("Asset", back_populates="customer")

class Asset(Base):
    __tablename__ = 'assets'
    name = Column(String, primary_key=True)
    customer_name = Column(String, ForeignKey('customers.name'))

    customer = relationship("Customer", back_populates="assets")
    timeseries = relationship("Timeseries", back_populates="asset")
    

class Timeseries(Base):
    __tablename__ = 'timeseries'
    timeseries_id = Column(Integer)
    label = Column(String, primary_key=True)
    asset_name = Column(String, ForeignKey('assets.name'))

    asset = relationship("Asset", back_populates="timeseries")
    datapoints = relationship("Datapoint", back_populates="timeseries")

class Datapoint(Base):
    __tablename__ = 'datapoints'
    datapoint_id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    timeseries_label = Column(String, ForeignKey('timeseries.label'))
    timeseries_id = Column(Integer)
    value = Column(String)
    asset_name = Column(String)

    timeseries = relationship("Timeseries", back_populates="datapoints")
