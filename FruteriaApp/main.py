import tkinter as tk
from Frontend.GUI.Auth.login import Login

if __name__ == "__main__":
    root = tk.Tk()
    login_screen = Login(root)
    root.mainloop()
