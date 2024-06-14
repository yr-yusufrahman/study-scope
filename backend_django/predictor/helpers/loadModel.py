import joblib
import io, os, numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


# Get the parameters of the default model
def defaultModelParams():
    # Find the path to the model file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    file_path = os.path.join(parent_directory, 'helpers\default_model.npz')

    # Load the parameters from the file
    data = np.load(file_path)
    coef = data['coef'].tolist()
    intercept = data['intercept'].tolist()

    print(f"Coef type: {type(coef)}\nIntercept type: {type(intercept)}\n")

    # Package the parameters into a dictionary
    params = {
        'coef': coef,
        'intercept': intercept
    }

    return params


# Make a prediction by building a model from the parameters
def queryModel(params, input):
    # Standardize the new data
    scaler = StandardScaler()
    scaled_input = scaler.fit_transform(input)

    # Create a Linear Regression model
    model = LinearRegression()
    model.coef_ = np.array(params['coef'])
    model.intercept_ = np.array(params['intercept'])

    # Make prediction
    prediction = model.predict(scaled_input)

    return prediction

