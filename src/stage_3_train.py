import argparse
import os
import shutil
from tqdm import tqdm
import logging
import joblib
import numpy as np
from utils.common import read_yaml, create_directories
from sklearn.ensemble import RandomForestClassifier


logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )

STAGE = "Training"

def main(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    artifacts = config["artifacts"]
    featurized_data_dir_path = os.path.join(artifacts["ARTIFACTS_DIR"],artifacts["FEATURIZED_DATA"])

    featurized_train_data_path = os.path.join(featurized_data_dir_path, artifacts["FEATURIZED_OUT_TRAIN"])

# Create a directory to store the model 

    model_dir_path = artifacts["MODEL_DIR"]
    create_directories([model_dir_path])
    model_path = os.path.join(model_dir_path, artifacts["MODEL_NAME"])

# Loading the train.pkl file

    matrix = joblib.load(featurized_train_data_path)

    labels = np.squeeze(matrix[:, 1].toarray())
    X = matrix[:, 2:]

    logging.info(f"Input matrix shape : {matrix.shape}")
    logging.info(f"X matrix shape : {X.shape}")
    logging.info(f"labels matrix shape : {labels.shape}")


    seed = params["train"]["seed"]
    n_est = params["train"]["n_est"]
    min_split= params["train"]["min_split"]

# Import & Train the Model Classifier -  Random Forest 

    rf_model = RandomForestClassifier(n_estimators=n_est, min_samples_split=min_split, random_state= seed, n_jobs=2)

    rf_model.fit(X, labels)

# Saving the trained model in specified path

    joblib.dump(rf_model, model_path)
    

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config, params_path = parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed! <<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e