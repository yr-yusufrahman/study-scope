import joblib, pickle
import io, os, numpy as np
from predictor.models import Predictor, Revision

from django.db.models import F, ExpressionWrapper, FloatField
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# Make a prediction after a quiz
def makePredictionOld(revision_obj, user_obj):
    days_since = revision_obj.days_since
    mistake_score = (revision_obj.mistakes / revision_obj.inputs) * 100
    mistake_score = round(mistake_score, 4)
    inputs = revision_obj.inputs
    course_id = revision_obj.chapter.course.id

    # Prepare the input for the model
    raw_data = np.array([
        [
            course_id,
            days_since,
            mistake_score, 
            inputs,
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


# Before making a prediction, check if the given course ID exists


# Make a prediction by loading the model from the database
def queryModel(predictor_obj, input):
    model_serialized = predictor_obj.tree
    model = pickle.loads(model_serialized)

    # Make prediction
    prediction = model.predict(input)
    return prediction


# One-hot encode the course ID for the given numpy data
def encodeCourse(data):
    # The column of the course id in the input data
    course_id_index = 0

    # One-hot encode the course ID
    one_hot_encoder = OneHotEncoder(categories='auto', sparse_output=False)

    # Create a ColumnTransformer to one-hot encode the course ID while passing other features as-is
    preprocessor = ColumnTransformer(
        transformers=[
            ('course_id', one_hot_encoder, [course_id_index])  # Apply OneHotEncoder to the course ID column
        ],
        remainder='passthrough'  # Leave other columns unchanged
    )

    # Transform the dataset
    transformed_data = preprocessor.fit_transform(data)

    return transformed_data


# Manually encode the course ID for prediction input data
def manualEncoder(data, id_list, given_id):
    course_exists = given_id in id_list
    
    # Template for the one-hot encoded columns
    coded_columns = np.full(shape=(len(data), len(id_list)), fill_value=0)
    if course_exists:
        index = id_list.index(given_id)
        coded_columns[:, index] = 1
    coded_data = np.column_stack((coded_columns, data))

    return coded_data


# Retrain the tree
def retrainTree(revisions, predictor_obj):
    # Format revision data into NumPy array
    revision_array = np.array([
        [revision.chapter.course.id, revision.days_since, round(revision.mistakes/revision.inputs, 4), revision.inputs]
        for revision in revisions
    ])
    
    # Get intervals as they are the labels
    revision_labels = np.array([revision.interval for revision in revisions])

    # Load the default data
    loaded_data = np.load('predictor/helpers/default_data.npz')
    default_x = loaded_data['features']
    default_y = loaded_data['labels']

    # Merge default data with the user revision data
    new_x = np.vstack((default_x, revision_array))
    new_y = np.hstack((default_y, revision_labels))

    

    # One-hot encode the course ID
    coded_x = encodeCourse(new_x)
    print(f"New X: {coded_x}\nNew Y: {new_y}\n")
    # Retrain the model
    model_serialized = predictor_obj.tree
    model = pickle.loads(model_serialized)
    model.fit(coded_x, new_y)

    # Save the model back to the database
    binary_model = pickle.dumps(model)
    predictor_obj.tree = binary_model
    predictor_obj.save()
    return predictor_obj


# Get an interval prediction for a new revision
def makePrediction(revision_obj, user_obj):
    days_since = revision_obj.days_since
    mistake_score = (revision_obj.mistakes / revision_obj.inputs) * 100
    mistake_score = round(mistake_score, 4)
    inputs = revision_obj.inputs
    course_id = revision_obj.chapter.course.id

    # Get the revision data for the user's drop-offs
    revision_query = Revision.objects.filter(
        is_loss=True, 
        interval__gt=0, 
        inputs__gt=0, 
        chapter__course__owner=user_obj
    ).order_by('date')

    # Get the user's predictor model
    predictor = Predictor.objects.get_or_create(user=user_obj)
    model = predictor[0]

    # Check if there was a new drop-off - retrain the model
    if revision_obj.dropOffDetected():
        model = retrainTree(revision_query, model)

    # The first column is the default data course ID, -1
    unique_courses = [-1]
    unique_courses += list(revision_query.values('chapter__course__id').distinct())

    # Prepare the input for the model
    raw_input = np.array([
        [
            #course_id,
            days_since,
            mistake_score, 
            inputs,
        ],
    ])

    # Get the order of the one-hot encoded courses
    coded_input = manualEncoder(raw_input, unique_courses, course_id)

    # Get the prediction from the tree
    prediction = queryModel(model, coded_input)
    days = round(prediction[0])
    print(f"Post-quiz Prediction: {days}\n")
    return days
    


# Get an interval prediction for a new revision
def makePredictionTest(user_obj):

    # Get the revision data for the user's drop-offs
    revision_query = Revision.objects.filter(
        is_loss=True, 
        interval__gt=0, 
        inputs__gt=0, 
        chapter__course__owner=user_obj
    ).order_by('date')

    # Get the user's predictor model
    predictor = Predictor.objects.get_or_create(user=user_obj)
    model = predictor[0]

    # retrain the model
    #model = retrainTree(revision_query, model)

    # The first column is the default data course ID, -1
    unique_courses = [-1]
    unique_courses += list(revision_query.values('chapter__course__id').distinct())

    # Prepare the input for the model
    raw_input = np.array([
        [
            #course_id,
            0,
            0.25, 
            8,
        ],
    ])

    # Get the order of the one-hot encoded courses
    coded_input = manualEncoder(raw_input, unique_courses, 1)

    # Get the prediction from the tree
    prediction = queryModel(model, coded_input)
    days = round(prediction[0])
    print(f"Test Tree Prediction should be 3: {days}\n")
    return days
