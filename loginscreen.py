import time
import tkinter as tk
from tkinter import messagebox as msg

from PIL import ImageTk, Image

from librarianscreen import libscr
from sqlconnectionfunc import check_sql_account

global img_exit_button, img, icon_image, img_minimize_button


def login(rt: tk.Tk):
    global img_exit_button, img, icon_image, img_minimize_button
    rt.destroy()
    root = tk.Tk()

    # Window Attributes/definition
    icon = tk.PhotoImage(file="icon.png")
    root.iconphoto(False, icon)
    root.title("AdLiMaS --Login")
    root.state('zoomed')
    root.minsize(1920, 1080)
    root.wm_attributes('-topmost', True)
    root.attributes('-fullscreen', True)

    # Background
    img = ImageTk.PhotoImage(Image.open("initbackground.jpg"))
    backgnd = tk.Label(root, image=img, cursor='star')
    backgnd.place(x=0, y=0, relwidth=1, relheight=1)
    popup(root, backgnd)

    # AdLiMaS logo
    icon_image = ImageTk.PhotoImage(Image.open("ffb03228-09e9-44dd-b411-806997d1ee8b_200x200.png"))
    icon_image_label = tk.Label(root, image=icon_image, bg='black', cursor='star')
    icon_image_label.place(relx=0, rely=1, anchor=tk.SW)
    popup(root, icon_image_label)

    # Copyright Protected (Background) Info label
    copyright_label = tk.Label(root,
                               text='Background is used from: https://wallpaperaccess.com\n'
                                    'WallpaperAccess © 2021 - Wallpapers are for personal use only.',
                               bg="black", fg='blue', font=('Calibri', '13'), cursor='star')
    copyright_label.place(relx=0.514, rely=0.98, anchor=tk.CENTER)
    popup(root, copyright_label)

    # Minimize button in the top-right corner
    img_minimize_button = ImageTk.PhotoImage(Image.open("minimize62512.png"))
    minimize_button = tk.Button(root, image=img_minimize_button, command=root.iconify, cursor='exchange')
    minimize_button.place(relx=0.97, y=-1, anchor=tk.NE)
    popup(root, minimize_button)

    def deff():
        if msg.askyesno("Leaving", "Are you sure you want to leave?"):
            root.destroy()

    # Exit Button in the top-right corner
    img_exit_button = ImageTk.PhotoImage(Image.open("exit62512.png"))
    exit_button = tk.Button(root, image=img_exit_button, command=deff, cursor='pirate')
    exit_button.place(relx=1, y=-1, anchor=tk.NE)
    popup(root, exit_button)

    # Login Frame at the centre
    login_frame = tk.LabelFrame(root, bg="#d3845f", bd=5, text='Login', font=('Calibri', '24', 'bold'), width=400,
                                height=400, cursor='star')
    login_frame.place(relx=0.514, rely=0.5265, anchor=tk.CENTER)
    popup(root, login_frame)

    # Label for "Credentials"
    credentials_label = tk.Label(login_frame, text='Credentials', cursor='star', font=('Times', '20', 'bold'),
                                 bg="#d3845f")
    credentials_label.place(anchor=tk.N, relx=0.19, rely=0.08)
    popup(root, credentials_label)

    # Label for "Username"
    username_label = tk.Label(login_frame, text='Username', cursor='star', font=('Times', '18', 'bold'), bg="#d3845f")
    username_label.place(anchor=tk.N, relx=0.22, rely=0.2)
    popup(root, username_label)

    # Entry Field for "Username"
    username_entry = tk.Entry(login_frame, exportselection=0, relief='ridge', bd=3, font=('Calibri', '14', 'bold'),
                              width=33, bg="#dfa68b", cursor='star')
    username_entry.place(anchor=tk.N, relx=0.55, rely=0.27)
    username_entry.focus()
    popup(root, username_entry)

    # Label for "Password"
    password_label = tk.Label(login_frame, text='Password', cursor='star', font=('Times', '18', 'bold'), bg="#d3845f")
    password_label.place(anchor=tk.N, relx=0.22, rely=0.37)
    popup(root, password_label)

    # Xeta function has been made for checking and logging in users
    # The reason password entry field was not assigned to variable is for security(Password must not be stored many times)

    def xeta(event):
        _ = event  # "_" has been used to assign to it a garbage value
        a = username_entry.get()
        if a != "" and password_entry.get() != "":
            if check_sql_account(a.strip(), password_entry.get().strip()):
                libscr(root, a)
            else:
                msg.showinfo(title="No Account Found", message="Not Registered?\n"
                                                               "Ask the Librarian to register you.")
        elif a == "":
            msg.showwarning(title="Username Field blank!", message="Please enter an Username!")
        else:
            msg.showwarning(title="Password Field blank!", message="Please enter a Password!")

    # Entry field for "Password"
    password_entry = tk.Entry(login_frame, exportselection=0, relief='ridge', bd=3, font=('Calibri', '14', 'bold'),
                              width=33, bg="#dfa68b", show="*", cursor='star')
    password_entry.place(anchor=tk.N, relx=0.55, rely=0.44)
    password_entry.bind("<Return>", xeta)  # to make it work with "Enter Key"
    popup(root, password_entry)

    # Button to "Login"
    login_button = tk.Button(login_frame, text='Login', font=('Calibri', '20', 'bold'), bg="#d3845f", relief='raised',
                             bd=5,
                             activebackground="#dfa68b", width=20, command=lambda: xeta(1), cursor='star')
    login_button.place(anchor=tk.N, relx=0.5, rely=0.68)
    login_button.bind("<Return>", xeta)  # to make it work with "Enter key"
    popup(root, login_button)

    # Label for Users with no account
    user_not_exist_label = tk.Label(login_frame,
                                    text='Not Registered?\nAsk the Librarian to register you.',
                                    bg="#d3845f", fg='blue', font=('Times', '12'), bd=3, relief='sunken', cursor='star')
    user_not_exist_label.place(anchor=tk.N, rely=0.9, relx=0.5)
    popup(root, user_not_exist_label)

    # Clock function has been defined and kept in script instead of a module in order to update the time every second.

    def clock():
        hour = time.strftime("%I")
        minute = time.strftime("%M")
        sec = time.strftime("%S")
        day = time.strftime("%A")
        am_pm = time.strftime("%p")
        day_of_month = time.strftime("%d")
        month = time.strftime("%B")
        year = time.strftime("%Y")
        clock_label.config(
            text=hour + " : " + minute + " : " + sec + " " + am_pm + "\n" + day + ", " + day_of_month + " " + month + " " + year)
        clock_label.after(1000, clock)

    # "The clock" on the bottom right corner
    clock_label = tk.Label(root, text='CLOCK', bg='black', fg='white', font=('Arial', '18', 'bold'), cursor='star')
    clock_label.place(anchor=tk.SE, relx=1, rely=1)
    clock()
    popup(root, clock_label)

    root.mainloop()


# Popup function is to enable right-clicking throughout the GUI


def popup(child: tk.Tk or tk.Toplevel, widget):
    def version():
        msg.showinfo(title="Version", message="This is a project in development\n"
                                              "But you can consider the version as\n"
                                              "___Version 2021.0.1___")

    def kill():
        if msg.askyesno("Leaving?", "Are you sure you want to exit?"):
            child.destroy()

    def copyrt():
        msg.showinfo(title='Copyrighted Materials Information', message="The background you are seeing\n"
                                                                        "has been taken from\n"
                                                                        "https://wallpaperaccess.com\n"
                                                                        "WallpaperAccess ©2021\n"
                                                                        "Wallpapers are for personal use only.")

    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label='Copyright Protected Resources', command=copyrt)
    menu.add_command(label="Version", command=version)
    menu.add_separator()
    menu.add_command(label='Exit', command=kill)

    def do_popup(event):
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    widget.bind("<Button-3>", do_popup)
