import os 
import logging
import pandas as pd
from scipy.sparse import csr_matrix, hstack
import joblib
import numpy as np

def save_matrix(df, matrix, out_path):
    id_matrix = csr_matrix(df.id.astype(np.int64)).T
    label_matrix = csr_matrix(df.label.astype(np.int64)).T

    result = hstack([id_matrix, label_matrix, matrix], format='csr')

    msg = f"The output matrix {out_path} of size {result.shape} and datatype {result.dtype}"
    logging.info(msg)

    joblib.dump(result, out_path)