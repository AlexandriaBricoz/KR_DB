'''
-- Создание базы данных
CREATE DATABASE EnterpriseDirectory;

-- Использование базы данных
USE EnterpriseDirectory;

-- Создание таблицы для предприятий
CREATE TABLE Enterprises (
    Id VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(100),
    FOREIGN KEY (IdActivityType) REFERENCES ActivityType(IdActivityType)
);

-- Создание таблицы для контактных телефонов предприятий
CREATE TABLE EnterpriseContacts (
    EnterpriseId VARCHAR(10),
    Phone VARCHAR(20),
    StartDate DATE,
    FinishDate DATE,
    FOREIGN KEY (EnterpriseCode) REFERENCES Enterprises(Id)
);

-- Создание таблицы для электронных адресов предприятий
CREATE TABLE EnterpriseEmails (
    EnterpriseId VARCHAR(10),
    Email VARCHAR(100),
    StartDate DATE,
    FinishDate DATE,
    FOREIGN KEY (EnterpriseId) REFERENCES Enterprises(Id)
);

-- Создание таблицы для видов активности
CREATE TABLE ActivityType (
    IdActivityType VARCHAR(10),
    Name VARCHAR(100),
);

-- Создание таблицы для руководителей предприятий
CREATE TABLE EnterpriseManagers (
    ManagerId VARCHAR(10),
    ManagerName VARCHAR(100),
    Position VARCHAR(50),
    StartDate DATE,
    FinishDate DATE,
    FOREIGN KEY (ManagerId) REFERENCES Enterprises(Id)
);

-- Создание таблицы для местоположений предприятий
CREATE TABLE EnterpriseLocations (
    EnterpriseId VARCHAR(10),
    Address VARCHAR(100),
    StartDate DATE,
    FinishDate DATE,
    FOREIGN KEY (EnterpriseId) REFERENCES Enterprises(Id)
);
'''

from datetime import datetime

import psycopg2


def create_missing_tables(connection):
    try:
        cursor = connection.cursor()
        existing_tables = []

        # Получаем список существующих таблиц в базе данных
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        existing_tables = [table[0] for table in cursor.fetchall()]

        # Проверяем, какие таблицы еще не созданы и создаем их
        missing_tables = {"ActivityType", "Enterprises", "EnterpriseContacts", "EnterpriseEmails", "EnterpriseManagers",
                          "EnterpriseLocations"} - set(existing_tables)

        for table in missing_tables:
            if table == "ActivityType":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ActivityType (
                        IdActivityType SERIAL PRIMARY KEY,
                        Name VARCHAR(100)
                    );
                """)
            elif table == "Enterprises":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Enterprises (
                        Id SERIAL PRIMARY KEY,
                        Name VARCHAR(100),
                        IdActivityType INTEGER,
                        IdMainEnterprise INTEGER,
                        FOREIGN KEY (IdActivityType) REFERENCES ActivityType(IdActivityType)
                    );
                """)
            elif table == "EnterpriseContacts":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS EnterpriseContacts (
                        Id SERIAL PRIMARY KEY,
                        EnterpriseId INTEGER,
                        Phone VARCHAR(20),
                        StartDate DATE,
                        FinishDate DATE,
                        FOREIGN KEY (EnterpriseId) REFERENCES Enterprises(Id)
                    );
                """)
            elif table == "EnterpriseEmails":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS EnterpriseEmails (
                        Id SERIAL PRIMARY KEY,
                        EnterpriseId INTEGER,
                        Email VARCHAR(100),
                        StartDate DATE,
                        FinishDate DATE,
                        FOREIGN KEY (EnterpriseId) REFERENCES Enterprises(Id)
                    );
                """)
            elif table == "EnterpriseManagers":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS EnterpriseManagers (
                        ManagerId SERIAL PRIMARY KEY,
                        EnterpriseId INTEGER,
                        ManagerName VARCHAR(100),
                        Position VARCHAR(50),
                        StartDate DATE,
                        FinishDate DATE,
                        FOREIGN KEY (EnterpriseId) REFERENCES Enterprises(Id)
                    );
                """)
            elif table == "EnterpriseLocations":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS EnterpriseLocations (
                        Id SERIAL PRIMARY KEY,
                        EnterpriseId INTEGER,
                        Address VARCHAR(100),
                        StartDate DATE,
                        FinishDate DATE,
                        FOREIGN KEY (EnterpriseId) REFERENCES Enterprises(Id)
                    );
                """)

        connection.commit()
        print("Missing tables created successfully.")
    except psycopg2.Error as e:
        print("Error creating missing tables:", e)


