import tkinter as tk
import tkinter.ttk as ttk
import sv_ttk
import pywinstyles, sys
import datetime
import os




path = "C:\\Users\\User\log\\"
month = datetime.date.today().strftime("%Y.%m")
day = datetime.date.today().strftime("%Y.%m\\%d.txt")
current_path = path + day
fcs = ""
def daily_check():
    if not os.path.exists(path + month):
        os.makedirs(path + month)
    if not os.path.exists(path + day):
        open(path + day, "a").close()

    with open(current_path, "r", encoding="utf-8") as input_file:
        text = input_file.read()
        input_file.close()
        return text
def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)
def handle_click(event):
    global fcs
    global current_path
    item = treeview.identify("item",event.x, event.y)
   # print(treeview.item(item)["text"]) #TXT FILE NAME
   # print(treeview.parent(item)) #FOLDER NAME
    click_path = f'{path}{treeview.parent(item)}\\{treeview.item(item)["text"]}'
   # print(click_path)
    if not fcs.__eq__(treeview.focus()) and click_path.find(".txt") != -1:
        print("focus changed to .txt")
        save_text()
        current_path = click_path
        with open(current_path, "r", encoding="utf-8") as input_file:
            txt = input_file.read()
            text.delete(1.0, tk.END)
            text.insert(tk.INSERT, txt)
            input_file.close()

    else:
        print("focus did not change")
    fcs = treeview.focus()
textdata = daily_check()
def callback():
    save_text()
    root.destroy()
def get_folders():
    directory = os.fsencode(path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        treeview.insert('',tk.END, filename,text=filename)
        txt_directory = os.fsencode(path + filename)
        for txt_file in os.listdir(txt_directory):
            txt_filename = os.fsdecode(txt_file)
            txt = treeview.insert(filename,tk.END, text=txt_filename)
def save_text():
    exittext = text.get("1.0",tk.END)
    with open(current_path, "w", encoding="utf-8") as input_file:
        input_file.write(exittext.strip())
        input_file.close()


root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", callback)
root.title("Log App")
root.bind("<Button-1>", handle_click)

#root.geometry("1100x560") #330x560 left side, 770x560 right side, 1100x560 total
root.rowconfigure(0, weight=1,minsize=560)
root.columnconfigure(0, weight=1,minsize=330)
root.columnconfigure(1, weight=1,minsize=770)
frm_left = ttk.Frame(root,borderwidth=5,relief="ridge", padding=10)
frm_right = ttk.Frame(root,borderwidth=5,relief="ridge", padding=10)

frm_left.grid(row=0, column=0,sticky="nsew")
frm_right.grid(row=0, column=1)

treeview = ttk.Treeview(frm_left)
treeview.grid(column=0,row=0, sticky=tk.NSEW)
s = ttk.Scrollbar(frm_left,orient=tk.VERTICAL,command=treeview.yview)
treeview['yscrollcommand'] = s.set
ttk.Label(frm_left, text="Status Message Here", anchor=tk.W).grid(column=0,columnspan=2,row=1,sticky=tk.EW)
frm_left.grid_columnconfigure(0, weight=1)
frm_left.grid_rowconfigure(0, weight=1)

get_folders()
text = tk.Text(frm_right)
text.insert(tk.INSERT, textdata)
text.grid(column=0,row=0,sticky=tk.NSEW)

sv_ttk.set_theme("dark")
# Example usage (replace `root` with the reference to your main/Toplevel window)

apply_theme_to_titlebar(root)
root.mainloop()