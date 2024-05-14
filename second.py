import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import psycopg2


# Функция для добавления предприятия
def add_enterprise(IdMainEnterprise=None):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO Enterprises (Name, IdMainEnterprise, IdActivityType) VALUES (%s, %s, %s)"
        cursor.execute(query, (name_entry.get(), IdMainEnterprise, active_entry.get()))
        connection.commit()
        messagebox.showinfo("Data inserted successfully.")
    except psycopg2.Error as e:
        messagebox.showinfo("Error inserting data into Enterprises table:", e)


# Функция для вывода предприятий
def show_enterprises():
    # Создаем новое окно для вывода таблицы
    window = tk.Toplevel(root)
    window.title("Enterprises")

    # Создаем виджет Treeview
    tree = ttk.Treeview(window, columns=("ID", "Name", "Active"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Active", text="Active")
    try:
        cursor = connection.cursor()
        query = """
            SELECT * FROM Enterprises
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for enterprise in rows:
            tree.insert("", "end", values=enterprise)

        # Размещаем таблицу в окне
        tree.pack(expand=True, fill="both")
    except psycopg2.Error as e:
        messagebox.showinfo("Error selecting data from Enterprises table:", e)
    # Добавляем данные в таблицу


def insert_activity_type():
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO ActivityType (Name) 
            VALUES (%s)
        """
        cursor.execute(query, (name_entry_act.get(),))
        connection.commit()
        messagebox.showinfo("Activity type data inserted successfully.")
    except psycopg2.Error as e:
        messagebox.showinfo("Error inserting activity type data:", e)


def select_all_activity_types():
    try:
        window = tk.Toplevel(root)
        window.title("Activity")

        # Создаем виджет Treeview
        tree = ttk.Treeview(window, columns=("ID", "Name"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        cursor = connection.cursor()
        query = """
            SELECT * FROM ActivityType
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for enterprise in rows:
            print(enterprise)
            tree.insert("", "end", values=enterprise)

        # Размещаем таблицу в окне
        tree.pack(expand=True, fill="both")
    except psycopg2.Error as e:
        messagebox.showinfo("Error selecting data from ActivityType table:", e)


def insert_enterprise_contact(finish_date=None):
    try:
        cursor = connection.cursor()
        print(finish_entry_con.get())

        # Если finish_date не указан, используем текущую дату
        if finish_entry_con.get() == '':
            finish_date = datetime.now().date()
            # Обновляем записи с предыдущим номером телефона, чтобы указать их недействительность
            update_query = "UPDATE EnterpriseContacts SET FinishDate = %s WHERE EnterpriseId = %s AND Phone = %s AND FinishDate IS NULL"
            cursor.execute(update_query, (finish_date, enterprise_entry_con.get(), number_entry_con.get()))

            # Вставляем новую запись с новым номером телефона
            insert_query = "INSERT INTO EnterpriseContacts (EnterpriseId, Phone, StartDate, FinishDate) VALUES (%s, %s, %s, NULL)"
            cursor.execute(insert_query, (enterprise_entry_con.get(), number_entry_con.get(), start_entry_con.get()))
        else:
            finish_date = finish_entry_con.get()
            # Обновляем записи с предыдущим номером телефона, чтобы указать их недействительность
            update_query = "UPDATE EnterpriseContacts SET FinishDate = %s WHERE EnterpriseId = %s AND Phone = %s AND FinishDate IS NULL"
            cursor.execute(update_query, (finish_date, enterprise_entry_con.get(), number_entry_con.get()))

            # Вставляем новую запись с новым номером телефона
            insert_query = "INSERT INTO EnterpriseContacts (EnterpriseId, Phone, StartDate, FinishDate) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query,
                           (enterprise_entry_con.get(), number_entry_con.get(), start_entry_con.get(), finish_date))

        connection.commit()
        messagebox.showinfo("Data inserted successfully.")
    except psycopg2.Error as e:
        messagebox.showinfo("Error inserting data into EnterpriseContacts table:", e)


def fetch_enterprise_contacts():
    """
                            Id SERIAL PRIMARY KEY,
                        EnterpriseId INTEGER,
                        Phone VARCHAR(20),
                        StartDate DATE,
                        FinishDate DATE,
                        FOREIGN KEY (EnterpriseId) REFERENCES Enterprises(Id)
    :return:
    """
    try:
        window = tk.Toplevel(root)
        window.title("Numbers")

        # Создаем виджет Treeview
        tree = ttk.Treeview(window, columns=("ID", "EnterpriseId", "Phone", "StartDate", "FinishDate"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("EnterpriseId", text="EnterpriseId")
        tree.heading("Phone", text="Phone")
        tree.heading("StartDate", text="StartDate")
        tree.heading("FinishDate", text="FinishDate")

        cursor = connection.cursor()
        query = "SELECT * FROM EnterpriseContacts WHERE EnterpriseId = %s"
        cursor.execute(query, (id_entry_con.get(),))
        rows = cursor.fetchall()
        for enterprise in rows:
            print(enterprise)
            enterprise = [str(e) for e in enterprise]
            tree.insert("", "end", values=enterprise)
        tree.pack(expand=True, fill="both")
    except psycopg2.Error as e:
        messagebox.showinfo("Error fetching contacts:", e)


# Создание главного окна
root = tk.Tk()
root.title("Enterprise Management System")

connection = psycopg2.connect(database="postgres", user="postgres", password="1234", host="127.0.0.1", port="5433")
# Поля для добавления предприятия
label_name = tk.Label(root, text="Name:")
label_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

label_active = tk.Label(root, text="Active:")
label_active.grid(row=1, column=0, padx=10, pady=5, sticky="e")
active_entry = tk.Entry(root)
active_entry.grid(row=1, column=1, padx=10, pady=5)

add_button = tk.Button(root, text="Add Enterprise", command=add_enterprise)
add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

show_button = tk.Button(root, text="Show Enterprises", command=show_enterprises)
show_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Поля для добавления активности
label_name_act = tk.Label(root, text="Name:")
label_name_act.grid(row=0, column=3, padx=10, pady=5, sticky="e")
name_entry_act = tk.Entry(root)
name_entry_act.grid(row=0, column=4, padx=10, pady=5)

add_button_act = tk.Button(root, text="Add Activity", command=insert_activity_type)
add_button_act.grid(row=2, column=3, columnspan=2, padx=10, pady=5)

show_button_act = tk.Button(root, text="Show Activity", command=select_all_activity_types)
show_button_act.grid(row=3, column=3, columnspan=2, padx=10, pady=5)

# Поля для добавления контактов
label_number_con = tk.Label(root, text="Number:")
label_number_con.grid(row=0, column=6, padx=10, pady=5, sticky="e")
number_entry_con = tk.Entry(root)
number_entry_con.grid(row=0, column=7, padx=10, pady=5)

label_enterprise_con = tk.Label(root, text="Enterprise ID:")
label_enterprise_con.grid(row=1, column=6, padx=10, pady=5, sticky="e")
enterprise_entry_con = tk.Entry(root)
enterprise_entry_con.grid(row=1, column=7, padx=10, pady=5)

label_start_con = tk.Label(root, text="Start:")
label_start_con.grid(row=2, column=6, padx=10, pady=5, sticky="e")
start_entry_con = tk.Entry(root)
start_entry_con.grid(row=2, column=7, padx=10, pady=5)

label_finish_con = tk.Label(root, text="Finish:")
label_finish_con.grid(row=3, column=6, padx=10, pady=5, sticky="e")
finish_entry_con = tk.Entry(root)
finish_entry_con.grid(row=3, column=7, padx=10, pady=5)

add_button_con = tk.Button(root, text="Add Number", command=insert_enterprise_contact)
add_button_con.grid(row=4, column=6, columnspan=2, padx=10, pady=5)

# Поля для добавления контактов
label_number_con = tk.Label(root, text="Enterprise ID:")
label_number_con.grid(row=5, column=6, padx=10, pady=5, sticky="e")
id_entry_con = tk.Entry(root)
id_entry_con.grid(row=5, column=7, padx=10, pady=5)

show_button_con = tk.Button(root, text="Show Numbers by ID", command=fetch_enterprise_contacts)
show_button_con.grid(row=6, column=6, columnspan=2, padx=10, pady=5)

root.mainloop()

# Запуск главного цикла обработки событий
root.mainloop()
