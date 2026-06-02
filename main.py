import torch
import numpy as np

from utils.data_loader import load_capnobase_subject
from preprocessing.signal_cleaning import butter_bandpass_filter, normalize_signal
from models.correncoder import CorrEncoder
from utils.visualization import plot_reconstruction


def main():
    # Load an unseen subject for model evaluation
    test_subject = "data/capnobase/0009_8min.mat"
    print(f"Testing on subject: {test_subject}")

    data = load_capnobase_subject(test_subject)
    fs = data['fs']

    # Preprocess PPG and respiration signals
    clean_ppg = normalize_signal(
        butter_bandpass_filter(data['ppg'], 0.1, 5.0, fs)
    )

    clean_resp = normalize_signal(
        butter_bandpass_filter(data['resp'], 0.1, 0.5, fs)
    )

    # Display statistics of the original and filtered respiration signal
    print("\n--- FULL FILE DATA CHECK ---")
    print(
        f"Raw Respiration Signal -> "
        f"Min: {np.min(data['resp']):.4f}, "
        f"Max: {np.max(data['resp']):.4f}"
    )

    print(
        f"Filtered Respiration Signal -> "
        f"Min: {np.min(clean_resp):.4f}, "
        f"Max: {np.max(clean_resp):.4f}"
    )

    # Automatically find a valid signal region where respiration is active
    non_zero_indices = np.where(np.abs(clean_resp) > 0.01)[0]

    if len(non_zero_indices) > 0:
        # Move forward from the first active sample to avoid unstable regions
        start = non_zero_indices[0] + 5000

        # Extract a 3000-sample window (~10 seconds at 300 Hz)
        end = start + 3000

        print(
            f"Valid respiration segment found. "
            f"Using samples from {start} to {end}"
        )
    else:
        # Fallback window if no valid respiration activity is detected
        start, end = 60000, 61000
        print(
            "Warning: No significant respiration activity "
            "detected in the entire recording."
        )

    # Extract test window
    test_x = clean_ppg[start:end]
    test_y = clean_resp[start:end]

    # Display basic statistics of the selected window
    print(
        f"PPG Segment -> "
        f"Mean: {np.mean(test_x):.4f}, "
        f"Max: {np.max(test_x):.4f}"
    )

    print(
        f"Respiration Segment -> "
        f"Mean: {np.mean(test_y):.4f}, "
        f"Max: {np.max(test_y):.4f}\n"
    )

    # Load the trained CorrEncoder model
    model = CorrEncoder()
    model.load_state_dict(torch.load("models/resp_model.pth"))
    model.eval()

    # Generate respiration prediction from PPG
    with torch.no_grad():
        input_tensor = torch.tensor(
            test_x,
            dtype=torch.float32
        ).view(1, 1, -1)

        prediction = model(input_tensor).squeeze().numpy()

    # Visualize ground truth and reconstructed respiration signals
    print("Generating reconstruction plot...")

    plot_reconstruction(
        test_y,
        prediction,
        fs,
        title=f"Reconstruction Test: {test_subject}"
    )


if __name__ == "__main__":
    main()
