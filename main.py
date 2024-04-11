import tkinter
from tkinter import *
from tkinter import _setit

import calculations


def ladida():
    print(valu.get())


def print_it():
    r3.pack()
    r4.pack()


def lala(*args):
    r3.pack()
    r4.pack()
    if val.get() == '1':
        drop["menu"].delete(0, "end")
        for option in options:
            drop["menu"].add_command(label=option, command=_setit(drop_dwn, option))
    else:
        drop["menu"].delete(0, "end")
        for option in options1:
            drop["menu"].add_command(label=option, command=_setit(drop_dwn, option))
    drop_dwn.set("")
    rt_wn.update()
    drop.pack()


def print_variable(variable):
    variable_name = [name for name, value in locals().items() if value is variable][0]
    print(f"Variable name using locals(): {variable_name}")


rt_wn = Tk()
access_data = calculations.calculations("csvs to load")
val = StringVar(rt_wn, "0")
valu = StringVar(rt_wn, "0")
r1 = Radiobutton(rt_wn, text='Suggest Best Price for Quantity or Profit', value=1, command=print_it,
                 variable=val)
r2 = Radiobutton(rt_wn, text="Optimal Prices by Seasons", value=2, command=print_it, variable=val)
r1.pack()
r2.pack()

optionz = access_data.get_dataFrame()["Product"].sort_values(ascending=True).unique()
options = optionz.tolist()
options1 = ["Jan - March", "April - June", "Jul - Sep", "Oct - Dec"]
r3 = Radiobutton(rt_wn, text='Quantity', value=3, command=lala, variable=valu)
r4 = Radiobutton(rt_wn, text="Profit", value=4, command=lala, variable=valu)
drop_dwn = StringVar()
drop = OptionMenu(rt_wn, drop_dwn, *options1)
drop.forget()
rt_wn.mainloop()
"""

"""
