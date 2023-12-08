import numpy as np
import json

import tensorflow as tf



from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import models, schemas, utils
from ..database import SessionLocal, get_db
from fastapi.responses import JSONResponse
from uuid import uuid4

from sqlalchemy.orm import Session

import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

input_dim = 23

class AEModel():
    def __init__(self):
        super(AEModel, self).__init__()

        self.model = self._build_model()

    def _get_safe_units(self, fraction):
        units = max(int(tf.math.ceil(fraction * input_dim)), 1)
        return units

    def _build_model(self):
        encoder = tf.keras.Sequential()
        encoder.add(tf.keras.layers.Dense(units=self._get_safe_units(0.75), activation='relu', input_shape=(input_dim,)))
        encoder.add(tf.keras.layers.Dense(units=self._get_safe_units(0.5), activation='relu'))
        encoder.add(tf.keras.layers.Dense(units=self._get_safe_units(0.33), activation='relu'))
        encoder.add(tf.keras.layers.Dense(units=self._get_safe_units(0.25), activation='relu'))

        print(encoder.summary())

        # Building the decoder
        # decoder = tf.keras.Sequential()
        # encoder.add(tf.keras.layers.Dense(units=self._get_safe_units(0.33), activation='relu', input_shape=(self._get_safe_units(0.25),)))
        # # encoder.add(tf.keras.layers.Dense(units=self._get_safe_units(0.33), activation='relu', input_shape=(self._get_safe_units(0.25),)))
        # encoder.add(tf.keras.layers.Dense(units=self._get_safe_units(0.5), activation='relu'))
        # encoder.add(tf.keras.layers.Dense(units=self._get_safe_units(0.75), activation='relu'))
        # encoder.add(tf.keras.layers.Dense(units=input_dim, activation='sigmoid'))

        encoder.add(tf.keras.layers.Dense(units=2, activation='relu', input_shape=(6,)))
        encoder.add(tf.keras.layers.Dense(units=12, activation='relu'))
        encoder.add(tf.keras.layers.Dense(units=18, activation='relu'))
        encoder.add(tf.keras.layers.Dense(units=23, activation='relu'))


        # print(decoder.summary())

        # Building the autoencoder
        # autoencoder = tf.keras.Sequential([encoder, decoder])
        encoder.compile(optimizer='adam', loss='mean_squared_error')
    
        return encoder




def fetch_latest_weight():
    db = next(get_db())

    try:
        latest_weight_obj = db.query(models.Aggregated_Model).order_by(models.Aggregated_Model.id.desc()).first()
        return latest_weight_obj.aggregated_weight if latest_weight_obj else None
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error fetching latest client weight: {e}")
        return None
    finally:
        db.close()


def load_model_weights(model):
    serialized_weights = fetch_latest_weight()
    layer_index = 0
    print("output this thing biatch", len(model.model.layers))

    # Iterate over the serialized weights assuming each layer's weights and biases are in sequence
    for i in range(0, len(serialized_weights), 2):
        layer_weights = np.array(serialized_weights[i])
        layer_biases = np.array(serialized_weights[i + 1]) if i + 1 < len(serialized_weights) else None

        # Set weights and biases for each layer
        if layer_biases is not None:
            if len(model.model.layers) > layer_index:
                model.model.layers[layer_index].set_weights([layer_weights, layer_biases])
                layer_index += 1
            else:
                print(f"Extra weights found for non-existent layer index: {layer_index}")
        else:
            print(f"Missing biases for layer index: {layer_index}")

    if layer_index != len(model.model.layers):
        print(f"Warning: Number of layers in the model ({len(model.model.layers)}) does not match provided weights ({layer_index})")
 # serialized_weights is your provided weights list


def evaluate_model(data_path):
    data = pd.read_csv(data_path)
    X = data
    # X = data.drop('Label', axis=1)
    Y = np.round(data['Label']).astype(int)

    model = AEModel()
    load_model_weights(model)
    print(model.model.summary())

    Y_pred = model.model.predict(X)
    Y_pred = np.round(Y_pred).astype(int)[:, 0]
    # print("this is Y", Y)
    # print("this is Y_pred", Y_pred)

    accuracy = accuracy_score(Y, Y_pred)
    precision = precision_score(Y, Y_pred)
    recall = recall_score(Y, Y_pred)
    f1 = f1_score(Y, Y_pred)

    print(f'Accuracy: {accuracy}')
    print(f'Precision: {precision}')
    print(f'Recall: {recall}')
    print(f'F1 Score: {f1}')

evaluate_model('/home/tomas/Desktop/RA/Safa Otoum/fldetect/backend/app/data/Data.csv')
