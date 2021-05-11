import tkinter as tk
from tkinter.messagebox import askyesno, showinfo, showerror
from View import WelcomeForm, ResultForm, AddNewPassword, NewRegisterForm


class NewRegister(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Register New Account")
        self.resizable(False, False)

        self.register_form = NewRegisterForm(self)
        self.register_form.pack(padx=10, pady=10)

        self.ok_btn = tk.Button(self, text="OK", width=12, borderwidth=6)
        self.ok_btn.pack(pady=(0, 10))

        self.grab_set()

    def validate_username_and_password(self, user_data):
        if not all([data != "" for data in user_data.values()]):
            showerror("Error Occurred!", "Field cannot be left empty!")
        elif user_data["password"] != user_data["password_reenter"]:
            showerror("Error Occurred!", "Passwords do not match!")
        else:
            return True

    def get_username_and_password(self):
        user_data = self.register_form.return_username_and_password()
        data_dict = {key: value for key, value in zip(["username", "password", "password_reenter"], user_data)}
        if self.validate_username_and_password(data_dict):
            return data_dict["username"], data_dict["password"]

    def register(self, add_user_to_db):
        self.ok_btn.config(command=lambda: add_user_to_db(self.get_username_and_password()))


class WelcomeWindow(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Account Overview")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.exit)

        self.add_password_window = None

        self.add_function = None

        self.menu_lane = tk.Menu(self)
        self.options_menu = tk.Menu(self.menu_lane, tearoff=0)
        self.sign_out_menu = tk.Menu(self.menu_lane, tearoff=0)

        self.options_menu.add_command(label="Add", command=self.open_add_password_window)
        self.sign_out_menu.add_command(label="Exit", command=self.exit)

        self.menu_lane.add_cascade(label="Options", menu=self.options_menu)
        self.menu_lane.add_cascade(label="Sign Out", menu=self.sign_out_menu)
        self.config(menu=self.menu_lane)


        self.welcome_label = WelcomeForm(self)
        self.welcome_label.pack(padx=10, pady=5)
        self.password_view = ResultForm(self)
        self.password_view.pack(padx=10)

        self.password_view.tree.bind("<<TreeviewSelect>>", self.enable_button)

        self.btn_frame = tk.Frame(self)
        #self.update_btn = tk.Button(self.btn_frame, text="Update", bg="#007ede", fg="#ffffff", state=tk.DISABLED,
                                    #font=("roboto slab", 8, "bold"), width=6, borderwidth=4, command=self.update_password)
        #self.update_btn.grid(row=2, column=0, pady=(5, 0), padx=5)
        self.delete_btn = tk.Button(self.btn_frame, text="Delete", bg="#db2500", fg="#ffffff", state=tk.DISABLED,
                                    font=("roboto slab", 8, "bold"), width=6, borderwidth=4, command=self.delete_password)
        self.delete_btn.grid(row=2, column=1, pady=(5, 0), padx=5)
        self.btn_frame.pack(pady=(5, 10))

    def delete_password(self, function):
        self.delete_btn.config(command=lambda: function(self.password_view.return_selected_item_values()))

    #def update_password(self):
        #pass

    def enable_button(self, event):
        #self.update_btn.config(state=tk.NORMAL)
        self.delete_btn.config(state=tk.NORMAL)

    def add_name(self, name):
        self.welcome_label.update_name(name)

    def insert_passwords_to_tree(self, passwords):
        self.password_view.empty_tree()
        for password in passwords:
            data_to_insert = password[1:3]  # Selects 'place' and 'password' from the tuple object
            self.password_view.tree.insert("", tk.END, value=data_to_insert)

    def open_add_password_window(self):
        self.add_password_window = AddNew(self)
        self.add_password_window.transient()
        self.add_password_window.add_password_to_db(self.add_function)

    def exit(self):
        if askyesno("Exit Application", "Are you sure you want to exit out of the application?"):
            self.destroy()
            self.master.deiconify()


class AddNew(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Add New Password")
        self.resizable(False, False)

        self.add_new_password_form = AddNewPassword(self)
        self.add_new_password_form.pack(padx=10, pady=10)
        self.ok_btn = tk.Button(self.add_new_password_form, text="OK", width=8, borderwidth=6, command=self.add_password_to_db)
        self.ok_btn.grid(row=2, column=0)

        self.grab_set()

    def get_place_and_password(self):
        place, password = self.add_new_password_form.return_place_and_password()
        if place and password:
            self.add_new_password_form.reset_place_and_password()
            return place, password

    def add_password_to_db(self, add_password):
        self.ok_btn.config(command=lambda: add_password(self.get_place_and_password()))