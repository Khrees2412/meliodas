import csv, json
from typing import List
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response, status, File, UploadFile
# from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from api import crud, models, schemas
from api.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

load_dotenv()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db():
    data_dict = {
        "CustomerWind" : "Turbine01",
        "CustomerSolar" : "SolarFarm01"
    }
    for key, value in data_dict.items():
        db = SessionLocal()
        crud.create_tables(db, key, value)

# create_db()


@app.post("/customer/{customer_name}/")
def ingest_data(customer_name:str, response: Response, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Convert the file bytes to a string
    file_str = file.file.read().decode()

    customer = crud.get_customer(db, customer_name)
    if customer is None:
        raise HTTPException(status_code=404, detail="Not found, try creating a customer first")
    
    asset = crud.get_asset(db, customer)

    response.status_code = status.HTTP_200_OK
    # Parse the CSV file using the csv module
    reader = csv.DictReader(file_str.splitlines())
    # Convert the data to a list of dictionaries
    data = list(reader)
    # Convert the data to a dictionary and prettify it
    data_dict = json.loads(json.dumps(data))
    prettified_dict = json.dumps(data_dict, indent=4)

    data = json.loads(prettified_dict)

    timeseries_id = 0
    for d in data:
        timestamp = d["timestamp"]
        del d["timestamp"]
        for label, value in d.items():
            if(len(label) < 1) or label == "Unnamed: 0":
                pass
            else:
                timeseries_id += 1
                crud.insert_timeseries(db, asset, label)
                crud.insert_datapoints(db, asset, label, timeseries_id, timestamp, value)

    return data[:5]

@app.get("/datapoints/{asset_name}/", response_model=List[schemas.Datapoint])
def get_datapoints(asset_name:str, response: Response, db: Session = Depends(get_db)):
    response.status_code = status.HTTP_200_OK
    return crud.get_datapoint_list(db, asset_name)


@app.get("/timeseries/{asset_name}/" ,response_model=List[schemas.Timeseries])
# , response_model=List[schemas.Timeseries]
def get_timeseries(asset_name:str, response: Response, db: Session = Depends(get_db)):
    response.status_code = status.HTTP_200_OK
    timeseries = crud.get_timeseries_list(db, asset_name)

    for t in timeseries:
        pass
    return timeseries

@app.get("/customers/", response_model=List[schemas.Customer])
def get_customers(response: Response, db: Session = Depends(get_db)):
    response.status_code = status.HTTP_200_OK
    customers = crud.get_customer_list(db)
    return customers