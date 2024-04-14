import os.path
import shutil
import tkinter
from tkinter import *
from tkinter import filedialog

final_path1 = os.path.join(os.path.expanduser('~'), 'IdeaProjects\\capstone2')
folder_path1 = os.path.join(final_path1, "csvs to load")
if not os.path.exists(folder_path1):
    os.makedirs(folder_path1)
file_wn = Tk()
wel_msg = Message(file_wn, text="Would you like to add a new file or folder to the database?", width=300)
exit_btn = Button(file_wn, text="exit", command=file_wn.destroy)
error_txt = Text(file_wn, height=10, width=30)


def add_file(yes_btn, no_btn):
    wel_msg.config(text="File or Folder?")
    yes_btn.config(text="File", command=lambda: open_file("File"))
    no_btn.config(text="Folder", command=lambda: open_file("Folder"))
    exit_btn.grid(row = 3, column = 2)


def open_file(file_vale):
    print(file_vale)
    if file_vale == "File":
        file_names = filedialog.askopenfilenames()
        move_multiple_files(file_names)
    else:
        folder_name = filedialog.askdirectory()
        move_all_directory(folder_name)


def move_multiple_files(filenames):
    success_failure = []
    for filename in filenames:
        print(filename)
        try:
            if filename.endswith(".csv"):
                shutil.move(filename, folder_path1)
        except FileNotFoundError:
            success_failure.append("File Not Found : " + filename.name)
        except PermissionError:
            success_failure.append("Permission denied. Make sure you have the necessary permissions : " + filename)
        except shutil.Error:
            success_failure.append("File already exists in database : " + filename)
    if len(success_failure) == 0:
        wel_msg.config(text="All files successfully added.  Exit or add more.")
    else:
        wel_msg.config(text="Not all files successfully added. Try again.")
        for item in success_failure:
            error_txt.insert(END, item + "\n")
        error_txt.grid(rowspan= 3, columnspan = 3)


def move_all_directory(folder_name):
    files_to_move = []
    for file in os.listdir(folder_name):
        if os.path.isfile(os.path.join(folder_name, file)):
            files_to_move.append(file)
    move_multiple_files(files_to_move)


def make_window():
    yes_value = StringVar()
    yes_value.set(" ")
    no_btn = Button(file_wn, text="no", command=file_wn.destroy)
    yes_btn = Button(file_wn, text="yes", command=lambda: add_file(yes_btn, no_btn))
    wel_msg.grid(rowspan= 3, columnspan = 3 )
    yes_btn.grid(row=3, column=0)
    no_btn.grid(row=3, column=1,)
    exit_btn.grid(row = 3, column = 2)
    file_wn.mainloop()


class file_add_window:
    def __init__(self):
        make_window()
