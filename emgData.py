#imports
import myo
import pandas as pd
import time
import matplotlib.pyplot as plt

class Listener(myo.DeviceListener):
    def __init__(self):
        self.emg_data = []
        self.should_stop = False
    
    #confirms connection
    def on_connected(self, event):
        print("Connected.")
        event.device.vibrate(myo.VibrationType.medium)

    #turns off program when double tap
    def on_pose(self, event):
        print(f"Detected pose: {event.pose}")
        if event.pose == myo.Pose.wave_out:
            self.should_stop = True
            print("Waved out. Program should stop.")
    
    #adds emg data
    def on_emg(self, myo, timestamp, emg):
        self.emg_data.append(emg)
        print(f"Getting EMG data: {emg}")

def plot(emg_df):
    #plot and save emg data
    plt.figure(figsize=(12,6))

    for i in range(emg_df.shape[1]):
        plt.plot(emg_df.index, emg_df[i])

    plt.title('EMG data')
    plt.xlabel('Index')
    plt.ylabel('EMG Value')
    plt.savefig('emg_dataplt.png')
    plt.show()

def main():
    #initialized myo armband
    myo.init()
    hub = myo.Hub()
    listener = Listener()

    #listens for emg data on pose
    while not listener.should_stop:
        hub.run(listener.on_event, duration_ms=200)
    
    print("Program has stopped recording EMG data.")
    hub.stop()
    
    #save the emg data to csv file
    emg_df = pd.DataFrame(listener.emg_data)
    emg_df.to_csv('emg_data.csv', index=False)
    print("Data saved.")

    plot(emg_df)

if __name__ == "__main__":
    main()