# Пример использования:
# Установка соединения с базой данных
# connection = psycopg2.connect(database="EnterpriseDirectory", user="yourusername", password="yourpassword", host="yourhost", port="yourport")
# create_missing_tables(connection)
# connection.close()


def connect_to_database():
    try:
        connection = psycopg2.connect(
            dbname="EnterpriseDirectory",
            user="your_username",
            password="your_password",
            host="your_host",
            port="your_port"
        )
        return connection
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL database:", e)


def insert_enterprise(connection, name, activity_type_id, IdMainEnterprise=None):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO Enterprises (Name, IdMainEnterprise, IdActivityType) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, IdMainEnterprise, activity_type_id))
        connection.commit()
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print("Error inserting data into Enterprises table:", e)


def insert_enterprise_contact(connection, enterprise_id, phone, start_date, finish_date=None):
    try:
        cursor = connection.cursor()

        # Если finish_date не указан, используем текущую дату
        if finish_date is None:
            finish_date = datetime.now().date()

        # Обновляем записи с предыдущим номером телефона, чтобы указать их недействительность
        update_query = "UPDATE EnterpriseContacts SET FinishDate = %s WHERE EnterpriseId = %s AND Phone = %s AND FinishDate IS NULL"
        cursor.execute(update_query, (finish_date, enterprise_id, phone))

        # Вставляем новую запись с новым номером телефона
        insert_query = "INSERT INTO EnterpriseContacts (EnterpriseId, Phone, StartDate, FinishDate) VALUES (%s, %s, %s, NULL)"
        cursor.execute(insert_query, (enterprise_id, phone, start_date))

        connection.commit()
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print("Error inserting data into EnterpriseContacts table:", e)


def select_enterprise_contacts_by_date(connection, date):
    try:
        cursor = connection.cursor()
        query = "SELECT Phone FROM EnterpriseContacts WHERE StartDate <= %s AND (FinishDate IS NULL OR FinishDate >= %s)"
        cursor.execute(query, (date, date))
        rows = cursor.fetchall()
        phone_numbers = [row[0] for row in rows]
        return phone_numbers
    except psycopg2.Error as e:
        print("Error selecting data from EnterpriseContacts table:", e)


def count_enterprises_without_email(connection, date):
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM Enterprises LEFT JOIN EnterpriseEmails USING (EnterpriseId) WHERE (StartDate <= %s AND (FinishDate IS NULL OR FinishDate >= %s)) AND (Email IS NULL OR StartDate > %s)"
        cursor.execute(query, (date, date, date))
        count = cursor.fetchone()[0]
        return count
    except psycopg2.Error as e:
        print("Error counting enterprises without email:", e)


def insert_enterprise_email(connection, enterprise_id, email, start_date):
    try:
        cursor = connection.cursor()

        # Добавляем finish_date к предыдущей записи, если она существует
        update_query = """
            UPDATE EnterpriseEmails 
            SET FinishDate = %s 
            WHERE EnterpriseId = %s AND FinishDate IS NULL
        """
        cursor.execute(update_query, (start_date, enterprise_id))

        # Вставляем новую запись
        insert_query = """
            INSERT INTO EnterpriseEmails (EnterpriseId, Email, StartDate, FinishDate) 
            VALUES (%s, %s, %s, NULL)
        """
        cursor.execute(insert_query, (enterprise_id, email, start_date))

        connection.commit()
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print("Error inserting data into EnterpriseEmails table:", e)


def insert_enterprise_location(connection, enterprise_id, address, start_date):
    try:
        cursor = connection.cursor()

        # Добавляем finish_date к предыдущей записи, если она существует
        update_query = """
            UPDATE EnterpriseLocations 
            SET FinishDate = %s 
            WHERE EnterpriseId = %s AND FinishDate IS NULL
        """
        cursor.execute(update_query, (start_date, enterprise_id))

        # Вставляем новую запись
        insert_query = """
            INSERT INTO EnterpriseLocations (EnterpriseId, Address, StartDate, FinishDate) 
            VALUES (%s, %s, %s, NULL)
        """
        cursor.execute(insert_query, (enterprise_id, address, start_date))

        connection.commit()
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print("Error inserting data into EnterpriseLocations table:", e)


