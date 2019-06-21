#!/usr/bin/env python

from lib import Display
from lib import Lidar

lidar = Lidar("")
display = Display()


if __name__ == "__main__":
    while True:
        scan = lidar.get_scan()
        display.draw(scan)    