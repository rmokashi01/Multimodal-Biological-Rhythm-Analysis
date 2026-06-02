from utils.data_loader import load_capnobase_subject

try:
    data = load_capnobase_subject('data/capnobase/0009_8min.mat')
    print("\n--- ACTUAL EXTRACTED VALUES ---")
    print(f"Keys inside dictionary: {list(data.keys())}")
    print(f"Sampling Rate (fs): {data['fs']} Hz")
    
    print("\n[PPG Signal]")
    print(f"- Data Type: {type(data['ppg'])}")
    print(f"- Total Samples (Length): {len(data['ppg'])}")
    print(f"- First 5 values: {data['ppg'][:5]}")
    
    print("\n[Respiration (CO2) Signal]")
    print(f"- Data Type: {type(data['resp'])}")
    print(f"- Total Samples (Length): {len(data['resp'])}")
    print(f"- First 5 values: {data['resp'][:5]}")
    
    print("\n[ECG Signal]")
    print(f"- Data Type: {type(data['ecg'])}")
    print(f"- Total Samples (Length): {len(data['ecg'])}")
    print(f"- First 5 values: {data['ecg'][:5]}")
    print("-------------------------------")
except Exception as e:
    print(f"Error: {e}")
