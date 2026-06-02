import matplotlib.pyplot as plt
import torch
import numpy as np

def plot_reconstruction(true_resp, pred_resp, fs, title="Respiration Reconstruction"):
    plt.figure(figsize=(12, 6))
    
    # Create time axis in seconds
    time = np.linspace(0, len(true_resp) / fs, len(true_resp))
    
    plt.plot(time, true_resp, label='True Respiration (CO2)', color='blue', alpha=0.6)
    plt.plot(time, pred_resp, label='Predicted Respiration (AI)', color='red', linestyle='--')
    
    plt.title(title)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Normalized Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()