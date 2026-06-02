import torch
import torch.nn as nn
import torch.optim as optim
import os

def train_model(model, ppg_data, resp_data, epochs=100, lr=0.0001):
    x = torch.tensor(ppg_data, dtype=torch.float32).view(1, 1, -1)
    y = torch.tensor(resp_data, dtype=torch.float32).view(1, 1, -1)
    
    criterion = nn.MSELoss() 
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    print(f"🎬 Starting training for {epochs} epochs...")
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        
        pred_resp = model(x)
        loss = criterion(pred_resp, y)
        
        if torch.isnan(loss):
            print(f"❌ Error: Loss became NaN at epoch {epoch+1}")
            break
            
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.6f}")
            
    torch.save(model.state_dict(), "models/resp_model.pth")
    print("💾 Model saved successfully.")