from rplidar import RPLidar
import random

class Lidar:
    def __init__(self, port):
        pass

    def get_scan(self):
        # scan = [random.randint(50, 12000)/1000 for i in range(360)]
        scan = [200 for i in range(360)]
        return scan
    
    def run(self):
        pass
    
