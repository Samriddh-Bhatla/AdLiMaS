from loginscreen import login
import tkinter as tk
from PIL import Image, ImageTk

kappa = tk.Tk()

kappa.resizable(0, 0)
img = ImageTk.PhotoImage(Image.open("init.jpg"))
kappa.geometry("{}x{}+{}+{}".format(img.width(), img.height(), int((kappa.winfo_screenwidth()-img.width())/2),
                                    int((kappa.winfo_screenheight()-img.height())/2)))
kappa.overrideredirect(True)

tk.Label(kappa, image=img).place(relheight=1, relwidth=1)


def main_win():
    kappa.withdraw()
    login(kappa)
    pass


kappa.after(3000, main_win)
kappa.mainloop()
