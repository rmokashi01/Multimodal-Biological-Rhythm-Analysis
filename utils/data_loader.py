import os
import h5py
import numpy as np

def load_capnobase_subject(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    mat_data = h5py.File(file_path, 'r')
    
    extracted_data = {
        "ppg": np.array(mat_data['signal']['pleth']['y']).flatten(),
        "resp": np.array(mat_data['signal']['co2']['y']).flatten(),
        "ecg": np.array(mat_data['signal']['ecg']['y']).flatten(),
        "fs": 300
    }
    
    return extracted_data