#imports
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_icm20x
import board
import busio
import digitalio
import spidev
import numpy as np
import scipy.io as sio

#setup for MCP3008
spi = spidev.SpiDev()
SPI_PORT = 0
SPI_DEVICE = 0
spi = spidev.SpiDev()
spi.open(SPI_PORT, SPI_DEVICE)
spi.mode = 0
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(busio.SPI(board.SCK, board.MOSI, board.MISO), cs)

#setup for lsm9ds1
i2c = board.I2C()
sensor = adafruit_icm20x.ICM20948(i2c)

#data arrays
emg_data = []
accel_data = []
gyro_data = []

def read_emg(channel=0):
    #read emg
    emg_values = []
    for i in range(8):
        channel = AnalogIn(mcp, getattr(MCP, f"P{i}"))
        emg_values.append(channel.value)
    return emg_values

def read_imu():
    #read accelerometer and gyroscope
    accel_x, accel_y, accell_z = sensor.acceleration
    gyro_x, gyro_y, gyro_z = sensor.gyro

    return (accel_x, accel_y, accell_z, gyro_x, gyro_y, gyro_z)

def saveMAT(emg_data, accel_data, gyro_data, filename, gesture, gestureID):
    #format data
    data_dict = {
        'filename': np.array([filename], dtype='<U17'),
        'gesture': np.array([gesture], dtype='<U10'),
        'gesture_id': np.array([[gestureID]], dtype=int),
        'emg': np.array(emg_data, dtype='<U3'),
        'accel': np.array(accel_data, dtype='<U3'),
        'gyro': np.array(gyro_data, dtype='<U3'),
        'sample': np.array([[len(emg_data)]], dtype=int)
    }

    sio.savemat(filename, data_dict)
    print(f"Data saved to {filename}")

def main():
    sample_rate = 100

    #data collection
    for i in range(sample_rate):
        #read emg data
        emg_value = read_emg()
        emg_data.append([str(emg_value)])

        #read IMU data
        imu_values = read_imu()
        accel_data.append([str(imu_values[0]), str(imu_values[1]), str(imu_values[2])])
        gyro_data.append([str(imu_values[3]), str(imu_values[4]), str(imu_values[5])])

        print(f"EMG Value: {emg_value}")
        print(f"Accelerometer: {imu_values[:3]}")
        print(f"Gyroscope: {imu_values[3:6]}")

    #save all data into mat file
    print("Data collection ended.")
    saveMAT(emg_data, accel_data, gyro_data, 'Gesture01.mat', 'tip grasp', 1)


if __name__ == '__main__':
    main()
                               


