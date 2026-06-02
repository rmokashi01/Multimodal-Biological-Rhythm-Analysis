import torch
import torch.nn as nn

class CorrEncoder(nn.Module):
    def __init__(self):
        super(CorrEncoder, self).__init__()
        
        # ⬇️ ENCODER: Data ko compress karega taaki heartbeat (high-freq) remove ho jaye
        self.encoder = nn.Sequential(
            # Layer 1: Bada kernel (31) taaki long-term trend pakde
            nn.Conv1d(in_channels=1, out_channels=16, kernel_size=31, padding=15),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),  # Length half ho jayegi
            
            # Layer 2
            nn.Conv1d(16, 32, kernel_size=15, padding=7),
            nn.ReLU(),
            nn.MaxPool1d(2),  # Length 1/4th ho jayegi
            
            # Layer 3: Bottleneck (Yahan saans ka pattern extract hoga)
            nn.Conv1d(32, 64, kernel_size=7, padding=3),
            nn.ReLU(),
            nn.MaxPool1d(2)   # Length 1/8th ho jayegi
        )
        
        # ⬆️ DECODER: Compressed breathing pattern ko wapas original size mein layega
        self.decoder = nn.Sequential(
            nn.ConvTranspose1d(in_channels=64, out_channels=32, kernel_size=2, stride=2),
            nn.ReLU(),
            
            nn.ConvTranspose1d(32, 16, kernel_size=2, stride=2),
            nn.ReLU(),
            
            # Final output layer (No ReLU here, taaki negative values bhi aa sakein)
            nn.ConvTranspose1d(16, 1, kernel_size=2, stride=2)
        )

    def forward(self, x):
        # x -> Encoder -> Decoder -> Reconstructed Breathing Wave
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded