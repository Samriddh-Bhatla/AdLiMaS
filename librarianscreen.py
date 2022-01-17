import calendar
import datetime
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as msg
from tkinter import ttk

import pandas as pd
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from iss_ret import iss, ret
from sqlconnectionfunc import add_sql_account as aye, check_sql_username as bye, csv_to_table as atit, \
    add_table_row as addit, read_table_cell as dialit, run_query as run

global zeta, icon, beta, icon_image, img_minimize_butto, add_acc_button_img, img_logout_butto, path, acc_pic, pic2, pic3, pic4


def libscr(root: tk.Tk, curuser: str):
    global zeta, icon, beta, icon_image, img_minimize_butto, add_acc_button_img, img_logout_butto, acc_pic

    # Window definition
    zeta = tk.Toplevel(root)
    root.withdraw()
    icon = tk.PhotoImage(file="icon.png")
    zeta.iconphoto(False, icon)
    zeta.title("AdLiMaS --{}".format(curuser))
    zeta.state('zoomed')
    zeta.minsize(1920, 1080)
    zeta.wm_attributes('-topmost', True)
    zeta.attributes('-fullscreen', True)

    # Background Image
    beta = ImageTk.PhotoImage(Image.open("253342.jpg"))
    background = tk.Label(zeta, image=beta)
    background.place(x=0, y=0, relwidth=1, relheight=1)
    popup(root, zeta, background)

    # AdLiMaS logo on bottom-left corner
    icon_image = ImageTk.PhotoImage(Image.open("ffb03228-09e9-44dd-b411-806997d1ee8b_200x200.png"))
    icon_image_label = tk.Label(zeta, image=icon_image, bg='black')
    icon_image_label.place(relx=0, rely=1, anchor=tk.SW)
    popup(root, zeta, icon_image_label)

    # Minimize button on top-right corner
    img_minimize_butto = ImageTk.PhotoImage(Image.open("minimize62512.png"))
    minimize_butto = tk.Button(zeta, image=img_minimize_butto, command=zeta.iconify)
    minimize_butto.place(relx=0.915, x=0, y=-1, anchor=tk.NE)
    popup(root, zeta, minimize_butto)

    # Copyright Protected (Background) Info label
    copyright_label = tk.Label(zeta,
                               text='Background is used from: https://wallpaperaccess.com\n'
                                    'WallpaperAccess © 2021 - Wallpapers are for personal use only.',
                               bg="black", fg='blue', font=('Calibri', '13'), cursor='star')
    copyright_label.place(relx=0.514, rely=0.98, anchor=tk.CENTER)
    popup(root, zeta, copyright_label)

    def add_book_csv():
        msg.showinfo("Important",
                     "The Columns of the csv file must be the following\n"
                     "Acc_no\n"
                     "ISBN\n"
                     "Title\n"
                     "Author\n"
                     "Category (One of Curriculum, Novel, Encyclopedia, Comic)\n"
                     "Genre_sub\n"
                     "Copies_total\n"
                     "Copies_available\n\n"
                     "And in the same order.")

        # Add Book Data From CSV file LabelFrame
        add2 = tk.LabelFrame(zeta, text="Add Book Data from CSV", bd=5,
                             font=('Times', '24', 'bold', 'italic'),
                             bg="#d3845f", width=zeta.winfo_screenwidth() - 750, height=zeta.winfo_screenheight() - 450)
        add2.place(anchor=tk.N, relx=0.52, rely=0.2)
        tree = ttk.Treeview(add2)
        tree_style = ttk.Style()
        tree_style.theme_use("clam")
        tree_style.configure("Treeview",
                             background="#dfa68b",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#d3845f")
        tree_style.map("Treeview",
                       background=[('selected', 'black')])
        vertical_bar = ttk.Scrollbar(add2, orient="vertical", command=tree.yview)
        horizontal_bar = ttk.Scrollbar(add2, orient="horizontal", command=tree.xview)
        var = tk.StringVar()
        popup(root, zeta, add2)

        def ch_f():
            global path
            path = filedialog.askopenfilename(initialdir="\\Documents",
                                              title="Select a CSV file containing book records",
                                              filetypes=[("CSV files", "*.csv")])
            if len(path.strip()) > 0:
                file_chosen_label.config(text=path)
                df = pd.read_csv(path)

                df.fillna('-', inplace=True)

                # Assuming columns of dataframe are Accession_no, ISBN, title, author, category, genre_subject, copies_total and copies_available

                tree['columns'] = list(df.columns)[1:]

                tree.column("#0", minwidth=50, anchor=tk.W)
                tree.heading("#0", text=list(df.columns)[0])
                dd = list(df.columns)[1:]
                for peta in dd:
                    tree.column("{}".format(peta), minwidth=50, anchor=tk.W)
                    tree.heading("{}".format(peta), text=str(peta))

                for x in tree.get_children():
                    tree.delete(x)

                count = 0
                for yotta in df.index:
                    local_list = list(df.loc[yotta])
                    tree.insert("", "end", iid=count, values=local_list[1:], text=local_list[0])
                    count += 1

                tree.place(anchor=tk.S, relx=0.5, rely=0.7, relwidth=0.6, relheight=0.4)
                horizontal_bar.place(anchor=tk.S, relx=0.5, rely=0.715, relwidth=0.6)
                vertical_bar.place(anchor=tk.S, relx=0.805, rely=0.7, relheight=0.4)
                tree.configure(xscrollcommand=horizontal_bar.set)
                tree.configure(yscrollcommand=vertical_bar.set)
                confirm_addition_button['state'] = tk.NORMAL

        choose_file = tk.Button(add2, text='Choose File..', command=ch_f, font=('Calibri', '16', 'bold'), bg="#d3845f",
                                activebackground="#e89611")
        choose_file.place(anchor=tk.N, relx=0.3, rely=0.22)
        popup(root, zeta, choose_file)
        choose_file_label = tk.Label(add2, text='Select A file :', width=10, font=('Times', '22', 'bold'),
                                     bg="#d3845f")
        choose_file_label.place(anchor=tk.NW, relx=0.1, rely=0.15)
        popup(root, zeta, choose_file_label)
        file_chosen_label = tk.Label(add2, text='No File chosen', bg="#d3845f", font=('Time', '18', 'italic'))
        file_chosen_label.place(anchor=tk.NW, relx=0.26, rely=0.16)
        popup(root, zeta, file_chosen_label)

        def on():
            add2.destroy()
            tree.destroy()
            add_acc_button['state'] = tk.NORMAL
            add_stud_button['state'] = tk.NORMAL
            menu_main_add_book['state'] = tk.NORMAL
            add_stud_acc_button['state'] = tk.NORMAL
            iss_ret_book_button['state'] = tk.NORMAL
            chart_button['state'] = tk.NORMAL

        cancel_button = tk.Button(add2, text='CANCEL', font=('Calibri', '16', 'bold'), bg="#d3845f", command=on,
                                  activebackground="#e89611")
        cancel_button.place(anchor=tk.SE, relx=0.94, rely=1)
        popup(root, zeta, cancel_button)

        def send_csv_sql():
            x = msg.askyesnocancel(title='Continue', message="Continue? Action can't be undone.")
            if x:
                try:
                    if var.get() == "rep_table_exist":
                        try:
                            atit(path, "Book_Data", 'replace')
                            msg.showinfo(title='Table Created',
                                         message="The data passed was saved into table Book_Data")
                        except Exception as err:
                            msg.showwarning(title="Error", message=err)
                    else:
                        try:
                            atit(path, "Book_Data", 'append')
                            msg.showinfo(title="Data Appended",
                                         message="Data was appended to table Book_Data")
                        except Exception as err:
                            msg.showwarning(title="Error", message=err)
                finally:
                    on()
            else:
                on()

        tablename_label = tk.Label(add2, text='Tablename : Book_Data', width=21, font=('Times', '22', 'bold'),
                                   bg="#d3845f")
        tablename_label.place(anchor=tk.NW, relx=0.1, rely=0.8)
        popup(root, zeta, tablename_label)

        confirm_addition_button = tk.Button(add2, text='ADD', font=('Calibri', '16', 'bold'), bg="#d3845f",
                                            command=send_csv_sql,
                                            activebackground="#e89611", state=tk.DISABLED)
        confirm_addition_button.place(anchor=tk.SE, relx=1, rely=1)
        popup(root, zeta, confirm_addition_button)

        check_table_exist = tk.Checkbutton(add2, text="Replace table", variable=var, font='14',
                                           onvalue="rep_table_ifexist", offvalue="no_rep_table_ifexist",
                                           bg="#d3845f", activebackground="#d3845f")
        check_table_exist.deselect()
        check_table_exist.place(anchor=tk.S, relx=0.4, rely=1)
        popup(root, zeta, check_table_exist)

        check_app_table_exist = tk.Checkbutton(add2, text="Append below table", variable=var, font='14',
                                               onvalue="app_table_ifexist", offvalue="no_app_table_ifexist",
                                               bg="#d3845f", activebackground="#d3845f")
        check_app_table_exist.select()
        check_app_table_exist.place(anchor=tk.S, relx=0.6, rely=1)
        popup(root, zeta, check_app_table_exist)

        add_acc_button['state'] = tk.DISABLED
        add_stud_button['state'] = tk.DISABLED
        menu_main_add_book['state'] = tk.DISABLED
        add_stud_acc_button['state'] = tk.DISABLED
        iss_ret_book_button['state'] = tk.DISABLED
        chart_button['state'] = tk.DISABLED

    add_stud_button_img = ImageTk.PhotoImage(Image.open("addstudcsv62512.png"))
    add_stud_button = tk.Button(zeta, image=add_stud_button_img, cursor='plus', width=275, height=85,
                                command=add_book_csv,
                                relief='raised')
    add_stud_button.place(anchor=tk.E, relx=1, rely=0.43)
    popup(root, zeta, add_stud_button)

    def add_lib_account_win():

        # Add Account labelframe
        add = tk.LabelFrame(zeta, text='Add Librarian User', bd=5, font=('Times', '24', 'bold', 'italic'), bg="#d3845f",
                            width=zeta.winfo_screenwidth() - 750, height=zeta.winfo_screenheight() - 700)
        add.place(anchor=tk.S, relx=0.52, rely=0.9)
        popup(root, zeta, add)

        def add_account():
            jh = add_label_username_entry.get()
            if jh != "" and add_label_password_entry.get() != "":
                if bye(jh):
                    if add_label_password_entry.get() == add_label_passwordc_entry.get():
                        if msg.askyesno(title="Confirm Addition",
                                        message="Are you sure you want to add '{}'".format(jh)):
                            aye(jh, add_label_password_entry.get())
                    else:
                        msg.showwarning(title="Password Error", message="Passwords don't match! Please retry.")
                else:
                    msg.showwarning(title="User Exists", message="The Username already exists!!")
            else:
                msg.showwarning(title="Empty Fields", message="Please don't leave the fields blank!")
            on()

        def on():
            add.destroy()
            add_acc_button['state'] = tk.NORMAL
            add_stud_button['state'] = tk.NORMAL
            add_stud_acc_button['state'] = tk.NORMAL
            menu_main_add_book['state'] = tk.NORMAL
            iss_ret_book_button['state'] = tk.NORMAL
            chart_button['state'] = tk.NORMAL

        cancel_button = tk.Button(add, text='CANCEL', font=('Calibri', '16', 'bold'), bg="#d3845f", command=on,
                                  activebackground="#e89611")
        cancel_button.place(anchor=tk.SE, relx=0.94, rely=1)
        popup(root, zeta, cancel_button)
        add_label_username_label = tk.Label(add, text='Username :', width=10, font=('Times', '22', 'bold'),
                                            bg="#d3845f")
        add_label_username_label.place(anchor=tk.NW, relx=0.1, rely=0.15)
        popup(root, zeta, add_label_username_label)
        add_label_password_label = tk.Label(add, text='Password :', width=10, font=('Times', '22', 'bold'),
                                            bg="#d3845f")
        add_label_password_label.place(anchor=tk.NW, relx=0.1035, rely=0.3)
        popup(root, zeta, add_label_password_label)
        add_label_username_entry = tk.Entry(add, exportselection=0, relief='ridge', bd=3, font=('Calibri', '20'),
                                            width=33, bg="#dfa68b")
        add_label_username_entry.place(anchor=tk.NW, relx=0.25, rely=0.15)
        popup(root, zeta, add_label_username_entry)
        add_label_password_entry = tk.Entry(add, exportselection=0, relief='ridge', bd=3, font=('Calibri', '20'),
                                            width=33, bg="#dfa68b", show="*")
        add_label_password_entry.place(anchor=tk.NW, relx=0.25, rely=0.3)
        popup(root, zeta, add_label_password_entry)
        add_label_passwordc_entry = tk.Entry(add, exportselection=0, relief='ridge', bd=3, font=('Calibri', '20'),
                                             width=33, bg="#dfa68b", show="*")
        add_label_passwordc_entry.place(anchor=tk.NW, relx=0.25, rely=0.55)
        popup(root, zeta, add_label_passwordc_entry)
        add_label_passwordc_label = tk.Label(add, text='Confirm    \nPassword     :', width=10,
                                             font=('Times', '22', 'bold'), bg="#d3845f")
        add_label_passwordc_label.place(anchor=tk.NW, relx=0.09, rely=0.45)
        popup(root, zeta, add_label_passwordc_label)
        ok_button = tk.Button(add, text='ADD', font=('Calibri', '16', 'bold'), bg="#d3845f", command=add_account,
                              activebackground="#e89611")
        ok_button.place(anchor=tk.SE, relx=1, rely=1)
        popup(root, zeta, ok_button)
        add_acc_button['state'] = tk.DISABLED
        add_stud_button['state'] = tk.DISABLED
        menu_main_add_book['state'] = tk.DISABLED
        add_stud_acc_button['state'] = tk.DISABLED
        iss_ret_book_button['state'] = tk.DISABLED
        chart_button['state'] = tk.DISABLED

    add_acc_button_img = ImageTk.PhotoImage(Image.open("addacc62512.png"))
    add_acc_button = tk.Button(zeta, image=add_acc_button_img, cursor='plus', width=275, height=75,
                               command=add_lib_account_win,
                               relief='raised')
    add_acc_button.place(anchor=tk.E, relx=1, rely=0.5)
    popup(root, zeta, add_acc_button)

    def add_stud_account_win():
        # Add3 LabelFrame for adding Student Details
        add3 = tk.LabelFrame(zeta, text='Add Student', bd=5, font=('Times', '24', 'bold', 'italic'), bg="#d3845f",
                             width=zeta.winfo_screenwidth() - 750, height=zeta.winfo_screenheight() - 600)
        popup(root, zeta, add3)
        add3.place(anchor=tk.S, relx=0.52, rely=0.7)

        # Using add_account() to add the row into Student_Details
        def add_account():

            # Constructing the full name
            local_fname = fname_entry.get().strip().capitalize()
            local_lname = lname_entry.get().strip().capitalize()
            local_mi = str(mi.get())

            # Checking for middle initial and then constructing full name
            if not local_mi == "-":
                local_full_name = local_fname + " " + local_mi + " " + local_lname
            else:
                local_full_name = local_fname + " " + local_lname

            # Getting and checking the roll number
            local_roll_no = rollno_entry.get().strip()
            if not local_roll_no.isnumeric():
                msg.showwarning("Error", "Please enter numeric roll number!")
                on()
                return

            # Getting Admission number and Class_sec
            local_admno = admno_entry.get().strip().upper()
            local_class = mi5.get() + " " + sec_entry.get().strip().upper()

            # Getting the date and checking it for validity in try block
            local_dob = str(mi2.get()) + " " + str(month_dict[mi3.get()]) + " " + str(mi4.get())
            try:
                _ = calendar.day_name[datetime.datetime.strptime(local_dob, '%Y %m %d').weekday()]

                # Replacing
                local_dob = local_dob.replace(" ", "-")
                b = addit({"ADM_NO": local_admno, "NAME": local_full_name, "DOB": local_dob, "ROLL_NO": local_roll_no,
                           "CLASS_SEC": local_class}, "STUDENT_DETAILS")
                if b[0] is False:
                    msg.showwarning("Error", "An error occurred. Details:\n{}".format(b[1]))
                else:
                    msg.showinfo("Successful", "Details of {} were added successfully.".format(local_full_name))
            except ValueError:
                msg.showwarning("Error", "The Date of Birth entered is invalid!")
            on()

        def on():
            add3.destroy()
            add_acc_button['state'] = tk.NORMAL
            add_stud_button['state'] = tk.NORMAL
            add_stud_acc_button['state'] = tk.NORMAL
            menu_main_add_book['state'] = tk.NORMAL
            iss_ret_book_button['state'] = tk.NORMAL
            chart_button['state'] = tk.NORMAL

        cancel_button = tk.Button(add3, text='CANCEL', font=('Calibri', '16', 'bold'), bg="#d3845f", command=on,
                                  activebackground="#e89611")
        cancel_button.place(anchor=tk.SE, relx=0.94, rely=1)
        popup(root, zeta, cancel_button)

        # First Name label
        fname_label = tk.Label(add3, text='First Name :', width=10, font=('Times', '22', 'bold'),
                               bg="#d3845f")
        fname_label.place(anchor=tk.NW, relx=0.1, rely=0.05)
        popup(root, zeta, fname_label)

        # Last Name label
        lname_label = tk.Label(add3, text='Last Name :', width=10, font=('Times', '22', 'bold'),
                               bg="#d3845f")
        lname_label.place(anchor=tk.NW, relx=0.1035, rely=0.15)
        popup(root, zeta, lname_label)

        # First Name entry
        fname_entry = tk.Entry(add3, exportselection=0, relief='ridge', bd=3, font=('Calibri', '20'),
                               width=33, bg="#dfa68b")
        fname_entry.place(anchor=tk.NW, relx=0.25, rely=0.05)
        popup(root, zeta, fname_entry)

        # Last Name Entry
        lname_entry = tk.Entry(add3, exportselection=0, relief='ridge', bd=3, font=('Calibri', '20'),
                               width=33, bg="#dfa68b")
        lname_entry.place(anchor=tk.NW, relx=0.25, rely=0.15)
        popup(root, zeta, lname_entry)

        # Middle Initial Entry
        mi = tk.StringVar()
        mi.set("-")
        middle_ini_ent = tk.OptionMenu(add3, mi, *[x for x in "-ABCDEFGHIJKLMNOPQRSTUVWXYZ"])
        middle_ini_ent.config(font=('Calibri', '20'), bg="#dfa68b", activebackground="#dfa68b", width=1)
        middle_ini_ent['menu'].config(font=('Calibri', '17'), bg="#d3845f", activebackground="black")
        middle_ini_ent.place(anchor=tk.NW, relx=0.25, rely=0.25)
        popup(root, zeta, middle_ini_ent)

        # Middle Initial Selection Info
        lbl = tk.Label(add3, text="Select '-' if no middle initial", font=('Times', '20'), bg="#d3845f")
        lbl.place(anchor=tk.NW, relx=0.35, rely=0.27)
        popup(root, zeta, lbl)

        # Middle Initial Label
        middle_ini_label = tk.Label(add3, text='Middle Initial :', font=('Times', '22', 'bold'), bg="#d3845f")
        middle_ini_label.place(anchor=tk.NW, relx=0.08, rely=0.265)
        popup(root, zeta, middle_ini_label)

        # Roll Number Label
        rollno_label = tk.Label(add3, text='Roll No :', width=10, font=('Times', '22', 'bold'), bg="#d3845f")
        rollno_label.place(anchor=tk.NW, relx=0.119, rely=0.366)
        popup(root, zeta, rollno_label)

        # Admission Number Entry
        admno_entry = tk.Entry(add3, exportselection=0, relief='ridge', bd=3, font=('Calibri', '20'), width=10,
                               bg="#dfa68b")
        admno_entry.place(anchor=tk.NW, relx=0.25, rely=0.467)
        popup(root, zeta, admno_entry)

        # Admission Number Label
        admno_label = tk.Label(add3, text='Admission No :', font=('Times', '22', 'bold'), bg="#d3845f")
        admno_label.place(anchor=tk.NW, relx=0.077, rely=0.467)
        popup(root, zeta, admno_label)

        # Roll Number Entry
        rollno_entry = tk.Entry(add3, exportselection=0, relief='ridge', bd=3, font=('Calibri', '20'), width=3,
                                bg="#dfa68b")
        rollno_entry.place(anchor=tk.NW, relx=0.25, rely=0.366)
        popup(root, zeta, rollno_entry)

        # Date of Birth label
        dob_label = tk.Label(add3, text='Date of Birth :', font=('Times', '22', 'bold'), bg="#d3845f")
        dob_label.place(anchor=tk.NW, relx=0.08, rely=0.57)
        popup(root, zeta, dob_label)

        # Date of Birth year OptionMenu
        mi2 = tk.IntVar()
        mi2.set(2021)
        dob_year_ent = tk.OptionMenu(add3, mi2, *[x for x in range(2021, 1995, -1)])
        dob_year_ent.config(font=('Calibri', '20'), bg="#dfa68b", activebackground="#dfa68b", width=4)
        dob_year_ent['menu'].config(font=('Calibri', '14'), bg="#d3845f", activebackground="black")
        dob_year_ent.place(anchor=tk.NW, relx=0.25, rely=0.565)
        popup(root, zeta, dob_year_ent)

        # Date of Birth Month OptionMenu
        mi3 = tk.StringVar()
        month_dict = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
                      "September": 9, "October": 10, "November": 11, "December": 12}
        mi3.set("January")
        dob_month_ent = tk.OptionMenu(add3, mi3, *month_dict.keys())
        dob_month_ent.config(font=('Calibri', '20'), bg="#dfa68b", activebackground="#dfa68b", width=10)
        dob_month_ent['menu'].config(font=('Calibri', '14'), bg="#d3845f", activebackground="black")
        dob_month_ent.place(anchor=tk.NW, relx=0.345, rely=0.565)
        popup(root, zeta, dob_month_ent)

        # Date of Birth Day Menu
        mi4 = tk.IntVar()
        mi4.set(1)
        dob_day_ent = tk.OptionMenu(add3, mi4, *[x for x in range(1, 32, 1)])
        dob_day_ent.config(font=('Calibri', '20'), bg="#dfa68b", activebackground="#dfa68b", width=2)
        dob_day_ent['menu'].config(font=('Calibri', '14'), bg="#d3845f", activebackground="black")
        dob_day_ent.place(anchor=tk.NW, relx=0.51, rely=0.565)
        popup(root, zeta, dob_day_ent)

        # Class Label
        class_label = tk.Label(add3, text='Class :', width=6, font=('Times', '22', 'bold'), bg="#d3845f")
        class_label.place(anchor=tk.NW, relx=0.155, rely=0.685)
        popup(root, zeta, class_label)

        # Class Selection OptionMenu
        mi5 = tk.StringVar()
        mi5.set("")
        class_ent = tk.OptionMenu(add3, mi5,
                                  *["Nursery", "LKG", "UKG", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
                                    "X", "XI", "XII"])
        class_ent.config(font=('Calibri', '20'), bg="#dfa68b", activebackground="#dfa68b", width=5)
        class_ent['menu'].config(font=('Calibri', '17'), bg="#d3845f", activebackground="black")
        class_ent.place(anchor=tk.NW, relx=0.25, rely=0.685)
        popup(root, zeta, class_ent)

        # Section Name Entry
        sec_entry = tk.Entry(add3, exportselection=0, relief='ridge', bd=3, font=('Calibri', '24'), width=8,
                             bg="#dfa68b")
        sec_entry.place(anchor=tk.NW, relx=0.355, rely=0.69)
        popup(root, zeta, sec_entry)

        global acc_pic

        # Photo from iconfinder.com(©2020 Iconfinder, ApS)
        acc_pic = ImageTk.PhotoImage(Image.open("iconfinder_header-account-image-line_1540176.png"))
        acc_pic_label = tk.Label(add3, image=acc_pic, bg="#d3845f")
        acc_pic_label.place(anchor=tk.NW, relx=0.8, rely=0.05, relwidth=0.2, relheight=0.5)
        popup(root, zeta, acc_pic_label)

        # Add button
        ok_button = tk.Button(add3, text='ADD', font=('Calibri', '16', 'bold'), bg="#d3845f", command=add_account,
                              activebackground="#e89611")
        ok_button.place(anchor=tk.SE, relx=1, rely=1)
        popup(root, zeta, ok_button)

        # Making all external LabelFrame calling buttons disabled
        add_acc_button['state'] = tk.DISABLED
        add_stud_button['state'] = tk.DISABLED
        add_stud_acc_button['state'] = tk.DISABLED
        menu_main_add_book['state'] = tk.DISABLED
        iss_ret_book_button['state'] = tk.DISABLED
        chart_button['state'] = tk.DISABLED

    add_stud_acc_button_img = ImageTk.PhotoImage(Image.open("Picture1.png"))
    add_stud_acc_button = tk.Button(zeta, image=add_stud_acc_button_img, cursor='plus', width=275, height=75,
                                    command=add_stud_account_win,
                                    relief='raised')
    add_stud_acc_button.place(anchor=tk.E, relx=1, rely=0.5725)
    popup(root, zeta, add_stud_acc_button)

    def deff():
        if msg.askyesno("Log out?", "Are you sure you want to log out?"):
            root.deiconify()
            zeta.destroy()

    img_logout_butto = ImageTk.PhotoImage(Image.open("log_out.png"))
    logout_butto = tk.Button(zeta, image=img_logout_butto, command=deff,
                             height=img_minimize_butto.height(), width=150)
    logout_butto.place(relx=1, x=0, y=-1, anchor=tk.NE)
    popup(root, zeta, logout_butto)

    # More Menu

    def add_book():

        add_book_frame = tk.LabelFrame(zeta, text="Add a Book", bd=5,
                                       font=('Times', '24', 'bold', 'italic'),
                                       bg="#d3845f", width=zeta.winfo_screenwidth() - 750,
                                       height=zeta.winfo_screenheight() - 450)
        add_book_frame.place(anchor=tk.N, relx=0.5, rely=0.3)
        popup(root, zeta, add_book_frame)

        menu_main_add_book['state'] = tk.DISABLED
        add_acc_button['state'] = tk.DISABLED
        add_stud_button['state'] = tk.DISABLED
        add_stud_acc_button['state'] = tk.DISABLED
        iss_ret_book_button['state'] = tk.DISABLED
        chart_button['state'] = tk.DISABLED

        def add():
            local_acc_no = book_id_entry.get().strip().upper()
            local_isbn = book_isbn_entry.get().strip().upper()
            local_isbn = local_isbn.replace("-", "")
            if len(local_isbn) != 13 and not local_isbn.isnumeric():
                msg.showwarning("Error", "The ISBN must be 13 characters only.")
                on()
                return
            local_title = book_title_entry.get().strip().title()
            local_author = book_author_entry.get().strip().title()
            local_cat = cat.get()
            local_gen_sub = book_gen_sub_entry.get().strip().title()
            local_copies_tot = book_copies_tot_entry.get().strip()
            if not local_copies_tot.isnumeric():
                msg.showwarning("Error", "Please enter only a number in Total Copies")
                on()
                return
            local_copies_av = book_copies_available_entry.get().strip()
            if not local_copies_av.isnumeric():
                msg.showwarning("Error", "Please enter only a number in Copies Available")
                on()
                return

            x = addit({"Acc_no": local_acc_no, "ISBN": local_isbn, "Title": local_title, "Author": local_author,
                       "Category": local_cat, "Genre_sub": local_gen_sub, "Copies_total": local_copies_tot,
                       "Copies_available": local_copies_av}, "Book_Data")
            if x[0] is False:
                msg.showwarning("Error", "An error occurred. Details:\n{}".format(x[1]))
            else:
                msg.showinfo("Success", "The Book {} was successfully added to Book_Data".format(local_title))
            on()

        def on():
            add_book_frame.destroy()
            menu_main_add_book['state'] = tk.NORMAL
            add_acc_button['state'] = tk.NORMAL
            add_stud_button['state'] = tk.NORMAL
            add_stud_acc_button['state'] = tk.NORMAL
            iss_ret_book_button['state'] = tk.NORMAL
            chart_button['state'] = tk.NORMAL

        ok_button = tk.Button(add_book_frame, text='ADD', font=('Calibri', '16', 'bold'), bg="#d3845f", command=add,
                              activebackground="#e89611")
        ok_button.place(anchor=tk.SE, relx=1, rely=1)
        popup(root, zeta, ok_button)

        cancel_button = tk.Button(add_book_frame, text='CANCEL', font=('Calibri', '16', 'bold'), bg="#d3845f",
                                  command=on,
                                  activebackground="#e89611")
        cancel_button.place(anchor=tk.SE, relx=0.94, rely=1)
        popup(root, zeta, cancel_button)

        book_id_label = tk.Label(add_book_frame, text='Accession No. :', width=12, font=('Times', '20', 'bold'),
                                 bg="#d3845f")
        book_id_label.place(anchor=tk.NW, relx=0.0858, rely=0.11)
        popup(root, zeta, book_id_label)

        book_id_entry = tk.Entry(add_book_frame, exportselection=0, relief='ridge', bd=3, font=('Calibri', '20'),
                                 width=33, bg="#dfa68b")
        book_id_entry.place(anchor=tk.NW, relx=0.26, rely=0.11)
        popup(root, zeta, book_id_entry)
        book_id_entry.focus_set()

        book_isbn_label = tk.Label(add_book_frame, text='13 Digit ISBN :', width=14, font=('Times', '20', 'bold'),
                                   bg="#d3845f")
        book_isbn_label.place(anchor=tk.NW, relx=0.072, rely=0.18)
        popup(root, zeta, book_isbn_label)

        book_isbn_entry = tk.Entry(add_book_frame, exportselection=0, relief='ridge', bd=3, font=('Calibri', '20'),
                                   width=33, bg="#dfa68b")
        book_isbn_entry.place(anchor=tk.NW, relx=0.26, rely=0.18)
        popup(root, zeta, book_isbn_entry)

        book_title_label = tk.Label(add_book_frame, text='Title :', width=12, font=('Times', '20', 'bold'),
                                    bg="#d3845f")
        book_title_label.place(anchor=tk.NW, relx=0.132, rely=0.25)
        popup(root, zeta, book_title_label)

        book_title_entry = tk.Entry(add_book_frame, exportselection=0, relief='ridge', bd=3, font=('Calibri', '20'),
                                    width=33, bg="#dfa68b")
        book_title_entry.place(anchor=tk.NW, relx=0.26, rely=0.25)
        popup(root, zeta, book_title_entry)

        book_author_label = tk.Label(add_book_frame, text='Author :', width=12, font=('Times', '20', 'bold'),
                                     bg="#d3845f")
        book_author_label.place(anchor=tk.NW, relx=0.119, rely=0.32)
        popup(root, zeta, book_author_label)

        book_author_entry = tk.Entry(add_book_frame, exportselection=0, relief='ridge', bd=3, font=('Calibri', '20'),
                                     width=33, bg="#dfa68b")
        book_author_entry.place(anchor=tk.NW, relx=0.26, rely=0.32)
        popup(root, zeta, book_author_entry)

        book_cat_label = tk.Label(add_book_frame, text='Category :', width=12, font=('Times', '20', 'bold'),
                                  bg="#d3845f")
        book_cat_label.place(anchor=tk.NW, relx=0.109, rely=0.39)
        popup(root, zeta, book_cat_label)

        cat = tk.StringVar()
        cat.set("Curriculum")
        cat_opt = tk.OptionMenu(add_book_frame, cat, *["Curriculum", "Novel", "Comic", "Encyclopedia"])
        cat_opt.config(font=('Calibri', '19'), bg="#dfa68b", activebackground="#dfa68b", width=12)
        cat_opt['menu'].config(font=('Calibri', '17'), bg="#d3845f", activebackground="black")
        cat_opt.place(anchor=tk.NW, relx=0.26, rely=0.39)
        popup(root, zeta, cat_opt)

        book_gen_sub_label = tk.Label(add_book_frame, text='Genre/Subject :', width=12, font=('Times', '20', 'bold'),
                                      bg="#d3845f")
        book_gen_sub_label.place(anchor=tk.NW, relx=0.083, rely=0.46)
        popup(root, zeta, book_gen_sub_label)

        book_gen_sub_entry = tk.Entry(add_book_frame, exportselection=0, relief='ridge', bd=2.7, font=('Calibri', '20'),
                                      width=33, bg="#dfa68b")
        book_gen_sub_entry.place(anchor=tk.NW, relx=0.26, rely=0.465)
        popup(root, zeta, book_gen_sub_entry)

        book_copies_tot_label = tk.Label(add_book_frame, text='Total Copies :', width=12, font=('Times', '20', 'bold'),
                                         bg="#d3845f")
        book_copies_tot_label.place(anchor=tk.NW, relx=0.0885, rely=0.53)
        popup(root, zeta, book_copies_tot_label)

        book_copies_tot_entry = tk.Entry(add_book_frame, exportselection=0, relief='ridge', bd=3,
                                         font=('Calibri', '20'), width=33, bg="#dfa68b")
        book_copies_tot_entry.place(anchor=tk.NW, relx=0.26, rely=0.535)
        popup(root, zeta, book_copies_tot_entry)

        book_copies_available_label = tk.Label(add_book_frame, text='Copies Available :', width=14,
                                               font=('Times', '20', 'bold'), bg="#d3845f")
        book_copies_available_label.place(anchor=tk.NW, relx=0.0532, rely=0.605)
        popup(root, zeta, book_copies_available_label)

        book_copies_available_entry = tk.Entry(add_book_frame, exportselection=0, relief='ridge', bd=3,
                                               font=('Calibri', '20'), width=33, bg="#dfa68b")
        book_copies_available_entry.place(anchor=tk.NW, relx=0.26, rely=0.605)
        popup(root, zeta, book_copies_available_entry)

    global pic4

    pic4 = ImageTk.PhotoImage(Image.open("Picture4.png"))
    menu_main_add_book = tk.Button(zeta, image=pic4, width=275, height=64,
                                   command=add_book, activebackground="#e89611", cursor="plus")
    menu_main_add_book.place(anchor=tk.E, relx=1, rely=0.359)
    popup(root, zeta, menu_main_add_book)

    def iss_ret_book():
        add4 = tk.LabelFrame(zeta, text=r"Issue\Return Book", bd=5,
                             font=('Times', '24', 'bold', 'italic'),
                             bg="#d3845f", width=zeta.winfo_screenwidth() - 750, height=zeta.winfo_screenheight() - 450)
        add4.place(anchor=tk.N, relx=0.52, rely=0.2)
        popup(root, zeta, add4)

        menu_main_add_book['state'] = tk.DISABLED
        add_acc_button['state'] = tk.DISABLED
        add_stud_button['state'] = tk.DISABLED
        add_stud_acc_button['state'] = tk.DISABLED
        iss_ret_book_button['state'] = tk.DISABLED
        chart_button['state'] = tk.DISABLED

        def on():
            add4.destroy()
            menu_main_add_book['state'] = tk.NORMAL
            add_acc_button['state'] = tk.NORMAL
            add_stud_button['state'] = tk.NORMAL
            add_stud_acc_button['state'] = tk.NORMAL
            iss_ret_book_button['state'] = tk.NORMAL
            chart_button['state'] = tk.NORMAL

        def refresh():
            local_acc_no = book_id_entry.get().strip()

            add5 = tk.LabelFrame(add4, text="Book Details", bd=5,
                                 font=('Times', '24', 'bold', 'italic'),
                                 bg="#d3845f", width=zeta.winfo_screenwidth() - 1200,
                                 height=zeta.winfo_screenheight() - 750)
            add5.place(anchor=tk.NW, relx=0.17, rely=0.22)
            popup(root, zeta, add5)

            issue_button = tk.Button(add5, text='ISSUE', font=('Calibri', '16', 'bold'), bg="#d3845f",
                                     activebackground="#e89611", state=tk.DISABLED,
                                     command=lambda: iss(zeta, local_acc_no, h, k))
            issue_button.place(anchor=tk.SE, relx=0.98, rely=1)
            popup(root, zeta, issue_button)

            return_button = tk.Button(add5, text='RETURN', font=('Calibri', '16', 'bold'), bg="#d3845f",
                                      activebackground="#e89611", state=tk.DISABLED,
                                      command=lambda: ret(zeta, local_acc_no, h, k))
            return_button.place(anchor=tk.SE, relx=0.14, rely=1)
            popup(root, zeta, return_button)

            got_title_label = tk.Label(add5, font=('Times', '14', 'bold'),
                                       bg="#d3845f", wraplength=300)
            got_title_label.place(anchor=tk.N, relx=0.51, rely=0.1)
            popup(root, zeta, got_title_label)

            got_author_label = tk.Label(add5, font=('Times', '14', 'bold'),
                                        bg="#d3845f", wraplength=300)
            got_author_label.place(anchor=tk.N, relx=0.51, rely=0.34)
            popup(root, zeta, got_author_label)

            book_copies_avai_label = tk.Label(add5, text='Available Copies :', font=('Times', '20', 'bold'),
                                              bg="#d3845f", justify="right")
            book_copies_avai_label.place(anchor=tk.N, relx=0.2, rely=0.5)
            popup(root, zeta, book_copies_avai_label)

            local_title = dialit("Book_Data", "Title", "Acc_no", local_acc_no)
            local_author = dialit("Book_Data", "Author", "Acc_no", local_acc_no)
            local_avai = dialit("Book_Data", "Copies_available", "Acc_no", local_acc_no)

            if local_title[0] is True:
                try:
                    h = local_title[1][0][0]
                    got_title_label.config(text=h)
                    got_author_label.config(text=local_author[1][0][0])
                    k = int(local_avai[1][0][0])
                    book_copies_avai_label.config(text="Available Copies : {}".format(k))
                    if k >= 1:
                        issue_button['state'] = tk.NORMAL
                    return_button['state'] = tk.NORMAL
                except IndexError:
                    got_title_label.config(text="No Book found")
                    got_author_label.config(text="-")
            else:
                got_title_label.config(text="No Book found")
                got_author_label.config(text="-")

            book_title_label = tk.Label(add5, text='Title :', font=('Times', '20', 'bold'),
                                        bg="#d3845f", justify="right")
            book_title_label.place(anchor=tk.N, relx=0.12, rely=0.1)
            popup(root, zeta, book_title_label)

            book_author_label = tk.Label(add5, text='Author :', font=('Times', '20', 'bold'),
                                         bg="#d3845f", justify="right")
            book_author_label.place(anchor=tk.N, relx=0.12, rely=0.32)
            popup(root, zeta, book_author_label)

        cancel_button = tk.Button(add4, text='CANCEL', font=('Calibri', '16', 'bold'), bg="#d3845f",
                                  command=on, activebackground="#e89611")
        cancel_button.place(anchor=tk.SE, relx=0.98, rely=1)
        popup(root, zeta, cancel_button)

        book_id_label = tk.Label(add4, text='Enter Accession No. :', font=('Times', '22', 'bold'),
                                 bg="#d3845f")
        book_id_label.place(anchor=tk.NW, relx=0.08, rely=0.11)
        popup(root, zeta, book_id_label)

        book_id_entry = tk.Entry(add4, exportselection=0, relief='ridge', bd=3, font=('Calibri', '20'),
                                 width=33, bg="#dfa68b")
        book_id_entry.place(anchor=tk.NW, relx=0.32, rely=0.11)
        popup(root, zeta, book_id_entry)
        book_id_entry.focus_set()

        refresh_button = tk.Button(add4, text='Refresh', font=('Calibri', '16', 'bold'), bg="#d3845f",
                                   command=refresh, activebackground="#e89611", cursor="exchange")
        refresh_button.place(anchor=tk.NW, relx=0.75, rely=0.105)
        popup(root, zeta, refresh_button)

    global pic2

    pic2 = ImageTk.PhotoImage(Image.open("Picture2.png"))
    iss_ret_book_button = tk.Button(zeta, image=pic2, cursor='plus', width=275, height=75,
                                    command=iss_ret_book,
                                    relief='raised')
    iss_ret_book_button.place(anchor=tk.E, relx=1, rely=0.645)
    popup(root, zeta, iss_ret_book_button)

    def charts():
        add6 = tk.LabelFrame(zeta, text=r"Matplotlib Charts", bd=5,
                             font=('Times', '24', 'bold', 'italic'),
                             bg="#d3845f", width=zeta.winfo_screenwidth() - 750, height=zeta.winfo_screenheight() - 450)
        add6.place(anchor=tk.N, relx=0.52, rely=0.2)
        popup(root, zeta, add6)

        menu_main_add_book['state'] = tk.DISABLED
        add_acc_button['state'] = tk.DISABLED
        add_stud_button['state'] = tk.DISABLED
        add_stud_acc_button['state'] = tk.DISABLED
        iss_ret_book_button['state'] = tk.DISABLED
        chart_button['state'] = tk.DISABLED

        def draw():
            f = Figure(figsize=(6, 4), dpi=100)
            f.set_facecolor("#dfa68b")
            a = f.add_subplot(111)
            s = 0

            if plot.get() == "PieChart of Books by Author":
                s = 1
                g = run("SELECT AUTHOR, COUNT(*) FROM BOOK_DATA GROUP BY AUTHOR")[1]
                auth = []
                count = []
                for x in g:
                    auth.append(x[0])
                    count.append(x[1])
                a.pie(count, labels=auth, autopct='%.2f%%', shadow=True)
            elif plot.get() == "Category Wise BarChart":
                s = 1
                g = run("SELECT CATEGORY, COUNT(*) FROM BOOK_DATA GROUP BY CATEGORY")[1]
                categ = []
                count = []
                for x in g:
                    categ.append(x[0])
                    count.append(x[1])
                a.bar(range(1, len(categ)+1, 1), height=count)
                a.set_xticks(range(1, len(categ)+1, 1))
                a.set_xticklabels(categ)
                a.set_xlabel("Categories")
                a.set_ylabel("No. of Books -->")
                a.set_yticks(range(0, max(count)+1, 1))
            elif plot.get() == "Books issued currently per class":
                s = 1
                g1 = run("SELECT * FROM CUR_ISSUES")[1]
                g2 = run("SELECT ADM_NO, CLASS_SEC FROM STUDENT_DETAILS")[1]

                dictionary = {}

                for xeta in g1:
                    for yotta in g2:
                        if xeta[0] == yotta[0]:
                            if yotta[1] in dictionary.keys():
                                dictionary[yotta[1]] += 1
                            else:
                                dictionary[yotta[1]] = 1

                local_class_sec = list(dictionary.keys())
                local_count = list(dictionary.values())

                a.bar(range(1, len(local_class_sec)+1, 1), height=local_count)
                a.set_xticks(range(1, len(local_class_sec)+1, 1))
                a.set_xticklabels(local_class_sec)
                a.set_xlabel("Classes and Section")
                a.set_ylabel("No. of Books issued -->")
                try:
                    a.set_yticks(range(0, max(local_count)+1, 1))
                except ValueError:
                    pass
            elif plot.get() == "No. of Students in each class":
                s = 1
                g = run("SELECT CLASS_SEC, COUNT(*) FROM STUDENT_DETAILS GROUP BY CLASS_SEC")[1]
                categ = []
                count = []
                for x in g:
                    categ.append(x[0])
                    count.append(x[1])
                a.bar(range(1, len(categ) + 1, 1), height=count)
                a.set_xticks(range(1, len(categ) + 1, 1))
                a.set_xticklabels(categ)
                a.set_xlabel("Class & Sec")
                a.set_ylabel("No. of Students -->")
                a.set_yticks(range(0, max(count) + 1, 1))
            elif plot.get() == "No. of Birthdays in each Month":
                s = 1
                g = run("SELECT MONTHNAME(DOB), COUNT(*) FROM STUDENT_DETAILS GROUP BY MONTHNAME(DOB) ORDER BY MONTH(DOB)")[1]
                categ = []
                count = []
                for x in g:
                    categ.append(x[0])
                    count.append(x[1])
                a.bar(range(1, len(categ) + 1, 1), height=count)
                a.set_xticks(range(1, len(categ) + 1, 1))
                a.set_xticklabels(categ)
                a.set_xlabel("Month -->")
                a.set_ylabel("No. of Birthdays -->")
                a.set_yticks(range(0, max(count) + 1, 1))

            if s != 0:
                canvas = FigureCanvasTkAgg(f, master=add6)
                canvas.draw()
                cc = canvas.get_tk_widget()
                cc.place(anchor=tk.NW, relx=0.24, rely=0.2)

        def on():
            add6.destroy()
            menu_main_add_book['state'] = tk.NORMAL
            add_acc_button['state'] = tk.NORMAL
            add_stud_button['state'] = tk.NORMAL
            add_stud_acc_button['state'] = tk.NORMAL
            iss_ret_book_button['state'] = tk.NORMAL
            chart_button['state'] = tk.NORMAL

        cancel_button = tk.Button(add6, text='BACK', font=('Calibri', '16', 'bold'), bg="#d3845f",
                                  command=on, activebackground="#e89611")
        cancel_button.place(anchor=tk.SE, relx=0.98, rely=1)
        popup(root, zeta, cancel_button)

        plot_label = tk.Label(add6, text='Draw Plot of :', font=('Times', '20', 'bold'), bg="#d3845f")
        plot_label.place(anchor=tk.NW, relx=0.08, rely=0.1)
        popup(root, zeta, plot_label)

        plot = tk.StringVar()
        plot_opt = tk.OptionMenu(add6, plot, *["PieChart of Books by Author", "Category Wise BarChart",
                                               "Books issued currently per class", "No. of Students in each class",
                                               "No. of Birthdays in each Month"])
        plot_opt.config(font=('Calibri', '20'), bg="#dfa68b", activebackground="#dfa68b", width=32)
        plot_opt['menu'].config(font=('Calibri', '17'), bg="#d3845f", activebackground="black")
        plot_opt.place(anchor=tk.NW, relx=0.24, rely=0.09)
        popup(root, zeta, plot_opt)

        draw_button = tk.Button(add6, text='DRAW', font=('Calibri', '16', 'bold'), bg="#d3845f",
                                command=draw,
                                activebackground="#e89611")
        draw_button.place(anchor=tk.SE, relx=0.75, rely=0.17)
        popup(root, zeta, draw_button)

    global pic3

    pic3 = ImageTk.PhotoImage(Image.open("Picture3.png"))
    chart_button = tk.Button(zeta, image=pic3, cursor='plus', width=70, height=225,
                             command=charts, relief='raised')
    chart_button.place(anchor=tk.W, relx=0, rely=0.5)
    popup(root, zeta, chart_button)

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

    clock_label = tk.Label(zeta, text='CLOCK', bg='black', fg='white', font=('Arial', '18', 'bold'), cursor='star')
    clock_label.place(anchor=tk.SE, relx=1, rely=1)
    clock()
    popup(root, zeta, clock_label)
    zeta.mainloop()


def popup(parent: tk.Tk, child: tk.Tk or tk.Toplevel, widget):
    def rules():
        msg.showinfo(title="Rules & Permissions for User Addition",
                     message="----Rules----\n1. The Usernames & Passwords are case sensitive\n"
                             "2. The Username once taken can never be repeated, regardless of the Account type\n"
                             "3. Both the passwords must match\n"
                             "----Permissions----\n"
                             "Librarians aren't bound by permissions")

    def stud_rules():
        msg.showinfo("Rules for Student Details Addition",
                     "----Rules----\n1. All the fields are compulsory")

    def version():
        msg.showinfo(title="Version", message="This is a project in development\n"
                                              "But you can consider the version as\n"
                                              "___Version 2021.0.1___")

    def kill():
        if msg.askyesno("Exit?", "Are you sure you want to exit?"):
            child.destroy()
            parent.destroy()
        else:
            menu.grab_release()

    def logout():
        if msg.askyesno(title="Log out?", message="Are you sure you want to log out?"):
            parent.deiconify()
            child.destroy()
        else:
            menu.grab_release()

    def copyrt():
        msg.showinfo(title='Copyrighted Materials Information', message="The background you are seeing\n"
                                                                        "has been taken from\n"
                                                                        "https://wallpaperaccess.com\n"
                                                                        "WallpaperAccess ©2021\n"
                                                                        "Wallpapers are for personal use only.\n\n\n"
                                                                        "The image used for Student Profile\n"
                                                                        "has been taken via Pinterest\n"
                                                                        "from https://iconfinder.com\n"
                                                                        "©2020 Iconfinder, ApS")

    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Rules & Permissions for User Addition", command=rules)
    menu.add_command(label="Rules for Student Details Addition", command=stud_rules)
    menu.add_separator()
    menu.add_command(label='Copyright Protected Resources', command=copyrt)
    menu.add_command(label="Version", command=version)
    menu.add_separator()
    menu.add_command(label="Log Out", command=logout)
    menu.add_command(label='Exit', command=kill)

    def do_popup(event):
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    widget.bind("<Button-3>", do_popup)
