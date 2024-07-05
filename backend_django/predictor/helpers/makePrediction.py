import joblib, pickle
import io, os, numpy as np
from predictor.models import Predictor


# Make a prediction after a quiz
def makePrediction(revision_obj, user_obj):
    days_since = revision_obj.days_since
    mistake_score = (revision_obj.mistakes / revision_obj.inputs) * 100
    mistake_score = round(mistake_score, 4)
    inputs = revision_obj.inputs
    #percentage_of_reveals = revision_obj.percentage_of_reveals

    # Prepare the input for the model
    raw_data = np.array([
        [
            days_since,
            mistake_score, 
            inputs, 
            #percentage_of_reveals
        ],
    ])
    
    # Get the course model parameters
    predictor = Predictor.objects.get_or_create(user=user_obj)
    model = predictor[0]

    # Make a prediction
    prediction = queryModel(model, raw_data)
    days = round(prediction[0])
    print(f"Post-quiz Prediction: {days}\n")
    return days


# Make a prediction by loading the model from the database
def queryModel(predictor_obj, input):
    model_serialized = predictor_obj.tree
    model = pickle.loads(model_serialized)

    # Make prediction
    prediction = model.predict(input)
    return prediction




