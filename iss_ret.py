import tkinter as tk
from sqlconnectionfunc import read_table_cell as r, add_table_row as addit, alter_table_cell as alt, delete_table_row as dlt
from tkinter import messagebox as msg


def iss(rt: tk.Tk or tk.Toplevel, book_id, book_name, old_avai: int):
    root = tk.Toplevel(rt)

    root.resizable(0, 0)
    root.geometry("600x150+400+400")
    root.wm_attributes('-topmost', True)

    root.title("Issue --{}".format(book_name))

    root.config(background="#D3D3D3")

    head = tk.Label(root, text="Issue {}".format(book_name), background="#D3D3D3", justify="center",  font=('Calibri', '20', 'bold'))
    head.grid(row=0, columnspan=2)

    issue_to = tk.Label(root, text="Issue to (Admission No of Student):", font=("Calibri", "14"), background="#D3D3D3")
    issue_to.grid(row=1, column=0)

    icon = tk.PhotoImage(file="icon.png")
    root.iconphoto(False, icon)

    stud_adm_no = tk.Entry(root, exportselection=0, relief='ridge', font=('Calibri', '14'), bd=3, bg="#D3D3D3")
    stud_adm_no.grid(row=1, column=1)
    stud_adm_no.focus_set()

    def call():
        c = r("Student_Details", "Adm_No", "Adm_No", stud_adm_no.get().strip())
        d = r("CUR_ISSUES", "BOOK_ISS", "ADM_NO", stud_adm_no.get().strip())
        if c[0] and d[0]:
            if d[2] == 0:
                try:
                    _ = c[2]
                    if c[2] != 0:
                        addit({"ADM_NO": stud_adm_no.get().strip(), "BOOK_ISS": book_id}, "CUR_ISSUES")
                        alt(old_avai-1, "Book_Data", "Copies_available", "Acc_no", book_id)
                        msg.showinfo("Success", "Book {} was issued to {}.".format(book_name, r("Student_Details", "Name", "Adm_No", stud_adm_no.get().strip())[1][0][0]))
                        root.destroy()
                        return
                    else:
                        msg.showwarning("Error", "The Student was not found")
                        root.destroy()
                        return
                except IndexError:
                    pass
            else:
                msg.showwarning("Error", "This child has already been issued a book.\nReturn it first.\n"
                                         "Details:\n"
                                         "{}\n{}".format(r("Student_Details", "Name", "Adm_No", stud_adm_no.get().strip())[1][0][0], r("Book_Data", "Title", "Acc_No", d[1][0][0])[1][0][0]))
                root.destroy()
                return

    conf_but = tk.Button(root, text="Confirm Issue", background="#D3D3D3", relief='raised', bd=4, command=call)
    conf_but.grid(row=2, column=1)

    cancel_but = tk.Button(root, text="Cancel", background="#D3D3D3", relief='raised', bd=4, command=root.destroy)
    cancel_but.grid(row=2, column=0)

    root.mainloop()


def ret(rt: tk.Tk or tk.Toplevel, book_id, book_name, old_avai: int):
    root = tk.Toplevel(rt)

    root.resizable(0, 0)
    root.geometry("600x150+400+400")
    root.wm_attributes('-topmost', True)

    root.title("Return --{}".format(book_name))

    root.config(background="#D3D3D3")

    head = tk.Label(root, text="Return {}".format(book_name), background="#D3D3D3", justify="center",  font=('Calibri', '20', 'bold'))
    head.grid(row=0, columnspan=2)

    issue_to = tk.Label(root, text="Return from (Admission No of Student):", font=("Calibri", "14"), background="#D3D3D3")
    issue_to.grid(row=1, column=0)

    icon = tk.PhotoImage(file="icon.png")
    root.iconphoto(False, icon)

    stud_adm_no = tk.Entry(root, exportselection=0, relief='ridge', font=('Calibri', '14'), bd=3, bg="#D3D3D3")
    stud_adm_no.grid(row=1, column=1)
    stud_adm_no.focus_set()

    def call():
        c = r("Student_Details", "Adm_No", "Adm_No", stud_adm_no.get().strip())
        d = r("CUR_ISSUES", "BOOK_ISS", "ADM_NO", stud_adm_no.get().strip())
        if c[0] and d[0]:
            if d[2] != 0:
                if r("Book_Data", "Title", "Acc_No", d[1][0][0])[1][0][0] == book_name:
                    try:
                        _ = c[2]
                        if c[2] != 0:
                            dlt(stud_adm_no.get().strip(), "CUR_ISSUES", "ADM_NO")
                            alt(old_avai+1, "Book_Data", "Copies_available", "Acc_no", book_id)
                            msg.showinfo("Success", "The book was returned.")
                            root.destroy()
                            return
                        else:
                            msg.showwarning("Error", "The Student was not found")
                            root.destroy()
                            return
                    except IndexError:
                        pass
                else:
                    msg.showerror("Error", "This child wasn't issued the book {}".format(book_name))
                    root.destroy()
                    return
            else:
                msg.showwarning("Error", "This child has not been issued a book")
                root.destroy()
                return

    conf_but = tk.Button(root, text="Confirm Return", background="#D3D3D3", relief='raised', bd=4, command=call)
    conf_but.grid(row=2, column=1)

    cancel_but = tk.Button(root, text="Cancel", background="#D3D3D3", relief='raised', bd=4, command=root.destroy)
    cancel_but.grid(row=2, column=0)

    root.mainloop()
