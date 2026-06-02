import torch
import numpy as np
from utils.data_loader import load_capnobase_subject
from preprocessing.signal_cleaning import butter_bandpass_filter, normalize_signal
from models.correncoder import CorrEncoder
from utils.visualization import plot_reconstruction

def main():
    # 1. Load an UNSEEN subject (Subject 0009 for diagnostic testing)
    test_subject = "data/capnobase/0009_8min.mat"
    print(f"🧪 Testing on subject: {test_subject}")
    
    data = load_capnobase_subject(test_subject)
    fs = data['fs']
    
    # 2. Preprocess Signals
    clean_ppg = normalize_signal(butter_bandpass_filter(data['ppg'], 0.1, 5.0, fs))
    clean_resp = normalize_signal(butter_bandpass_filter(data['resp'], 0.1, 0.5, fs))
    
    # 🔍 FULL FILE DATA CHECK (Terminal pe details dekhne ke liye)
    print("\n--- 🔍 FULL FILE DATA CHECK ---")
    print(f"Raw Resp (From MAT) -> Min: {np.min(data['resp']):.4f}, Max: {np.max(data['resp']):.4f}")
    print(f"Clean Resp (Filtered) -> Min: {np.min(clean_resp):.4f}, Max: {np.max(clean_resp):.4f}")
    
    # 🚨 AUTOMATIC WINDOW FINDER: Jahan respiration zero nahi hai, wahan ki window khud select hogi
    non_zero_indices = np.where(np.abs(clean_resp) > 0.01)[0]
    if len(non_zero_indices) > 0:
        # Pehle active segment se 5000 samples aage jao taaki signal completely stable mile
        start = non_zero_indices[0] + 5000  
        end = start + 3000  # Updated to 3000 samples (10 seconds) for deep bottleneck architecture
        print(f"✅ Found valid signal window automatically! Slicing from: {start} to {end}")
    else:
        start, end = 60000, 61000
        print("❌ Warning: Entire respiration signal seems to be zero across the file!")

    test_x = clean_ppg[start:end]
    test_y = clean_resp[start:end]

    print(f"Test X (PPG) Mean: {np.mean(test_x):.4f}, Max: {np.max(test_x):.4f}")
    print(f"Test Y (Resp) Mean: {np.mean(test_y):.4f}, Max: {np.max(test_y):.4f}\n")
    
    # 3. Load the Trained Model
    model = CorrEncoder()
    model.load_state_dict(torch.load("models/resp_model.pth"))
    model.eval()
    
    # 4. Predict Respiration from PPG
    with torch.no_grad():
        input_tensor = torch.tensor(test_x, dtype=torch.float32).view(1, 1, -1)
        prediction = model(input_tensor).squeeze().numpy()
    
    # 5. Visualize Results
    print("📊 Generating reconstruction plot...")
    plot_reconstruction(test_y, prediction, fs, title=f"Reconstruction Test: {test_subject}")

if __name__ == "__main__":
    main()