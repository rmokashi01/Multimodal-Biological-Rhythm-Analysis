import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
from utils.data_loader import load_capnobase_subject
from preprocessing.signal_cleaning import butter_bandpass_filter, normalize_signal
from models.correncoder import CorrEncoder

def create_windows(ppg, resp, window_size):
    num_windows = len(ppg) // window_size
    x_wins, y_wins = [], []
    for i in range(num_windows):
        start = i * window_size
        end = start + window_size
        seg_x = ppg[start:end]
        seg_y = resp[start:end]
        if np.std(seg_x) > 1e-4 and np.std(seg_y) > 1e-4:
            x_wins.append(seg_x)
            y_wins.append(seg_y)
    return np.array(x_wins), np.array(y_wins)

def train():
    print("Starting Training Pipeline...")
    data_file = "data/capnobase/0009_8min.mat"
    print(f"Loading data from {data_file}")
    data = load_capnobase_subject(data_file)
    fs = data['fs']
    
    print("Preprocessing signals (Bandpass + Normalize)...")
    clean_ppg = normalize_signal(butter_bandpass_filter(data['ppg'], 0.1, 5.0, fs))
    clean_resp = normalize_signal(butter_bandpass_filter(data['resp'], 0.1, 0.5, fs))
    
    WINDOW_SIZE = 3000
    print(f"Slicing data into {WINDOW_SIZE}-sample windows...")
    x_windows, y_windows = create_windows(clean_ppg, clean_resp, WINDOW_SIZE)
    
    print(f"Generated {len(x_windows)} aligned training windows.")
    
    X_tensor = torch.tensor(x_windows, dtype=torch.float32).unsqueeze(1) 
    Y_tensor = torch.tensor(y_windows, dtype=torch.float32).unsqueeze(1)
    
    print("Initializing Deep CorrEncoder...")
    model = CorrEncoder()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    epochs = 100
    print(f"Starting training for {epochs} epochs...")
    
    for epoch in range(1, epochs + 1):
        optimizer.zero_grad() # Reset gradients
        
        # Forward pass: Try to predict respiration from PPG
        predictions = model(X_tensor)
        
        # Calculate how wrong the predictions were
        loss = criterion(predictions, Y_tensor)
        
        # Backward pass: Learn from the mistakes
        loss.backward()
        optimizer.step()
        
        # Print progress every 10 epochs
        if epoch % 10 == 0:
            print(f"Epoch [{epoch:3d}/{epochs}], Loss: {loss.item():.6f}")
            
    # 6. Save Model
    save_path = "models/resp_model.pth"
    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), save_path)
    print(f"Model saved successfully to '{save_path}'!")

if __name__ == "__main__":
    train()
