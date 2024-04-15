import tkinter as tk
from tkinter import ttk, _setit

import matplotlib.backends.backend_tkagg
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import calculations
import file_add_window


def lo():
    drop.grid()
    frame_drp.grid()
    exit_btn.grid(row=9)


def run_process():
    y_axis = sec_set.get()
    product_sell = drp_.get()
    final_eval = access_data.optimal_price("Price", y_axis, product_sell)
    return final_eval


def select_drop(*args):
    quant_profit = sec_set.get()
    drp_choice = drp_.get()
    final_lola = {}
    final_mess.grid_forget()
    if first_set.get() == "1":
        a = run_process()
        if a != -1:
            final_string = "The best price for max " + quant_profit.lower() + " is $" + str(a)
            final_mess.config(text=final_string, width=300)
            final_mess.grid()
            plot_button.config(text="See trend line", command=lambda: show_plot(drp_choice))
            plot_button.grid()
        else:
            plot_button.grid_forget()
            frame_line.grid_forget()
            final_mess.config(text="Not enough data. Add more records or try another product", width=300)
            final_mess.grid()
    else:
        index = 1
        aa = access_data.best_prod_for_season(drp_choice, quant_profit)
        final_lola = aa
        bb = ""
        label.config(text=("Best items to sell during " + drp_choice + " and optimal sales price."))
        for key, value in aa.items():
            bb = f"{key}: {value}"
            listbox.insert(index, bb)
            index += 1
        label.grid()
        listbox.grid()
        frame_list.grid()
    for g in range(len(final_lola)):
        listbox.delete(g)


def print_it():
    sec_set.set(" ")
    frame_plots.grid_forget()
    frame_line.grid_forget()
    num = int(first_set.get())
    if num == 2:
        options1 = ["Jan - March", "April - June", "Jul - Sep", "Oct - Dec"]
        drop["menu"].delete(0, "end")
        for option in options1:
            drop["menu"].add_command(label=option, command=_setit(drp_, option))
    else:
        drop["menu"].delete(0, "end")
        for option in options:
            drop["menu"].add_command(label=option, command=_setit(drp_, option))

    r8_var.set(" ")
    frame.grid(row=5)
    exit_btn.grid(row=7)


def show_plot(drp_1):
    frame_line.grid_forget()
    frog1.clear()
    canvas3.get_tk_widget().forget()
    frame_line.update()
    if drp_1 is not "0" and type(drp_1) is str:
        plot2 = access_data.linear_reg(frog1, drp_1, sec_set.get())
        canvas3.draw()
        canvas3.get_tk_widget().grid()
        frame_line.grid()


def show_plots(fog):
    final_mess.grid_forget()
    first_set.set(" ")
    frame.grid_forget()
    frame_line.grid_forget()
    frame_drp.grid_forget()
    frame_list.grid_forget()
    fog.clear()
    if r8_var.get() == "3":
        access_data.pie_chatrt(frame_plots)

    else:
        access_data.bar_chart(frame_plots)
    frame_plots.grid()


initial_window = file_add_window.file_add_window()
rt_wn = tk.Tk()
rt_wn.title("Capstone Project")

frame = tk.Frame(rt_wn)
frame_plots = tk.Frame(rt_wn)
frame_drp = tk.Frame(rt_wn)
frame_line = tk.Frame(rt_wn)
frame_list = tk.Frame(rt_wn)

access_data = calculations.calculations("csvs to load")
first_set = tk.StringVar(rt_wn, "0")
r8_var = tk.StringVar(frame_plots, "0")
sec_set = tk.StringVar(frame, " ")

fig, ax = plt.subplots()

r1 = tk.Radiobutton(rt_wn, text='Suggest Best Price for Quantity or Profit', value=1,
                    command=print_it,
                    variable=first_set)
r2 = tk.Radiobutton(rt_wn, text="Optimal Prices by Seasons", value=2, command=print_it,
                    variable=first_set)

# second set of radio buttons
r3 = tk.Radiobutton(frame, text='Quantity', command=lo, value="Quantity", variable=sec_set)
r4 = tk.Radiobutton(frame, text="Profit", command=lo, value="Profit", variable=sec_set)

# third set of radio buttons
r7 = tk.Radiobutton(rt_wn, text='Profit by Product', command=lambda: show_plots(fig), variable=r8_var,
                    value="3")
r8 = tk.Radiobutton(rt_wn, text="Total Profit YoY", command=lambda: show_plots(fig), variable=r8_var, value="4")

r1.grid()
r2.grid()
r3.grid()
r4.grid()
r7.grid()
r8.grid()
final_mess = tk.Message(rt_wn, text="Not enough data. Add more records or try another product", width=300)

# Drop down menu and options
optionz = access_data.get_dataframe()["Product"].sort_values(ascending=True).unique()
options = optionz.tolist()
drp_ = tk.StringVar(frame_drp, " ")
drop = tk.OptionMenu(frame_drp, drp_, *options)
drp_.trace_add("write", select_drop)

plot_button = tk.Button(frame_drp, text="shouldbgone")

# Show frame 1 initially
exit_btn = tk.Button(rt_wn, text="exit", command=rt_wn.destroy)
exit_btn.grid()

frog1 = Figure(figsize=(5, 5),
               dpi=100)
canvas3 = FigureCanvasTkAgg(frog1, frame_line)

# Label and List box
label = tk.Message(frame_list, width=300, text="Best", )
listbox = tk.Listbox(frame_list, height=10, width=30)

rt_wn.mainloop()
