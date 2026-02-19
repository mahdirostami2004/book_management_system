


import tkinter as tk
import sys
import os

# افزودن مسیر پروژه به path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.ui.main_window import MainWindow


def main():
    
    root = tk.Tk()
    app = MainWindow(root)
    
    # تنظیم handler برای بستن برنامه
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # اجرای برنامه
    root.mainloop()


if __name__ == "__main__":
    main()