def select_contacts_and_emails_by_date(connection, date):
    try:
        cursor = connection.cursor()
        query = "SELECT Phone, Email FROM EnterpriseContacts ec LEFT JOIN EnterpriseEmails ee ON ec.EnterpriseId = ee.EnterpriseId WHERE ec.StartDate <= %s AND (ec.FinishDate IS NULL OR ec.FinishDate >= %s) AND (ee.StartDate <= %s AND (ee.FinishDate IS NULL OR ee.FinishDate >= %s))"
        cursor.execute(query, (date, date, date, date))
        rows = cursor.fetchall()
        contacts_and_emails = [(row[0], row[1]) for row in rows]
        return contacts_and_emails
    except psycopg2.Error as e:
        print("Error selecting data from EnterpriseContacts and EnterpriseEmails tables:", e)


def select_enterprise_with_most_manager_changes(connection, start_date, end_date):
    try:
        cursor = connection.cursor()
        query = "SELECT EnterpriseId FROM (SELECT EnterpriseId, COUNT(*) AS manager_changes FROM EnterpriseManagers WHERE (StartDate >= %s AND StartDate <= %s) OR (FinishDate >= %s AND FinishDate <= %s) GROUP BY EnterpriseId ORDER BY manager_changes DESC LIMIT 1) AS max_changes"
        cursor.execute(query, (start_date, end_date, start_date, end_date))
        enterprise_id = cursor.fetchone()[0]
        return enterprise_id
    except psycopg2.Error as e:
        print("Error selecting enterprise with most manager changes:", e)


def out_manager(connection, manager_id):
    try:
        cursor = connection.cursor()
        query = "UPDATE EnterpriseManagers SET FinishDate = %s WHERE ManagerId = %s AND FinishDate IS NULL"
        cursor.execute(query, (datetime.now().date(), manager_id))
        connection.commit()
        print("Manager data inserted successfully.")
    except psycopg2.Error as e:
        print("Error inserting manager data:", e)


def insert_manager(connection, enterprise_id, manager_name, position, start_date=None):
    try:
        if start_date is None:
            start_date = datetime.now().date()
        cursor = connection.cursor()
        query = "INSERT INTO EnterpriseManagers (EnterpriseId, ManagerName, Position, StartDate) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (enterprise_id, manager_name, position, start_date))
        connection.commit()
        print("Manager data inserted successfully.")
    except psycopg2.Error as e:
        print("Error inserting manager data:", e)


def fetch_enterprise_managers(connection):
    try:
        cursor = connection.cursor()

        # Выбираем всех менеджеров предприятий
        select_query = "SELECT * FROM EnterpriseManagers"
        cursor.execute(select_query)
        managers = cursor.fetchall()

        print("Enterprise Managers:")
        for manager in managers:
            print(manager)

    except psycopg2.Error as e:
        print("Error fetching managers:", e)


def delete_tables(connection):
    try:
        cursor = connection.cursor()

        # Выбираем всех менеджеров предприятий
        query = "DROP TABLE IF EXISTS ActivityType, Enterprises, EnterpriseContacts, EnterpriseEmails, EnterpriseManagers, EnterpriseLocations CASCADE;"
        cursor.execute(query)
        answer = cursor.fetchall()

        print(answer)

    except psycopg2.Error as e:
        print("Error drop:", e)


def update_manager_finish_date(connection, manager_id, finish_date=None):
    try:
        if finish_date is None:
            finish_date = datetime.now().date()
        cursor = connection.cursor()
        query = "UPDATE EnterpriseManagers SET FinishDate = %s WHERE ManagerId = %s"
        cursor.execute(query, (finish_date, manager_id))
        connection.commit()
        print("Manager finish date updated successfully.")
    except psycopg2.Error as e:
        print("Error updating manager finish date:", e)


def insert_activity_type(connection, name):
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO ActivityType (Name) 
            VALUES (%s)
        """
        cursor.execute(query, (name,))
        connection.commit()
        print("Activity type data inserted successfully.")
    except psycopg2.Error as e:
        print("Error inserting activity type data:", e)


def select_all_enterprises(connection):
    try:
        cursor = connection.cursor()
        query = """
            SELECT * FROM Enterprises
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print("Id:", row[0])
            print("Name:", row[1])
            print("Activity Type Id:", row[2])
            print("-----------------------")
    except psycopg2.Error as e:
        print("Error selecting data from Enterprises table:", e)


