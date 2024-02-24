import tkinter as tk
from tkinter import Menu, messagebox
from FrmLogin import FormLogin
from FrmPerpustakaan import FrmPerpustakaan
from Users import Users
class Dashboard:
    def __init__(self):
        # root window
        self.root = tk.Tk()
        self.root.title('Aplikasi data perpustakaan dan peminjaman')
        self.root.geometry("900x400")
        self.__data = None
        self.__level = None

        # create a menubar
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        # create menus
        self.file_menu = Menu(self.menubar)
        self.admin_menu = Menu(self.menubar)
        self.mahasiswa_menu = Menu(self.menubar)
        self.dosen_menu = Menu(self.menubar)

        # add menu items to File menu
        self.file_menu.add_command(label='Login', command=lambda: self.new_window("Log Me In", FormLogin))
        self.file_menu.add_command(label='Exit', command=self.root.destroy)

        # add menu items to menu Admin
        self.admin_menu.add_command(label='Admin-1', command=lambda: self.new_window("FrmPerpustakaan", FrmPerpustakaan))

        # add menus to the menubar
        self.menubar.add_cascade(label="File", menu=self.file_menu)

    def new_window(self, title, _class):
        new_window = tk.Toplevel(self.root)
        new_window.title(title)
        if title == "Log Me In":
            _class(new_window, title, self.update_main_window)
        elif title == "FrmPerpustakaan":
            _class(new_window, title)

    def update_main_window(self, data):
        self.__data = data
        level = self.__data[0]
        loginvalid = self.__data[1]
        if loginvalid:
            index = self.file_menu.index('Login')
            self.file_menu.delete(index)
            self.file_menu.add_command(label='Logout', command=self.Logout)
            if level == 'admin': 
                self.menubar.add_cascade(label="Admin", menu=self.admin_menu)
                self.__level = 'Admin'
            elif level == 'mahasiswa': 
                self.menubar.add_cascade(label="Mahasiswa", menu=self.mahasiswa_menu)
                self.__level = 'Mahasiswa'
            elif level == 'dosen':
                self.menubar.add_cascade(label="Dosen", menu=self.dosen_menu)
                self.__level = 'Dosen'

    def Logout(self):
        index = self.file_menu.index('Logout')
        self.file_menu.delete(index)
        self.file_menu.add_command(label='Login', command=lambda: self.new_window("Log Me In", FormLogin))
        self.remove_all_menus()

    def remove_all_menus(self):
        index = self.menubar.index(self.__level)
        if index is not None:
            self.menubar.delete(index)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    menu_app = Dashboard()
    menu_app.run()
