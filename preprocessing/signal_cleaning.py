import numpy as np
from scipy.signal import butter, sosfiltfilt


def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    """
    Apply a Butterworth bandpass filter to the input signal.

    Parameters:
        data (numpy.ndarray): Input signal.
        lowcut (float): Lower cutoff frequency in Hz.
        highcut (float): Upper cutoff frequency in Hz.
        fs (float): Sampling frequency in Hz.
        order (int): Filter order.

    Returns:
        numpy.ndarray: Filtered signal.
    """

    # Replace any NaN values with the mean of the signal
    data = np.nan_to_num(data, nan=np.nanmean(data))

    # Compute normalized cutoff frequencies
    nyquist_frequency = 0.5 * fs
    low = lowcut / nyquist_frequency
    high = highcut / nyquist_frequency

    # Create a Butterworth bandpass filter using
    # Second-Order Sections (SOS) for improved numerical stability
    sos = butter(
        order,
        [low, high],
        btype="band",
        output="sos"
    )

    # Apply zero-phase filtering to avoid phase distortion
    filtered_signal = sosfiltfilt(sos, data)

    # Replace any remaining NaN or infinite values
    return np.nan_to_num(filtered_signal)


def normalize_signal(data):
    """
    Normalize a signal to zero mean and unit variance.

    Parameters:
        data (numpy.ndarray): Input signal.

    Returns:
        numpy.ndarray: Normalized signal.
    """

    # Replace NaN and infinite values with finite numbers
    data = np.nan_to_num(data)

    signal_mean = np.mean(data)
    signal_std = np.std(data)

    # Handle nearly constant signals to avoid division by zero
    if signal_std < 1e-6:
        return data - signal_mean

    # Standard score normalization (Z-score)
    return (data - signal_mean) / signal_std
