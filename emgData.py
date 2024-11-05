#imports
import myo
import pandas as pd
import time
import matplotlib.pyplot as plt

class Listener(myo.DeviceListener):
    def __init__(self):
        self.emg_data = []
        self.timestamps = []
    
    #confirms connection
    def on_connected(self, event):
        print("Connected.")
        event.device.stream_emg(myo.StreamEmg.enabled)
        event.device.vibrate(myo.VibrationType.medium)

    #adds emg data
    def on_emg(self, event):
        self.emg_data.append(event.emg)
        self.timestamps.append(event.timestamp)

def plot(emg_df):
    #plot and save emg data
    plt.figure(figsize=(12,6))

    for i in range(emg_df.shape[1] - 1):
        plt.plot(emg_df['Time'], emg_df[f'channel_{i+1}'], label=f'Channel {i+1}')

    plt.title('EMG data')
    plt.xlabel('Time (ms)')
    plt.ylabel('EMG Value')
    plt.savefig('emg_dataplt.png')
    plt.show()

def main():
    #initialized myo armband
    myo.init()
    hub = myo.Hub()
    listener = Listener()

    #records emg data for 2 seconds
    print("Programs has started recording EMG data")
    hub.run(listener.on_event, duration_ms=2000)
    hub.stop()
    print("Program has stopped recording EMG data")

    start_time = listener.timestamps[0] if listener.timestamps else 0
    time_in_ms = [(ts - start_time) * 1e-3 for ts in listener.timestamps]
    
    #save the emg data to csv file
    emg_df = pd.DataFrame(listener.emg_data, columns=[f'channel_{i+1}' for i in range(8)])
    emg_df['Time'] = time_in_ms
    emg_df.to_csv('emg_data.csv', index=False)
    print("Data saved.")

    plot(emg_df)

if __name__ == "__main__":
    main()