def select_all_activity_types(connection):
    try:
        cursor = connection.cursor()
        query = """
            SELECT * FROM ActivityType
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print("Id Activity Type:", row[0])
            print("Name:", row[1])
            print("-----------------------")
    except psycopg2.Error as e:
        print("Error selecting data from ActivityType table:", e)


def get_enterprise_emails(connection, enterprise_id):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM EnterpriseEmails WHERE EnterpriseId = %s AND FinishDate IS NULL"
        cursor.execute(query, (enterprise_id,))
        emails = cursor.fetchall()
        print("Enterprise Emails:")
        for email in emails:
            print(email)
    except psycopg2.Error as e:
        print("Error fetching enterprise emails:", e)


def get_enterprise_locations(connection, enterprise_id):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM EnterpriseLocations WHERE EnterpriseId = %s"
        cursor.execute(query, (enterprise_id,))
        locations = cursor.fetchall()
        print("Enterprise Locations:")
        for location in locations:
            print(location)
    except psycopg2.Error as e:
        print("Error fetching enterprise locations:", e)


def fetch_enterprise_contacts(connection, enterprise_id):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM EnterpriseContacts WHERE EnterpriseId = %s"
        cursor.execute(query, (enterprise_id,))
        contacts = cursor.fetchall()
        if not contacts:
            print("No contacts found for enterprise with ID:", enterprise_id)
        else:
            print("Contacts for enterprise with ID:", enterprise_id)
            for contact in contacts:
                print(contact)
    except psycopg2.Error as e:
        print("Error fetching contacts:", e)


# Пример использования:
# Установка соединения с базой данных
connection = psycopg2.connect(database="postgres", user="postgres", password="1234", host="127.0.0.1", port="5433")
# delete_tables(connection)
create_missing_tables(connection)
# insert_activity_type(connection, "Type A")
# insert_activity_type(connection, "2", "Type B")
# insert_activity_type(connection, "3", "Type C")
# insert_enterprise(connection, "Enterprise 1", "1")
# insert_enterprise(connection, "Enterprise 2", "2")
# insert_enterprise(connection, "Enterprise 3", "3")
# Вывод данных из таблицы ActivityType
# print("Data from ActivityType table:")
# select_all_activity_types(connection)

# Вывод данных из таблицы Enterprises
# print("\nData from Enterprises table:")
# select_all_enterprises(connection)
# insert_enterprise_contact(connection, "123-454а56-7890", "2024-04-15", None)
# fetch_enterprise_contacts(connection, "1")
# connection.close()

while True:
    print("""
            Выберите пункт меню:
            1 - добавление предприятия
            2 - вывод предприятий
            3 - добавление активности
            4 - вывод активностей
            5 - добавление телефонного номера предприятия
            6 - вывод телефонного номера предприятия
            7 - добавление адреса предприятия
            8 - вывод адреса предприятия
            9 - добавление email предприятия
            10 - вывод email предприятия
            11 - добавление работника предприятия
            12 - вывод работников
            13 - уволить работника
    """)
    a = input()
    if a == '1':
        print('Введите name, active')
        name = input()
        active = input()
        insert_enterprise(connection, name, active)
    elif a == '2':
        print("\nData from Enterprises table:")
        select_all_enterprises(connection)
    elif a == '3':
        print('Введите id, active')
        active = input()
        insert_activity_type(connection, active)
    elif a == '4':
        print("Data from ActivityType table:")
        select_all_activity_types(connection)
    elif a == '5':
        print('Введите id, number, date')
        id = int(input())
        number = input()
        date = input()
        try:
            insert_enterprise_contact(connection, id, number, date, None)
        except psycopg2.Error as e:
            print("Error:", e)
    elif a == '6':
        print('Введите ID предприятия')
        b = input()
        fetch_enterprise_contacts(connection, b)
    elif a == '7':
        print('Введите id, address')
        id = int(input())
        address = input()
        try:
            insert_enterprise_location(connection, id, address, datetime.now().date())
        except psycopg2.Error as e:
            print("Error:", e)
    elif a == '8':
        print('Введите ID предприятия')
        id = int(input())
        get_enterprise_locations(connection, id)
    elif a == '9':
        print('Введите id, email')
        id = int(input())
        email = input()
        try:
            insert_enterprise_email(connection, id, email, datetime.now().date())
        except psycopg2.Error as e:
            print("Error:", e)
    elif a == '10':
        print('Введите ID предприятия')
        id = int(input())
        get_enterprise_emails(connection, id)
    elif a == '11':
        print('Введите id, name, work')
        id = int(input())
        name = input()
        work = input()
        try:
            insert_manager(connection, id, name, work, datetime.now().date())
        except psycopg2.Error as e:
            print("Error:", e)
    elif a == '12':
        fetch_enterprise_managers(connection)
    elif a == '13':
        print('Введите id')
        id = int(input())
        try:
            out_manager(connection, id)
        except psycopg2.Error as e:
            print("Error:", e)
