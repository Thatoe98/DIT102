#create login window with tkinter and ttk module
#use tk, ttk to develop a login screen with the following widgets:
#1. label
#photo
#entry
#button
import tkinter as tk
from tkinter import ttk
root = tk.Tk()  #create a window
root.geometry("400x400")
label = ttk.Label(text="Login")
label.pack()
photo = tk.PhotoImage(file="D:/6708351_dit102/GUI/DIT.ico")
label = ttk.Label(image=photo) 
label.image = photo  # keep a reference to the image
label.pack()
root.mainloop()  #display the window