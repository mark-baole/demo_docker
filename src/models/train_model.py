"""
This file trains a support vector classifier on the iris dataset and saves the model as a pickle file.

It uses the following libraries and modules:
- pandas: for data manipulation and analysis
- sklearn.svm: for support vector machine algorithms
- pickle: for serializing and deserializing Python objects
"""

# Import libraries and modules
import pandas as pd
from sklearn.svm import SVC
import pickle
import logging

# Define constants
INPUT_FILE = './data/processed/iris_processed.csv'
OUTPUT_FILE = './models/iris_model.pkl'
MODEL_NAME = 'iris_model'

# Define main function
def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(f'Starting {MODEL_NAME} training')

    # Load and prepare data
    logging.info(f'Loading data from {INPUT_FILE}')
    iris = pd.read_csv(INPUT_FILE)
    X = iris.drop(columns='variety')
    y = iris['variety']

    # Train model
    logging.info(f'Training support vector classifier')
    clf = SVC(probability=True)
    clf.fit(X, y)

    # Save model
    logging.info(f'Saving model to {OUTPUT_FILE}')
    try:
        with open(OUTPUT_FILE, 'wb') as f:
            pickle.dump(clf, f)
        logging.info(f'Model saved successfully')
    except Exception as e:
        logging.error(f'An error occurred while saving the model: {e}')

    logging.info(f'Finished {MODEL_NAME} training')

if __name__ == '__main__':
    main()