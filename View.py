import tkinter as tk
from tkinter.ttk import Treeview, Style
import datetime


class MainPage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.header_label = tk.Label(self, text="Password Manager", font=("roboto slab", 20))
        self.header_label.pack(pady=20)
        self.info_label = tk.Label(self, text="If you already have an account LOGIN\nelse click on REGISTER",
                                   font=("roboto slab", 12, "italic"))
        self.info_label.pack()

        self.login_detail_frame = tk.Frame(self)
        self.login_detail_frame.pack(pady=20)
        self.username_label = tk.Label(self.login_detail_frame, text="Username:", font=("roboto slab", 14))
        self.username_label.grid(row=0, column=0, padx=5, pady=(0, 10))
        self.username_entry = tk.Entry(self.login_detail_frame, textvariable=self.username, width=25, justify=tk.CENTER)
        self.username_entry.grid(row=0, column=1)
        self.password_label = tk.Label(self.login_detail_frame, text="Password:", font=("roboto slab", 14))
        self.password_label.grid(row=1, column=0, padx=5, pady=(0, 10))
        self.password_entry = tk.Entry(self.login_detail_frame, textvariable=self.password, width=25, justify=tk.CENTER,
                                       show="*")
        self.password_entry.grid(row=1, column=1)

    def return_username_and_password(self):
        return self.username.get(), self.password.get()

    def reset_username_and_password(self):
        self.username.set("")
        self.password.set("")


class WelcomeForm(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.DATE = datetime.date.today().strftime("%d/%m/%Y")
        self.DAY = datetime.date.today().strftime("%A")

        self.header_label = tk.Label(self, font=("roboto slab", 14))
        self.header_label.grid(row=0, column=0, pady=10)
        self.time_label = tk.Label(self, font=("roboto slab", 12))
        self.time_label.grid(row=2, column=0)
        self.date_label = tk.Label(self, text=f"Today is {self.DAY} ({self.DATE})", font=("roboto slab", 10, "italic"))
        self.date_label.grid(row=1, column=0)

        self.clock()

    def clock(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.time_label.after(10, self.clock)

    def update_name(self, name):
        self.header_label.config(text="Hello {},\nwelcome to your personal password manager!".format(name))


class ResultForm(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.header_label = tk.Label(self, text="All your saved passwords:", font=("roboto slab", 12, "bold"))
        self.header_label.grid(row=0, column=0, pady=(0, 5), sticky=tk.W)

        self.scrollbar_y = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.tree = Treeview(self, columns=("Place", "Password"), yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.config(command=self.tree.yview)
        self.scrollbar_y.grid(row=1, column=1, sticky="nsew")

        self.tree.heading("Place", text="Place")
        self.tree.heading("Password", text="Password")

        self.tree.column("#0", minwidth=0, width=0)
        self.tree.column("#1", width=175)
        self.tree.column("#2", width=175)

        self.style = Style()
        # noinspection SpellCheckingInspection
        self.style.configure("Treeview", rowheight=15)
        # noinspection SpellCheckingInspection
        self.style.configure("Treeview.Heading", font=("roboto slab", 10, "bold"), foreground="#a6a6a6")

        self.tree.grid(row=1, column=0)

        self.instruction_label = tk.Label(self, text="* First select an item, then choose from below",
                                          font=("roboto slab", 8, "italic"))
        self.instruction_label.grid(row=2, column=0, sticky=tk.W)

    def insert_to_tree(self, values):
        for value in values:
            self.tree.insert("", tk.END, value=value)

    def empty_tree(self):
        if self.tree.get_children():
            self.tree.delete(*self.tree.get_children())

    def return_selected_item_values(self):
        """Returns the values of the highlighted item inside TreeView"""
        highlighted_item = self.tree.selection()
        if highlighted_item:
            return tuple(self.tree.item(highlighted_item)["values"])


class NewRegisterForm(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.password_reenter = tk.StringVar()

        self.header_label = tk.Label(self, text="Register A New Account", font=("roboto slab", 18))
        self.header_label.pack()
        self.info_label = tk.Label(self, text="Please fill out the fields below!", font=("roboto slab", 12))
        self.info_label.pack()

        self.register_frame = tk.Frame(self, padx=5, pady=10)
        self.register_frame.pack(side=tk.TOP)

        self.username_label = tk.Label(self.register_frame, text="Enter your username:",
                                       font=("roboto slab", 10, "italic"))
        self.username_label.pack()
        self.username_entry = tk.Entry(self.register_frame, textvariable=self.username, width=25)
        self.username_entry.pack(pady=(0, 15))
        self.password_label = tk.Label(self.register_frame, text="Enter your password",
                                       font=("roboto slab", 10, "italic"))
        self.password_label.pack()
        self.password_entry = tk.Entry(self.register_frame, textvariable=self.password, width=20, show="*")
        self.password_entry.pack(pady=(0, 5))
        self.password_reenter_label = tk.Label(self.register_frame, text="Confirm password:",
                                               font=("roboto slab", 10, "italic"))
        self.password_reenter_label.pack()
        self.password_reenter_entry = tk.Entry(self.register_frame, textvariable=self.password_reenter, width=20,
                                               show="*")
        self.password_reenter_entry.pack()

    def return_username_and_password(self):
        return self.username.get(), self.password.get(), self.password_reenter.get()


class AddNewPassword(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.place = tk.StringVar(value="")
        self.password = tk.StringVar(value="")

        self.header_label = tk.Label(self, text="Add New Password", font=("roboto slab", 14))
        self.header_label.grid(row=0, column=0)

        self.add_frame = tk.Frame(self)
        self.add_frame.grid(row=1, column=0, pady=15, padx=10)
        self.place_label = tk.Label(self.add_frame, text="Place:", font=("roboto slab", 10))
        self.place_label.grid(row=0, column=0, sticky=tk.W)
        self.place_entry = tk.Entry(self.add_frame, textvariable=self.place, width=25)
        self.place_entry.grid(row=0, column=1)
        self.example_label = tk.Label(self.add_frame, text="(E.g.: Facebook, Spotify, etc.)",
                                      font=("roboto slab", 8, "italic"))
        self.example_label.grid(row=1, column=1, pady=(0, 5), sticky=tk.W)
        self.password_label = tk.Label(self.add_frame, text="Password:", font=("roboto slab", 10))
        self.password_label.grid(row=2, column=0)
        self.password_entry = tk.Entry(self.add_frame, textvariable=self.password, width=25)
        self.password_entry.grid(row=2, column=1)

    def return_place_and_password(self):
        return self.place.get(), self.password.get()

    def reset_place_and_password(self):
        self.place.set("")
        self.password.set("")
