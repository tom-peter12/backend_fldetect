import numpy as np
import json


from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.routers.testing import evaluate_model
from .. import models, schemas, utils
from ..database import SessionLocal, get_db
from fastapi.responses import JSONResponse
from uuid import uuid4
import torch

THRESHOLD = 4



def delete_client_weights(session):
    try:
        session.query(models.Model).delete()
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error deleting client weights: {e}")


def fetch_all_weights(session):
    try:
        all_weights_objs = session.query(models.Model).all()
        return [weight_obj.client_weights for weight_obj in all_weights_objs]
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error fetching client weights: {e}")
        return []

# with SessionLocal() as session:
#     all_weights = fetch_all_weights(session)


def save_aggregated_model(session, aggregated_model):
    try:
        aggregated_model_obj = models.Aggregated_Model(aggregated_weight=aggregated_model)
        session.add(aggregated_model_obj)
        session.commit()
        session.refresh(aggregated_model_obj)
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error saving aggregated model: {e}")


def federated_averaging(local_models):
    
    if not local_models:
        raise ValueError("No local models provided for averaging.")
    
    aggregated_updates = [np.zeros_like(layer) for layer in local_models[0]]

    num_devices = len(local_models)
    # federated_averaging
    for local_model in local_models:
        for idx, layer in enumerate(local_model):
            aggregated_updates[idx] += np.array(layer)
    
    for idx, total_weight in enumerate(aggregated_updates):
        aggregated_updates[idx] = (total_weight / num_devices).tolist()
    
    return aggregated_updates




with SessionLocal() as session:


    try:
        all_weights = fetch_all_weights(session)
        print(len(all_weights))
        
        if len(all_weights) >= THRESHOLD:
            aggregated_model = federated_averaging(all_weights)
            
            save_aggregated_model(session, aggregated_model)
            
            delete_client_weights(session)




        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error in the aggregation process: {e}")
    finally:
        session.close()





router = APIRouter(tags=['Federated Learning End Point'])

@router.post("/get_averaged_weights/")
def get_averaged_weights(request: schemas.ClientRequest, db: Session = Depends(get_db)): 

    weights_entry = db.query(models.Aggregated_Model).order_by(models.Aggregated_Model.id.desc()).first()
    model_entry = db.query(models.The_Model).order_by(models.The_Model.id.desc()).first()

    if not weights_entry:
        raise HTTPException(status_code=404, detail="No averaged weights found in the database.")

    if request.flag == 1:
        return {"averaged_weights": weights_entry.aggregated_weight}
    elif request.flag == 0:
        return {
            "model": model_entry.model,
            "averaged_weights": weights_entry.aggregated_weight
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid flag value.")



