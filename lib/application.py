#coding=utf-8

from tkinter import *
from tkinter import filedialog
from .scanner import Scanner
import threading
from time import sleep, time
from math import pi, cos, sin
import sdxf


WINDOW_W = 600
WINDOW_H = 600

# display params
DISPLAY_W = 600
DISPLAY_H = 400
FPS = 10

# scan params
SCAN_LEN = 360
RESOLUTION = 0.05
SCALE_MIN = 1.0
SCALE_MAX = 3.0

class Application:
    def __init__(self, master=Tk()):
        self.root = master
        self.root.title("EasyScan")
        self.root.geometry('%dx%d' %(WINDOW_W, WINDOW_H))
        self.root.resizable(0,0)

        # variables
        self.port = StringVar()
        self.port.set('COM3')
        self.ignore_min = IntVar()
        self.ignore_min.set(0)
        self.ignore_max = IntVar()
        self.ignore_max.set(0)
        self.scale = DoubleVar()
        self.scale.set(1.0)
        self.connect_button_text = StringVar()
        self.connect_button_text.set('连接')
        self.start_button_text = StringVar()
        self.start_button_text.set('开始扫描')
        self.export_button_text = StringVar()
        self.export_button_text.set('保存文件')
        self.status = StringVar()
        self.status.set('欢迎使用openarm EasyScan！')
        
        self.connect_flag = False
        self.start_flag = False

        # objects
        self.scanner = None

        # threads
        self.display_thread = threading.Thread(name='display', target=self.display_func)
        self.display_thread.setDaemon(True)

        self.init_gui()
    
    def init_gui(self):
    # settings
        self.setting_container = Frame(self.root)
        # 设备端口
        Label(self.setting_container, text='设备端口：').grid(row=0, column=0, sticky=W)
        Entry(self.setting_container, textvariable=self.port).grid(row=0, column=1, sticky=W+E)
        # 忽略范围
        Label(self.setting_container, text='忽略范围(度)：').grid(row=1, column=0, sticky=W)
        Entry(self.setting_container, textvariable=self.ignore_min, width=8).grid(row=1, column=1, sticky=W)
        Label(self.setting_container, text=' 至 ').grid(row=1, column=1)
        Entry(self.setting_container, textvariable=self.ignore_max, width=8).grid(row=1, column=1, sticky=E)
        # 扫描距离
        Label(self.setting_container, text='显示比例：').grid(row=2, column=0, sticky=W)
        Scale(self.setting_container, variable=self.scale, orient=HORIZONTAL, from_=SCALE_MIN, to=SCALE_MAX, resolution=0.01).grid(row=2, column=1, columnspan=2, sticky=W+E)
        # Buttons
        Button(self.setting_container, textvariable=self.connect_button_text, width=15, height=2, command=self.connect_reg).grid(row=0, column=2, rowspan=2, sticky=E+S)
        Button(self.setting_container, textvariable=self.start_button_text, width=15, height=2, command=self.start_reg).grid(row=5, column=1, pady=10, sticky=E)
        Button(self.setting_container, textvariable=self.export_button_text, width=15, height=2, command=self.export_reg).grid(row=5, column=2, pady=10, sticky=E)

        self.setting_container.grid(pady=10)

    # display
        self.display_container = Frame(self.root)
        # 画布
        self.canvas = Canvas(self.display_container, width=600, height=400, bg='WHITE')
        self.canvas.pack()

        self.display_container.grid()
    
    # status
        self.status_container = Frame(self.root)
        Label(self.status_container, textvariable=self.status).grid()

        self.status_container.grid()

    def launch(self):
        self.root.mainloop()
    
    def connect_reg(self):
        if not self.connect_flag:
            try:
                self.scanner = Scanner(self.port.get())
            except:
                self.scanner = None
                self.show_status('连接失败,请检查端口号')
                return

            self.show_status('正在连接...')
            sleep(0.5)
            self.show_status('检查设备状态...')
            sleep(1.0)
            try:
                info, health = self.scanner.check_device()
                if 'Good' in health[0]:
                    self.show_status('设备正常，请点击开始扫描')
                    self.connect_flag = True
                    self.connect_button_text.set('已连接')
                    return
            except:
                pass
            self.show_status('连接失败，请重新连接')
        else:
            self.connect_flag = False
            self.connect_button_text.set('连接')

    def start_reg(self):
        if not self.start_flag:
            if not self.connect_flag:
                self.show_status('错误：设备未连接')
                return
            self.start_flag = True
            self.start_button_text.set('停止')
            self.scanner.start()
            self.display_thread.start()
            self.show_status('正在扫描 ...')
        else:
            self.start_flag = False
            self.start_button_text.set('开始扫描')
    
    def export_reg(self):
        filename = filedialog.asksaveasfilename()
        if not filename:
            return
        self.show_status('生在生成dxf文件...')
        dxf = sdxf.Drawing()
        dxf.append(sdxf.LineList(points=self.process_scan_for_cad(), closed=1, layer='drawinglayer'))
        self.show_status('保存中...')
        if '.dxf' not in filename:
            filename += '.dxf'
        dxf.saveas(filename)
        self.show_status('已保存至'+filename)

    def display_func(self):
        center_x = int(DISPLAY_W / 2)
        center_y = int(DISPLAY_H / 2)

        img = PhotoImage(width=DISPLAY_W, height=DISPLAY_H)
        self.canvas.create_image(center_x, center_y, image=img, state='normal')

        interval = 1.0/FPS
        last = time()
        while self.start_flag:
            if time()-last > interval:
                scan = self.scanner.get_scan()
                if len(scan) != SCAN_LEN:
                    self.show_status('扫描数据异常')
                    break
                color_mat = self.calc_color_mat(scan)
                img.put(''.join("{" + (" ".join(str(color) for color in row)) + "} " for row in color_mat), (0, 0))
                last = time()

    def calc_color_mat(self, scan):
        mat = [["#000000" for x in range(0, DISPLAY_W)] for y in range(DISPLAY_H)]
        for i in range(SCAN_LEN):
            if scan[i] == 0.0:
                continue
            d = scan[i]
            th = (360-i) / 180.0 * pi
            x = d * cos(th)
            y = d * sin(th)
            resolution = RESOLUTION / self.scale.get()
            posx = int(DISPLAY_W/2.0 + (x / resolution))
            posy = int(DISPLAY_H/2.0 - (y / resolution))
            if posx >= 0 and posx < DISPLAY_W and posy >= 0 and posy < DISPLAY_H:
                mat[posy][posx] = '#ffff00'
        return mat
    
    def process_scan_for_cad(self):
        scan_list = []
        cad_scan = [0.0 for i in range(SCAN_LEN)]
        num_scan = 20
        for i in range(num_scan):
            scan_list.append(self.scanner.get_scan())
        for i in range(SCAN_LEN):
            d = 0.0
            n = 0
            for scan in scan_list:
                if scan[i] == 0.0:
                    continue
                d += scan[i]
                n += 1
            if n > 0:
                cad_scan[i] = d / n
        # transform to x,y coordinate
        cad_points = []
        for i in range(SCAN_LEN):
            if cad_scan[i] == 0.0:
                continue
            d = cad_scan[i]
            th = (360-i) / 180 * pi
            x = d * 1000 * cos(th)
            y = d * 1000 * sin(th)
            cad_points.append((x,y))
        return cad_points

    def show_status(self, ss):
        self.status.set(ss)
        self.root.update()

if __name__ == "__main__":
    app = Application()
    app.launch()

