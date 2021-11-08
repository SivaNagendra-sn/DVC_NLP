import argparse
import os
import shutil
from tqdm import tqdm
import logging
from utils.common import read_yaml

STAGE = "Data Preparation"

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )

def prep_data(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    print("red the data")

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        prep_data(config_path=parsed_args.config, params_path = parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed! <<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e