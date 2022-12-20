from email import message
import tkinter as tk
from tkinter import filedialog as fd
from .PlatformConstants import CUR_DIR as cdir

root = tk.Tk()
root.title("Open File")
root.resizable(False, False)
root.geometry("300x150")
root.withdraw()


def open_file():
    types = (("All files", "*.*"),)

    filename = fd.askopenfilename(title="Open files", initialdir=cdir, filetypes=types)

    return filename
