import tkinter as tk
from tkinter import ttk

root= tk.Tk()
root.title(" Menu Demo")

menubar= tk.Menu(root)
root.config(menu=menubar)


file_menu= tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)

root.mainloop()