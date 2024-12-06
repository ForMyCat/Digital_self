import pandas as pd

# the txt files are sorted by record time, the earliest one corresponds to test ID 1
# you can also use the .csv files, _0.csv corresponds to test ID 1

openbci_datapath = '/home/hxiong/Desktop/Research/Digital_self/data/OpenBCI_data/2024-10-24-tianwen-11tests/OpenBCISession_2024-10-24_tianwen_11tests/OpenBCI-RAW-2024-10-24_15-22-13.txt'

sample_rate = 125
data_raw = pd.read_csv(openbci_datapath, sep=",", header=6, index_col=False, names=["Sample Index", "ch0", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8", "ch9", "ch10", "ch11", "ch12", "ch13", "ch14", "ch15", "Accel Channel 0", "Accel Channel 1", "Accel Channel 2", "Not Used", "Digital Channel 0 (D11)", "Digital Channel 1 (D12)", "Digital Channel 2 (D13)", "Digital Channel 3 (D17)", "Not Used 2", "Digital Channel 4 (D18)", "Analog Channel 0", "Analog Channel 1", "Analog Channel 2", "Timestamp", "Marker", "Timestamp (Formatted)"])
data_raw.drop(labels = ['Not Used','Not Used 2'], inplace = True, axis = 1)
data_raw.reset_index(inplace=True, drop=True)
print("OpenBCI data shape: ", data_raw.shape)
print(data_raw.columns)
