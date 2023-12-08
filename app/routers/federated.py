from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# from app.routers.fedavg import federated_averaging, fetch_all_weights, save_aggregated_model



from .. import database, schemas, models, utils, oauth2

model_count_since_last_avg = 0




router = APIRouter(tags=['Federated Learning End Point'])


@router.post('/federated', status_code=status.HTTP_202_ACCEPTED, response_model=dict)
def upload_weights(weights_data: schemas.ClientWeights, db: Session = Depends(database.get_db)):

    global model_count_since_last_avg

    try:
        db_model = models.Model(
            client_weights=weights_data.weights
        )

        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        model_count_since_last_avg += 1

        # if model_count_since_last_avg >= 10:
        #     all_weights = fetch_all_weights(db)
        #     averaged_weights = federated_averaging(all_weights)
        #     save_aggregated_model(db, averaged_weights)
        #     model_count_since_last_avg = 0

        return {"message": "Weights accepted"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
