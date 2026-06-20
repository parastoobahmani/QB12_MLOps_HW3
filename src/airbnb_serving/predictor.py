import pandas as pd
from .schema import ListingFeatures, PredictionResponse

def predict_single(features: ListingFeatures, model, run_id: str) -> PredictionResponse:
    x = pd.DataFrame([features.model_dump()])
    print(type(model))
    print(hasattr(model, "predict_proba"))
    pred = model.predict(x)[0]
    prob = model.predict_proba(x)[0, 1]


    return PredictionResponse(
                listing_id= features.listing_id,
                prediction= int(pred),
                probability_high_demand= float(prob),
                model_run_id= str(run_id)  
            )




def predict_batch(features_list: list[ListingFeatures], model, run_id: str) -> list[PredictionResponse]:
    rows = [ feature.model_dump() for feature in features_list]
    x = pd.DataFrame(rows)

    predictions = model.predict(x)
    probabilities = model.predict_proba(x)[:, 1]

    responses = []

    for feature, pred, prob in zip(features_list, predictions, probabilities):
        responses.append(
            PredictionResponse(
                listing_id= feature.listing_id,
                prediction= int(pred),
                probability_high_demand= float(prob),
                model_run_id= str(run_id)  
            )
        )

    return responses
