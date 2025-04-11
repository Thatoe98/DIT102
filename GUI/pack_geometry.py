import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x900+200+200")

root.iconbitmap("D:/6708351_dit102/GUI/DIT.ico")

label_welcome = tk.Label(root, text="Welcome to Fuel Efficiency Calculator", bg="orange", fg="white")
label_welcome.pack(fill=tk.X)

fuel_image = tk.PhotoImage(file="D:/6708351_dit102/GUI/fuel.png")
resized_image = fuel_image.subsample(4, 4)
label_image = tk.Label(root, image=resized_image)
label_image.pack()

label_distance = tk.Label(root, text="Distance travelled in km:", bg="blue", fg="white")
label_distance.pack(fill=tk.X, pady=10)
entry_distance = tk.Entry(root)
entry_distance.pack()

label_fuel = tk.Label(root, text="Fuel used in litres:", bg="orange", fg="white")   
label_fuel.pack(fill=tk.X, pady=10)
entry_fuel = tk.Entry(root)
entry_fuel.pack()
output = None

def calculate_efficiency():
    try:
        distance = float(entry_distance.get())
        fuel = float(entry_fuel.get())
        efficiency = round(distance / fuel , 2)
        output = tk.Label(root, text="Fuel efficiency is: " + str(efficiency) + " km/l", bg="green", fg="white")
        output.pack()
    except ValueError:
        tk.Label(root, text="Invalid input", bg="red", fg="white").pack()
    except ZeroDivisionError:
        tk.Label(root, text="Fuel cannot be zero", bg="red", fg="white").pack()

button_calculate = ttk.Button(root, text="Calculate", command=calculate_efficiency) # Corrected line!
def clear_all ():
    entry_distance.delete(0, tk.END)
    entry_fuel.delete(0, tk.END)
    if output:
        output.pack_forget()
button_calculate = ttk.Button(root, text="Calculate", command=calculate_efficiency) # Corrected line!
button_clear = ttk.Button(root, text="Clear", command=clear_all).pack()

button_calculate.pack()
root.mainloop()