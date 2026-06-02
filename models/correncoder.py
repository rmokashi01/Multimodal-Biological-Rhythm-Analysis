import torch
import torch.nn as nn


class CorrEncoder(nn.Module):
    def __init__(self):
        super(CorrEncoder, self).__init__()

        # Encoder:
        # Compresses the input PPG signal and extracts
        # low-frequency respiratory information while
        # reducing high-frequency cardiac components.
        self.encoder = nn.Sequential(

            # Layer 1:
            # Large kernel size captures long-term trends
            # present in the signal.
            nn.Conv1d(
                in_channels=1,
                out_channels=16,
                kernel_size=31,
                padding=15
            ),
            nn.ReLU(),

            # Downsample by a factor of 2
            nn.MaxPool1d(kernel_size=2),

            # Layer 2:
            # Learns higher-level temporal features.
            nn.Conv1d(
                in_channels=16,
                out_channels=32,
                kernel_size=15,
                padding=7
            ),
            nn.ReLU(),

            # Further downsampling
            nn.MaxPool1d(kernel_size=2),

            # Layer 3 (Bottleneck):
            # Encodes the most important respiratory patterns.
            nn.Conv1d(
                in_channels=32,
                out_channels=64,
                kernel_size=7,
                padding=3
            ),
            nn.ReLU(),

            # Final compression stage
            nn.MaxPool1d(kernel_size=2)
        )

        # Decoder:
        # Reconstructs the respiration waveform from the
        # compressed latent representation.
        self.decoder = nn.Sequential(

            # Upsample by a factor of 2
            nn.ConvTranspose1d(
                in_channels=64,
                out_channels=32,
                kernel_size=2,
                stride=2
            ),
            nn.ReLU(),

            # Upsample by another factor of 2
            nn.ConvTranspose1d(
                in_channels=32,
                out_channels=16,
                kernel_size=2,
                stride=2
            ),
            nn.ReLU(),

            # Final reconstruction layer
            # No activation function is used so that the
            # output can contain both positive and negative values.
            nn.ConvTranspose1d(
                in_channels=16,
                out_channels=1,
                kernel_size=2,
                stride=2
            )
        )

    def forward(self, x):
        """
        Forward pass:
        Input Signal -> Encoder -> Latent Representation
                     -> Decoder -> Reconstructed Respiration Signal
        """
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)

        return decoded
