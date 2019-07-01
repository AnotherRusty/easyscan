from rplidar import RPLidar
import threading
from time import sleep


class Scanner(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.lidar = RPLidar(port)
        self.lidar.stop_motor()
        sleep(0.5)
        self.lidar.start_motor()
        
        self.setDaemon(True)
        self.scan = [0.0 for i in range(360)]

    def check_device(self):
        info = self.lidar.get_info()
        print(info)
        health = self.lidar.get_health()
        print(health)
        return (info, health)

    def get_scan(self):
        return self.scan
    
    def run(self):
        self.lidar.clear_input()
        while True:
            for meas in self.lidar.iter_measurments():
                new_scan    = meas[0]
                quality     = meas[1]
                angle       = meas[2]
                distance    = meas[3]
                if angle <  360:
                    self.scan[int(angle)] = (angle, distance / 1000.0)
    
