#coding=utf-8

from tkinter import *


WINDOW_W = 600
WINDOW_H = 800

SCAN_RANGE_MIN = 1.0
SCAN_RANGE_MAX = 10.0


class Application:
    def __init__(self, master=Tk()):
        self.root = master
        self.root.title("EasyScan")
        self.root.geometry('%dx%d' %(WINDOW_W, WINDOW_H))

        # variables
        self.port = StringVar()
        self.port.set('/dev/ttyUSB0')
        self.ignore_min = IntVar()
        self.ignore_min.set(150)
        self.ignore_max = IntVar()
        self.ignore_max.set(210)
        self.scan_range = DoubleVar()
        self.scan_range.set(5.0)
        self.start_button_text = StringVar()
        self.start_button_text.set('开始扫描')
        self.export_button_text = StringVar()
        self.export_button_text.set('保存文件')

        self.start_flag = False

        self.init_gui()
    
    def init_gui(self):
    # settings
        self.setting_container = Frame(self.root)
        # 设备端口
        Label(self.setting_container, text='设备端口：', font=('Arial', 12)).grid(row=0, column=0, pady=10, sticky=W)
        Entry(self.setting_container, textvariable=self.port, font=('Arial', 10)).grid(row=0, column=1)
        # 忽略范围
        Label(self.setting_container, text='忽略范围(度)：', font=('Arial', 12)).grid(row=1, column=0, sticky=W)
        Entry(self.setting_container, textvariable=self.ignore_min, font=('Arial', 10)).grid(row=1, column=1)
        Label(self.setting_container, text=' 至 ', font=('Arial', 10)).grid(row=1, column=2)
        Entry(self.setting_container, textvariable=self.ignore_max, font=('Arial', 10)).grid(row=1, column=3)
        # 扫描距离
        Label(self.setting_container, text='扫描距离(m)：', font=('Arial', 12)).grid(row=4, column=0, pady=10, sticky=W)
        Scale(self.setting_container, variable=self.scan_range, orient=HORIZONTAL, length=400, from_=SCAN_RANGE_MIN, to=SCAN_RANGE_MAX, resolution=0.01).grid(row=4, column=1, columnspan=3)
        # Buttons
        Button(self.setting_container, textvariable=self.start_button_text, width=15, height=2, command=self.start_reg).grid(row=5, column=2, pady=20, sticky=E)
        Button(self.setting_container, textvariable=self.export_button_text, width=15, height=2, command=self.export_reg).grid(row=5, column=3, pady=20, sticky=E)

        self.setting_container.grid(row=0, column=0, rowspan=6, columnspan=4, padx=10, pady=10, sticky=W+E+N+S)

    # display
        self.display_container = Frame(self.root)
        # 画布
        self.canvas = Canvas(self.display_container, width=500, height=500, bg='BLACK')
        self.canvas.pack()

        self.display_container.grid(row=6, column=0, rowspan=4, columnspan=4, padx=50, pady=20, sticky=W+E+N+S)

    def launch(self):
        self.root.mainloop()
    
    def start_reg(self):
        if not self.start_flag:
            self.start_flag = True
            self.start_button_text.set('停止')
        else:
            self.start_flag = False
            self.start_button_text.set('开始扫描')
    
    def export_reg(self):
        pass



if __name__ == "__main__":
    app = Application()
    app.launch()

