import joblib, pickle
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



# Default User tree - 3 features is sufficient - maybe 1-hot encode course for the tree
def defaultTree():
    # Find the path to the model file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    file_path = os.path.join(parent_directory, 'helpers\default_tree.joblib')

    # Load model from file into memory with joblib and serialize it with pickle for storing in DB
    model = joblib.load(file_path)
    model_serialized = pickle.dumps(model)

    return model_serialized

# Write a function that will take raw quiz data and package into numpy to make prediction on the tree
# def prepareQuizData(raw_data):
