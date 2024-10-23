#imports
from __future__ import print_function
import myo

class Listener(myo.DeviceListener):

    def on_connected(self, event):
        print("Hello, '{}'!")
        event.device.vibrate(myo.VibrationType.short)
        event.device.request_battery_level()

    def on_battery_level(self, event):
        print("battery level:", event.battery_level)
    
    def on_pose(self, event):
        if event.pose == myo.Pose.double_tap:
            return False


if __name__ == '__main__':
    myo.init()
    hub = myo.Hub()
    listener = Listener()
    while hub.run(listener.on_event, 500):
        pass
    print('Bye!')


