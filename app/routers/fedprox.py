# import tensorflow as tf
# from tensorflow import keras
import numpy as np
import json


from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.routers.fedavg import delete_client_weights, fetch_all_weights, save_aggregated_model
from .. import models, schemas, utils
from ..database import SessionLocal, get_db
from fastapi.responses import JSONResponse



MU = 0.001
THRESHOLD = 4

def fedprox_aggregation(local_models, global_model):

    if not local_models:
        raise ValueError("No local models provided for aggregation.")
    
    aggregated_updates = [[0 for _ in layer] for layer in global_model]
    num_devices = len(local_models)
    
    for local_model in local_models:
        for layer_idx, layer in enumerate(local_model):
            for weight_idx, weight in enumerate(layer):
                proximal_term = MU * (weight - global_model[layer_idx][weight_idx])
                aggregated_updates[layer_idx][weight_idx] += weight + proximal_term
    
    # Average the updates
    for layer_idx, layer_total in enumerate(aggregated_updates):
        for weight_idx, total_weight in enumerate(layer_total):
            aggregated_updates[layer_idx][weight_idx] = total_weight / num_devices
    
    return aggregated_updates


with SessionLocal() as session:

    try:
        all_weights = fetch_all_weights(session)
        print(len(all_weights))

        if len(all_weights) >= THRESHOLD:
            global_model = session.query(models.Aggregated_Model).order_by(models.Aggregated_Model.id.desc()).first()


            aggregated_model = fedprox_aggregation(all_weights, global_model)
            
            save_aggregated_model(session, aggregated_model)
            
            delete_client_weights(session)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error in the aggregation process: {e}")
    finally:
        session.close()


