import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import psycopg2


# Функция для добавления предприятия
def add_enterprise():
    try:
        if root_entry.get() == '':
            cursor = connection.cursor()
            query = "INSERT INTO Enterprises (Name, IdMainEnterprise, IdActivityType) VALUES (%s, %s, %s);"
            cursor.execute(query, (name_entry.get(), '0', active_entry.get()))
            connection.commit()
            messagebox.showinfo("Data inserted successfully.")
        else:
            cursor = connection.cursor()
            query = "INSERT INTO Enterprises (Name, IdMainEnterprise, IdActivityType) VALUES (%s, %s, %s);"
            cursor.execute(query, (name_entry.get(), root_entry.get(), active_entry.get()))
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
    tree = ttk.Treeview(window, columns=("ID", "Name", "Active", "Root"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Active", text="Active")
    tree.heading("Root", text="Root")
    try:
        cursor = connection.cursor()
        query = """
            SELECT * FROM Enterprises;
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
            VALUES (%s);
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
            SELECT * FROM ActivityType;
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


def insert_enterprise_contact():
    try:
        cursor = connection.cursor()
        print(finish_entry_con.get())

        #   Если номер уже был привязан к конкретной организации, то он добавит дату окончания поддержки номера

        # Если finish_date не указан, используем текущую дату
        if finish_entry_con.get() == '':
            finish_date = datetime.now().date()
            # Обновляем записи с предыдущим номером телефона, чтобы указать их недействительность
            update_query = "UPDATE EnterpriseContacts SET FinishDate = %s WHERE EnterpriseId = %s AND Phone = %s AND FinishDate IS NULL;"
            cursor.execute(update_query, (finish_date, enterprise_entry_con.get(), number_entry_con.get()))

            # Вставляем новую запись с новым номером телефона
            insert_query = "INSERT INTO EnterpriseContacts (EnterpriseId, Phone, StartDate, FinishDate) VALUES (%s, %s, %s, NULL);"
            cursor.execute(insert_query, (enterprise_entry_con.get(), number_entry_con.get(), start_entry_con.get()))
        else:
            finish_date = finish_entry_con.get()
            # Обновляем записи с предыдущим номером телефона, чтобы указать их недействительность
            update_query = "UPDATE EnterpriseContacts SET FinishDate = %s WHERE EnterpriseId = %s AND Phone = %s AND FinishDate IS NULL;"
            cursor.execute(update_query, (finish_date, enterprise_entry_con.get(), number_entry_con.get()))

            # Вставляем новую запись с новым номером телефона
            insert_query = "INSERT INTO EnterpriseContacts (EnterpriseId, Phone, StartDate, FinishDate) VALUES (%s, %s, %s, %s);"
            cursor.execute(insert_query,
                           (enterprise_entry_con.get(), number_entry_con.get(), start_entry_con.get(), finish_date))

        connection.commit()
        messagebox.showinfo("Data inserted successfully.")
    except psycopg2.Error as e:
        messagebox.showinfo("Error inserting data into EnterpriseContacts table:", e)


def insert_enterprise_location():
    try:
        cursor = connection.cursor()
        if finish_entry_loc.get() == '':
            # НЕ ЗАБЫТЬ либо сделать так чтобы при повторном вводе просто закрывался адресс, либо сделать меню для удаления адреса
            finish_date = datetime.now().date()
            # Обновляем записи с предыдущим номером телефона, чтобы указать их недействительность
            update_query = "UPDATE EnterpriseLocations SET FinishDate = %s WHERE EnterpriseId = %s AND Address = %s AND FinishDate IS NULL;"
            cursor.execute(update_query, (finish_date, enterprise_entry_loc.get(), name_entry_loc.get()))

            # Вставляем новую запись с новым номером телефона
            insert_query = "INSERT INTO EnterpriseLocations (EnterpriseId, Address, StartDate, FinishDate) VALUES (%s, %s, %s, NULL);"
            cursor.execute(insert_query, (enterprise_entry_loc.get(), name_entry_loc.get(), start_entry_loc.get()))
        else:
            finish_date = finish_entry_con.get()
            # Обновляем записи с предыдущим номером телефона, чтобы указать их недействительность
            update_query = "UPDATE EnterpriseLocations SET FinishDate = %s WHERE EnterpriseId = %s AND Address = %s AND FinishDate IS NULL;"
            cursor.execute(update_query, (finish_date, enterprise_entry_loc.get(), name_entry_loc.get()))

            # Вставляем новую запись с новым номером телефона
            insert_query = "INSERT INTO EnterpriseLocations (EnterpriseId, Address, StartDate, FinishDate) VALUES (%s, %s, %s, %s);"
            cursor.execute(insert_query,
                           (enterprise_entry_loc.get(), name_entry_loc.get(), start_entry_loc.get(), finish_date))

        connection.commit()
        messagebox.showinfo("Data inserted successfully.")
        print(finish_entry_con.get())

        #   Если номер уже был привязан к конкретной организации, то он добавит дату окончания поддержки номера

        # Если finish_date не указан, используем текущую дату

    except psycopg2.Error as e:
        messagebox.showinfo("Error inserting data into EnterpriseLocations table:", e)


def insert_enterprise_email():
    try:
        cursor = connection.cursor()
        if finish_entry_email.get() == '':
            # НЕ ЗАБЫТЬ либо сделать так чтобы при повторном вводе просто закрывался адресс, либо сделать меню для удаления адреса
            finish_date = datetime.now().date()
            # Обновляем записи с предыдущим номером телефона, чтобы указать их недействительность
            update_query = "UPDATE EnterpriseEmails SET FinishDate = %s WHERE EnterpriseId = %s AND Email = %s AND FinishDate IS NULL;"
            cursor.execute(update_query, (finish_date, enterprise_entry_email.get(), name_entry_email.get()))

            # Вставляем новую запись с новым номером телефона
            insert_query = "INSERT INTO EnterpriseEmails (EnterpriseId, Email, StartDate, FinishDate) VALUES (%s, %s, %s, NULL);"
            cursor.execute(insert_query,
                           (enterprise_entry_email.get(), name_entry_email.get(), start_entry_email.get()))
        else:
            finish_date = finish_entry_con.get()
            # Обновляем записи с предыдущим номером телефона, чтобы указать их недействительность
            update_query = "UPDATE EnterpriseEmails SET FinishDate = %s WHERE EnterpriseId = %s AND Email = %s AND FinishDate IS NULL;"
            cursor.execute(update_query, (finish_date, enterprise_entry_email.get(), name_entry_email.get()))

            # Вставляем новую запись с новым номером телефона
            insert_query = "INSERT INTO EnterpriseEmails (EnterpriseId, Email, StartDate, FinishDate) VALUES (%s, %s, %s, %s);"
            cursor.execute(insert_query,
                           (enterprise_entry_email.get(), name_entry_email.get(), start_entry_email.get(), finish_date))

        connection.commit()
        messagebox.showinfo("Data inserted successfully.")
        print(finish_entry_con.get())

        #   Если номер уже был привязан к конкретной организации, то он добавит дату окончания поддержки номера

        # Если finish_date не указан, используем текущую дату

    except psycopg2.Error as e:
        messagebox.showinfo("Error inserting data into EnterpriseEmails table:", e)


def insert_manager():
    try:
        cursor = connection.cursor()
        if finish_entry_worker.get() == '':
            # НЕ ЗАБЫТЬ либо сделать так чтобы при повторном вводе просто закрывался адресс, либо сделать меню для удаления адреса
            finish_date = datetime.now().date()
            # Обновляем записи с предыдущим номером телефона, чтобы указать их недействительность
            update_query = "UPDATE EnterpriseManagers SET FinishDate = %s WHERE EnterpriseId = %s AND ManagerName = %s AND FinishDate IS NULL;"
            cursor.execute(update_query, (finish_date, enterprise_entry_worker.get(), name_entry_worker.get()))

            # Вставляем новую запись с новым номером телефона
            insert_query = "INSERT INTO EnterpriseManagers (EnterpriseId, ManagerName, Position, StartDate, FinishDate) VALUES (%s, %s,%s, %s, NULL);"
            cursor.execute(insert_query,
                           (enterprise_entry_worker.get(), name_entry_worker.get(), position_entry_worker.get(),
                            start_entry_worker.get()))
        else:
            finish_date = finish_entry_con.get()
            # Обновляем записи с предыдущим номером телефона, чтобы указать их недействительность
            update_query = "UPDATE EnterpriseManagers SET FinishDate = %s WHERE EnterpriseId = %s AND  ManagerName  = %s AND FinishDate IS NULL;"
            cursor.execute(update_query, (finish_date, enterprise_entry_worker.get(), name_entry_worker.get()))

            # Вставляем новую запись с новым номером телефона
            insert_query = "INSERT INTO EnterpriseManagers (EnterpriseId, ManagerName, Position, StartDate, FinishDate) VALUES (%s, %s, %s,%s, %s);"
            cursor.execute(insert_query,
                           (enterprise_entry_worker.get(), name_entry_worker.get(), position_entry_worker.get(),
                            start_entry_worker.get(), finish_date))

        connection.commit()
        messagebox.showinfo("Data inserted successfully.")
        print(finish_entry_con.get())

    except psycopg2.Error as e:
        messagebox.showinfo("Error inserting data into EnterpriseManagers table:", e)


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
        query = "SELECT * FROM EnterpriseContacts WHERE EnterpriseId = %s;"
        cursor.execute(query, (id_entry_con.get(),))
        rows = cursor.fetchall()
        for enterprise in rows:
            print(enterprise)
            enterprise = [str(e) for e in enterprise]
            tree.insert("", "end", values=enterprise)
        tree.pack(expand=True, fill="both")
    except psycopg2.Error as e:
        messagebox.showinfo("Error fetching contacts:", e)


def get_enterprise_locations():
    try:
        window = tk.Toplevel(root)
        window.title("Addresses")

        # Создаем виджет Treeview
        tree = ttk.Treeview(window, columns=("ID", "EnterpriseId", "Address", "StartDate", "FinishDate"),
                            show="headings")
        tree.heading("ID", text="ID")
        tree.heading("EnterpriseId", text="EnterpriseId")
        tree.heading("Address", text="Address")
        tree.heading("StartDate", text="StartDate")
        tree.heading("FinishDate", text="FinishDate")

        cursor = connection.cursor()
        query = "SELECT * FROM EnterpriseLocations WHERE EnterpriseId = %s;"
        cursor.execute(query, (id_entry_loc.get(),))
        rows = cursor.fetchall()
        for enterprise in rows:
            print(enterprise)
            enterprise = [str(e) for e in enterprise]
            tree.insert("", "end", values=enterprise)
        tree.pack(expand=True, fill="both")
    except psycopg2.Error as e:
        messagebox.showinfo("Error fetching locations:", e)


def get_enterprise_emails():
    try:
        window = tk.Toplevel(root)
        window.title("Emails")

        # Создаем виджет Treeview
        tree = ttk.Treeview(window, columns=("ID", "EnterpriseId", "Email", "StartDate", "FinishDate"),
                            show="headings")
        tree.heading("ID", text="ID")
        tree.heading("EnterpriseId", text="EnterpriseId")
        tree.heading("Email", text="Email")
        tree.heading("StartDate", text="StartDate")
        tree.heading("FinishDate", text="FinishDate")

        cursor = connection.cursor()
        query = "SELECT * FROM  EnterpriseEmails WHERE EnterpriseId = %s;"
        cursor.execute(query, (id_entry_email.get(),))
        rows = cursor.fetchall()
        for enterprise in rows:
            print(enterprise)
            enterprise = [str(e) for e in enterprise]
            tree.insert("", "end", values=enterprise)
        tree.pack(expand=True, fill="both")
    except psycopg2.Error as e:
        messagebox.showinfo("Error fetching locations:", e)


def select_enterprise_contacts_by_date():
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
        if finish_entry_z1.get() == '':
            finish_date = datetime.now().date()
        else:
            finish_date = datetime.strptime(finish_entry_z1.get(), "%d.%m.%Y")
        query = "SELECT * FROM EnterpriseContacts WHERE EnterpriseId = %s AND (StartDate >= %s AND StartDate <= %s ) OR (FinishDate >= %s AND FinishDate <= %s );"
        cursor.execute(query, (id_entry_z1.get(), datetime.strptime(start_entry_z1.get(), "%d.%m.%Y"),
                               finish_date, datetime.strptime(start_entry_z1.get(), "%d.%m.%Y"),
                               finish_date))
        rows = cursor.fetchall()
        for enterprise in rows:
            print(enterprise)
            enterprise = [str(e) for e in enterprise]
            tree.insert("", "end", values=enterprise)
        tree.pack(expand=True, fill="both")
    except psycopg2.Error as e:
        messagebox.showinfo("Error fetching contacts:", e)


def count_enterprises_without_email():
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM Enterprises LEFT JOIN EnterpriseEmails ON Enterprises.Id = EnterpriseEmails.EnterpriseId WHERE (StartDate <= %s AND (FinishDate IS NULL OR FinishDate >= %s)) AND (Email IS NULL OR StartDate < %s)"
        cursor.execute(query, (
        datetime.strptime(date_entry_email.get(), "%d.%m.%Y"), datetime.strptime(date_entry_email.get(), "%d.%m.%Y"),
        datetime.strptime(date_entry_email.get(), "%d.%m.%Y")))
        count = cursor.fetchone()[0]
        print(count)
        messagebox.showinfo("Count", count)
    except psycopg2.Error as e:
        messagebox.showinfo("Error counting enterprises without email:", e)


def select_enterprise_with_most_manager_changes():
    try:
        if finish_entry_lead.get() == '':
            finish_date = datetime.now().date()
        else:
            finish_date = datetime.strptime(finish_entry_lead.get(), "%d.%m.%Y")
        cursor = connection.cursor()
        query = "SELECT EnterpriseId FROM (SELECT EnterpriseId, COUNT(*) AS manager_changes FROM EnterpriseManagers WHERE (StartDate >= %s AND StartDate <= %s) OR (FinishDate >= %s AND FinishDate <= %s) GROUP BY EnterpriseId ORDER BY manager_changes DESC LIMIT 1) AS max_changes"
        cursor.execute(query, (datetime.strptime(start_entry_lead.get(), "%d.%m.%Y"),
                               finish_date, datetime.strptime(start_entry_lead.get(), "%d.%m.%Y"),
                               finish_date))
        count = cursor.fetchone()[0]
        print(count)
        messagebox.showinfo("Count", count)
    except psycopg2.Error as e:
        messagebox.showinfo("Error counting enterprises without email:", e)


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

label_root = tk.Label(root, text="Root(None):")
label_root.grid(row=2, column=0, padx=10, pady=5, sticky="e")
root_entry = tk.Entry(root)
root_entry.grid(row=2, column=1, padx=10, pady=5)

add_button = tk.Button(root, text="Add Enterprise", command=add_enterprise)
add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

show_button = tk.Button(root, text="Show Enterprises", command=show_enterprises)
show_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Поля для добавления активности
label_name_act = tk.Label(root, text="Name:")
label_name_act.grid(row=0, column=2, padx=10, pady=5, sticky="e")
name_entry_act = tk.Entry(root)
name_entry_act.grid(row=0, column=3, padx=10, pady=5)

add_button_act = tk.Button(root, text="Add Activity", command=insert_activity_type)
add_button_act.grid(row=2, column=3, columnspan=2, padx=10, pady=5)

show_button_act = tk.Button(root, text="Show Activity", command=select_all_activity_types)
show_button_act.grid(row=3, column=3, columnspan=2, padx=10, pady=5)

# Поля для добавления контактов
label_number_con = tk.Label(root, text="Number:")
label_number_con.grid(row=6, column=0, padx=10, pady=5, sticky="e")
number_entry_con = tk.Entry(root)
number_entry_con.grid(row=6, column=1, padx=10, pady=5)

label_enterprise_con = tk.Label(root, text="Enterprise ID:")
label_enterprise_con.grid(row=7, column=0, padx=10, pady=5, sticky="e")
enterprise_entry_con = tk.Entry(root)
enterprise_entry_con.grid(row=7, column=1, padx=10, pady=5)

label_start_con = tk.Label(root, text="Start:")
label_start_con.grid(row=8, column=0, padx=10, pady=5, sticky="e")
start_entry_con = tk.Entry(root)
start_entry_con.grid(row=8, column=1, padx=10, pady=5)

label_finish_con = tk.Label(root, text="Finish:")
label_finish_con.grid(row=9, column=0, padx=10, pady=5, sticky="e")
finish_entry_con = tk.Entry(root)
finish_entry_con.grid(row=9, column=1, padx=10, pady=5)

add_button_con = tk.Button(root, text="Add Number", command=insert_enterprise_contact)
add_button_con.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

# Поля для поиска адреса
label_number_con = tk.Label(root, text="Enterprise ID:")
label_number_con.grid(row=11, column=0, padx=10, pady=5, sticky="e")
id_entry_con = tk.Entry(root)
id_entry_con.grid(row=11, column=1, padx=10, pady=5)

show_button_con = tk.Button(root, text="Show Address by ID", command=fetch_enterprise_contacts)
show_button_con.grid(row=12, column=0, columnspan=2, padx=10, pady=5)

# Поля для добавления email
label_email_loc = tk.Label(root, text="Address:")
label_email_loc.grid(row=6, column=6, padx=10, pady=5, sticky="e")
name_entry_loc = tk.Entry(root)
name_entry_loc.grid(row=6, column=7, padx=10, pady=5)

label_enterprise_loc = tk.Label(root, text="Enterprise ID:")
label_enterprise_loc.grid(row=7, column=6, padx=10, pady=5, sticky="e")
enterprise_entry_loc = tk.Entry(root)
enterprise_entry_loc.grid(row=7, column=7, padx=10, pady=5)

label_start_loc = tk.Label(root, text="Start:")
label_start_loc.grid(row=8, column=6, padx=10, pady=5, sticky="e")
start_entry_loc = tk.Entry(root)
start_entry_loc.grid(row=8, column=7, padx=10, pady=5)

label_finish_loc = tk.Label(root, text="Finish:")
label_finish_loc.grid(row=9, column=6, padx=10, pady=5, sticky="e")
finish_entry_loc = tk.Entry(root)
finish_entry_loc.grid(row=9, column=7, padx=10, pady=5)

add_button_loc = tk.Button(root, text="Add Address", command=insert_enterprise_location)
add_button_loc.grid(row=10, column=6, columnspan=2, padx=10, pady=5)

# Поля для поиска адреса
label_number_loc = tk.Label(root, text="Enterprise ID:")
label_number_loc.grid(row=11, column=6, padx=10, pady=5, sticky="e")
id_entry_loc = tk.Entry(root)
id_entry_loc.grid(row=11, column=7, padx=10, pady=5)

show_button_email = tk.Button(root, text="Show Addresses by ID", command=get_enterprise_locations)
show_button_email.grid(row=12, column=6, columnspan=2, padx=10, pady=5)

# Поля для добавления email
label_email_email = tk.Label(root, text="Email:")
label_email_email.grid(row=6, column=2, padx=10, pady=5, sticky="e")
name_entry_email = tk.Entry(root)
name_entry_email.grid(row=6, column=3, padx=10, pady=5)

label_enterprise_email = tk.Label(root, text="Enterprise ID:")
label_enterprise_email.grid(row=7, column=2, padx=10, pady=5, sticky="e")
enterprise_entry_email = tk.Entry(root)
enterprise_entry_email.grid(row=7, column=3, padx=10, pady=5)

label_start_email = tk.Label(root, text="Start:")
label_start_email.grid(row=8, column=2, padx=10, pady=5, sticky="e")
start_entry_email = tk.Entry(root)
start_entry_email.grid(row=8, column=3, padx=10, pady=5)

label_finish_email = tk.Label(root, text="Finish:")
label_finish_email.grid(row=9, column=2, padx=10, pady=5, sticky="e")
finish_entry_email = tk.Entry(root)
finish_entry_email.grid(row=9, column=3, padx=10, pady=5)

add_button_email = tk.Button(root, text="Add Email", command=insert_enterprise_email)
add_button_email.grid(row=10, column=2, columnspan=2, padx=10, pady=5)

# Поля для поиска локаций
label_number_email = tk.Label(root, text="Enterprise ID:")
label_number_email.grid(row=11, column=2, padx=10, pady=5, sticky="e")
id_entry_email = tk.Entry(root)
id_entry_email.grid(row=11, column=3, padx=10, pady=5)

show_button_email = tk.Button(root, text="Show Emails by ID", command=get_enterprise_emails)
show_button_email.grid(row=12, column=2, columnspan=2, padx=10, pady=5)

# Поля для добавления работников
label_worker_worker = tk.Label(root, text="Name:")
label_worker_worker.grid(row=13, column=0, padx=10, pady=5, sticky="e")
name_entry_worker = tk.Entry(root)
name_entry_worker.grid(row=13, column=1, padx=10, pady=5)

label_enterprise_worker = tk.Label(root, text="Enterprise ID:")
label_enterprise_worker.grid(row=14, column=0, padx=10, pady=5, sticky="e")
enterprise_entry_worker = tk.Entry(root)
enterprise_entry_worker.grid(row=14, column=1, padx=10, pady=5)

label_position_worker = tk.Label(root, text="Position:")
label_position_worker.grid(row=15, column=0, padx=10, pady=5, sticky="e")
position_entry_worker = tk.Entry(root)
position_entry_worker.grid(row=15, column=1, padx=10, pady=5)

label_start_worker = tk.Label(root, text="Start:")
label_start_worker.grid(row=16, column=0, padx=10, pady=5, sticky="e")
start_entry_worker = tk.Entry(root)
start_entry_worker.grid(row=16, column=1, padx=10, pady=5)

label_finish_worker = tk.Label(root, text="Finish:")
label_finish_worker.grid(row=17, column=0, padx=10, pady=5, sticky="e")
finish_entry_worker = tk.Entry(root)
finish_entry_worker.grid(row=17, column=1, padx=10, pady=5)

add_button_worker = tk.Button(root, text="Add Worker", command=insert_manager)
add_button_worker.grid(row=18, column=0, columnspan=2, padx=10, pady=5)

# Поля для поиска работников
label_number_worker = tk.Label(root, text="Enterprise ID:")
label_number_worker.grid(row=19, column=0, padx=10, pady=5, sticky="e")
id_entry_worker = tk.Entry(root)
id_entry_worker.grid(row=19, column=1, padx=10, pady=5)

show_button_worker = tk.Button(root, text="Show Workers by ID", command=get_enterprise_emails)
show_button_worker.grid(row=20, column=0, columnspan=2, padx=10, pady=5)

# Поля для поиска работников
label_number_worker = tk.Label(root, text="Enterprise ID:")
label_number_worker.grid(row=19, column=0, padx=10, pady=5, sticky="e")
id_entry_worker = tk.Entry(root)
id_entry_worker.grid(row=19, column=1, padx=10, pady=5)

show_button_worker = tk.Button(root, text="Show Workers by ID", command=get_enterprise_emails)
show_button_worker.grid(row=20, column=0, columnspan=2, padx=10, pady=5)

# Поля для поиска работников
label_number_z1 = tk.Label(root, text="Enterprise ID:")
label_number_z1.grid(row=13, column=2, padx=10, pady=5, sticky="e")
id_entry_z1 = tk.Entry(root)
id_entry_z1.grid(row=13, column=3, padx=10, pady=5)

label_start_z1 = tk.Label(root, text="Start:")
label_start_z1.grid(row=14, column=2, padx=10, pady=5, sticky="e")
start_entry_z1 = tk.Entry(root)
start_entry_z1.grid(row=14, column=3, padx=10, pady=5)

label_finish_z1 = tk.Label(root, text="Finish:")
label_finish_z1.grid(row=15, column=2, padx=10, pady=5, sticky="e")
finish_entry_z1 = tk.Entry(root)
finish_entry_z1.grid(row=15, column=3, padx=10, pady=5)

show_button_z1 = tk.Button(root, text="Show Workers by ID and date", command=select_enterprise_contacts_by_date)
show_button_z1.grid(row=16, column=2, columnspan=2, padx=10, pady=5)

label_start_email1 = tk.Label(root, text="Date:")
label_start_email1.grid(row=13, column=6, padx=10, pady=5, sticky="e")
date_entry_email = tk.Entry(root)
date_entry_email.grid(row=13, column=7, padx=10, pady=5)

show_button_email_date = tk.Button(root, text="Show Emails by ID and date", command=count_enterprises_without_email)
show_button_email_date.grid(row=14, column=6, columnspan=2, padx=10, pady=5)

label_start_lead = tk.Label(root, text="Start:")
label_start_lead.grid(row=15, column=6, padx=10, pady=5, sticky="e")
start_entry_lead = tk.Entry(root)
start_entry_lead.grid(row=15, column=7, padx=10, pady=5)

label_start_z1 = tk.Label(root, text="Finish:")
label_start_z1.grid(row=16, column=6, padx=10, pady=5, sticky="e")
finish_entry_lead = tk.Entry(root)
finish_entry_lead.grid(row=16, column=7, padx=10, pady=5)

show_button_finish_date = tk.Button(root, text="Show Name", command=select_enterprise_with_most_manager_changes)
show_button_finish_date.grid(row=17, column=6, columnspan=2, padx=10, pady=5)

# Запуск главного цикла обработки событий
root.mainloop()
