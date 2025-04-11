

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry('300x200')
root.title('Button Widget')

tk.Label(root, text='Username').pack()
textbox = ttk.Entry(root)
textbox.pack()

def on_button_click():
    s = textbox.get()
    print(s)
    ttk.Label(root, text="Welcome to RSU " + s, foreground="blue", background="red").pack()

ttk.Button(root, text='Submit', command=on_button_click).pack() # corrected line


root.mainloop()