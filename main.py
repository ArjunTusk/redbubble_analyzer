import tkinter
from tkinter import *
from tkinter import _setit

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import calculations

"""
calls the second set of radio buttons. Disappears radio btns if item =0. Display otherwise
Also updates the drop down menu with relevant options.
"""


def print_it(plot_button1):
    final_mess.grid_forget()
    canvas.get_tk_widget().grid_forget()
    plot_button1.grid_forget()
    fig.clear()
    if item.get() == "0":
        r3.forget()
        r4.forget()
    else:
        r3.grid()
        r4.grid()
    if int(item.get()) == 2:
        options1 = ["Jan - March", "April - June", "Jul - Sep", "Oct - Dec"]
        drop["menu"].delete(0, "end")
        for option in options1:
            drop["menu"].add_command(label=option, command=_setit(drp_, option))
    else:
        drop["menu"].delete(0, "end")
        for option in options:
            drop["menu"].add_command(label=option, command=_setit(drp_, option))
    listbox.grid_forget()
    label.grid_forget()
    rt_wn.update()


"""
Removes the buttons then displays drop down menu
"""


def next_up(r5, r6):
    r5.forget()
    r6.forget()
    rt_wn.update()
    drop.grid()


def select_drop(*args):
    run_process()


"""
For use when selecting optimal prices.
options22 is the dict that holds the time ranges
"""


def run_process():
    final_eval = 0.0
    final_lol = {}
    options22 = {"Jan - March": [1, 3], "April - June": [4, 6], "Jul - Sep": [7, 9], "Oct - Dec": [10, 12]}
    if item.get() == "1":
        final_eval = access_data.optimal_price("Price", valu.get(), drp_.get())
        if final_eval != -1:
            final_string = "The best price for max " + valu.get().lower() + " is $" + str(final_eval)
            final_mess.config(text=final_string, width=300)
            final_mess.grid()
            a = drp_.get()
            plot_button.config(command=lambda: show_plot(a), text="See trendlines for data")
            plot_button.grid()
        else:
            final_mess.grid()
    else:
        index = 1
        aa = access_data.best_prod_for_season(options22[drp_.get()][0], options22[drp_.get()][1], valu.get())
        final_lol = aa
        bb = ""
        label.config(text=("Items to sell during " + drp_.get() + " and optimal sales price."))
        for key, value in aa.items():
            bb = f"{key}: {value}"
            listbox.insert(index, bb)
            index += 1
        final_mess.grid_forget()
        plot_button.config(command=lambda: show_plot(final_lol), text="See trendlines for data")
        plot_button.grid()
        label.grid()
        listbox.grid()
    for g in range(len(final_lol)):
        listbox.delete(g)
    drp_.set("")
    drop.grid()


def show_plot(drp_1):
    if drp_1 is not "0" and type(drp_1) is str:
        plot2 = access_data.linear_reg(fig, drp_1, valu.get())
        canvas.draw()
        canvas.get_tk_widget().grid()
    else:
        access_data.linear_reg1(drp_1)


rt_wn = Tk()
drp_ = StringVar()
plot_button = Button(rt_wn, text="shouldbgone")
access_data = calculations.calculations("csvs to load")
# item = first set of radio buttons variables
item = StringVar(rt_wn, "0")
fig = Figure(figsize=(5, 5),
             dpi=100)
canvas = FigureCanvasTkAgg(fig, rt_wn)
# valu = second set of radio buttons variables
valu = StringVar(rt_wn, " ")
# first set of radio buttons
r1 = Radiobutton(rt_wn, text='Suggest Best Price for Quantity or Profit', value=1,
                 command=lambda: print_it(plot_button),
                 variable=item)
r2 = Radiobutton(rt_wn, text="Optimal Prices by Seasons", value=2, command=lambda: print_it(plot_button), variable=item)
r1.grid()
r2.grid()

# second set of radio buttons
r3 = Radiobutton(rt_wn, text='Quantity', value="Quantity", command=lambda: next_up(r3, r4), variable=valu)
r4 = Radiobutton(rt_wn, text="Profit", value="Profit", command=lambda: next_up(r3, r4), variable=valu)

# Drop down menu and options
optionz = access_data.get_dataframe()["Product"].sort_values(ascending=True).unique()
options = optionz.tolist()
drop = OptionMenu(rt_wn, drp_, *options)
drp_.trace_add("write", select_drop)
plot1 = access_data.linear_reg(fig, drp_.get(), "Quantity")
# Label and List box
label = Message(rt_wn, width=300, text="Best", )
listbox = Listbox(rt_wn, height=10, width=30)
final_mess = Message(rt_wn, text="Not enough data. Add more records or try another product", width=300)
rt_wn.mainloop()

"""
"""
