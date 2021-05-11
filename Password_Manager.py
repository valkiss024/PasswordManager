import tkinter as tk
from tkinter.messagebox import showerror, showinfo, askyesno
from View import MainPage
from Windows import NewRegister, WelcomeWindow
from db_handler import DataBase


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.WIDTH = 400
        self.HEIGHT = 300
        self.geometry("%sx%s+%d+%d" % (self.WIDTH, self.HEIGHT,
                                       (self.winfo_screenwidth() / 2 - self.WIDTH / 2),
                                       (self.winfo_screenheight() / 2 - self.HEIGHT / 2)))
        self.resizable(False, False)

        self.db = DataBase("password_manager.db")
        self.db.create_tables()
        self.password_data = []

        self.user_id = None

        self.welcome_frame = MainPage(self)
        self.welcome_frame.pack()
        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack()

        self.login_btn = tk.Button(self.btn_frame, text="Login", width=12, borderwidth=6, command=self.login)
        self.login_btn.grid(row=1, column=0, padx=10)
        self.register_btn = tk.Button(self.btn_frame, text="Register", width=12, borderwidth=6,
                                      command=self.register)
        self.register_btn.grid(row=1, column=1, padx=10)

    def register(self):
        self.register_window = NewRegister(self)
        self.register_window.transient()

        self.register_window.register(self.add_new_user_to_db)

    def add_new_user_to_db(self, values):
        if values:
            try:
                self.db.insert_into_user(values)
            except Exception as e:
                print(e)
                showerror("Error", "Username already exists!")
            else:
                showinfo("Info", "Registration successful!")
                self.register_window.destroy()

    def login(self):
        username = self.validate_user(self.welcome_frame.return_username_and_password())
        if username:
            self.get_passwords_from_db()
            self.welcome_frame.reset_username_and_password()
            self.withdraw()

            self.user_window = WelcomeWindow(self)
            self.user_window.add_name(username)
            self.user_window.insert_passwords_to_tree(self.password_data)
            self.user_window.add_function = self.add_new_password_to_db
            self.user_window.delete_password(self.delete_password_from_db)
        else:
            showerror("Error", "Login failed!")

    def validate_user(self, values):
        user = self.db.select_user(values)
        if user:
            self.user_id = user[0]
            username = user[1]
            return username

    def get_passwords_from_db(self):
        self.password_data = self.db.select_password(self.user_id)

    def add_new_password_to_db(self, values):
        if values:
            try:
                self.db.insert_into_collection(values, self.user_id)
            except Exception as e:
                print(e)
                showerror("Error", "Something's went wrong when adding new password!")
            else:
                self.get_passwords_from_db()
                self.user_window.insert_passwords_to_tree(self.password_data)
                showinfo("Info", "Password added successfully!")

    def delete_password_from_db(self, values):
        if values:
            if askyesno("Delete Password", "Are you sure you want to permanently delete this password?"):
                try:
                    self.db.delete_password(values, self.user_id)
                except Exception as e:
                    print(e)
                    showerror("Error", "Something's went wrong when deleting password!")
                else:
                    self.get_passwords_from_db()
                    self.user_window.insert_passwords_to_tree(self.password_data)
                    showinfo("Info", "Password has been deleted successfully!")

    """
    def update_password_in_db(self, new_values, old_values):
        place, password = old_values
        password_id = None
        for p in self.password_data:
            if place in p and password in p:
                password_id = p[0]
        try:
            self.db.update_password(new_values, password_id)
        except Exception as e:
            print(e)
            showerror("Error", "Something's went wrong when updating password!")
        else:
            self.get_passwords_from_db()
            self.user_window.insert_passwords_to_tree(self.password_data)
            showinfo("Info", "Password has been update successfully!")"""


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
