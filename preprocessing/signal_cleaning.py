import numpy as np
from scipy.signal import butter, sosfiltfilt

def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    # Step A: Fill any NaNs in raw data with the mean
    data = np.nan_to_num(data, nan=np.nanmean(data))
    
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    
    # 🛠️ FIX: b, a ki jagah 'sos' (Second-Order Sections) format ka use kiya hai stability ke liye
    sos = butter(order, [low, high], btype='band', output='sos')
    
    # 🛠️ FIX: filtfilt ki jagah sosfiltfilt use hoga jo bilkul stable rehta hai
    filtered = sosfiltfilt(sos, data)
    
    # Step C: Final NaN check after filtering
    return np.nan_to_num(filtered)

def normalize_signal(data):
    # Ensure no NaNs or Infs
    data = np.nan_to_num(data)
    std = np.std(data)
    if std < 1e-6: # If signal is flat
        return data - np.mean(data)
    return (data - np.mean(data)) / std