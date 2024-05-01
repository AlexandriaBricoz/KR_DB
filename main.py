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
        missing_tables = { "Enterprises","ActivityType", "EnterpriseContacts", "EnterpriseEmails", "EnterpriseManagers",
                          "EnterpriseLocations"} - set(existing_tables)

        for table in missing_tables:
            if table == "ActivityType":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ActivityType (
                        IdActivityType VARCHAR(10) PRIMARY KEY,
                        Name VARCHAR(100)
                    )
                """)
            elif table == "Enterprises":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Enterprises (
                        Id VARCHAR(10) PRIMARY KEY,
                        Name VARCHAR(100),
                        IdActivityType VARCHAR(10),
                        FOREIGN KEY (IdActivityType) REFERENCES ActivityType(IdActivityType)
                    )
                """)
            elif table == "EnterpriseContacts":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS EnterpriseContacts (
                        EnterpriseId VARCHAR(10) PRIMARY KEY,
                        Phone VARCHAR(20),
                        StartDate DATE,
                        FinishDate DATE,
                        FOREIGN KEY (EnterpriseId) REFERENCES Enterprises(Id)
                    )
                """)
            elif table == "EnterpriseEmails":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS EnterpriseEmails (
                        EnterpriseId VARCHAR(10) PRIMARY KEY,
                        Email VARCHAR(100),
                        StartDate DATE,
                        FinishDate DATE,
                        FOREIGN KEY (EnterpriseId) REFERENCES Enterprises(Id)
                    )
                """)
            elif table == "EnterpriseManagers":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS EnterpriseManagers (
                        ManagerId VARCHAR(10) PRIMARY KEY,
                        ManagerName VARCHAR(100),
                        Position VARCHAR(50),
                        StartDate DATE,
                        FinishDate DATE,
                        FOREIGN KEY (ManagerId) REFERENCES Enterprises(Id)
                    )
                """)
            elif table == "EnterpriseLocations":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS EnterpriseLocations (
                        EnterpriseId VARCHAR(10) PRIMARY KEY,
                        Address VARCHAR(100),
                        StartDate DATE,
                        FinishDate DATE,
                        FOREIGN KEY (EnterpriseId) REFERENCES Enterprises(Id)
                    )
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


def insert_enterprise(connection, id, name, activity_type_id):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO Enterprises (Id, Name, IdActivityType) VALUES (%s, %s, %s)"
        cursor.execute(query, (id, name, activity_type_id))
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


def insert_enterprise_emails(connection, enterprise_id, email, start_date, finish_date=None):
    try:
        cursor = connection.cursor()

        # Если finish_date не указан, используем текущую дату
        if finish_date is None:
            finish_date = datetime.now().date()

        # Обновляем записи с предыдущим адресом электронной почты, чтобы указать их недействительность
        update_query = "UPDATE EnterpriseEmails SET FinishDate = %s WHERE EnterpriseId = %s AND Email = %s AND FinishDate IS NULL"
        cursor.execute(update_query, (finish_date, enterprise_id, email))

        # Вставляем новую запись с новым адресом электронной почты
        insert_query = "INSERT INTO EnterpriseEmails (EnterpriseId, Email, StartDate, FinishDate) VALUES (%s, %s, %s, NULL)"
        cursor.execute(insert_query, (enterprise_id, email, start_date))

        connection.commit()
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print("Error inserting data into EnterpriseEmails table:", e)


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


def insert_manager(connection, manager_id, manager_name, position, start_date=None):
    try:
        if start_date is None:
            start_date = datetime.now().date()
        cursor = connection.cursor()
        query = "INSERT INTO EnterpriseManagers (ManagerId, ManagerName, Position, StartDate) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (manager_id, manager_name, position, start_date))
        connection.commit()
        print("Manager data inserted successfully.")
    except psycopg2.Error as e:
        print("Error inserting manager data:", e)


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
def insert_activity_type(connection, id, name):
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO ActivityType (IdActivityType, Name) 
            VALUES (%s, %s)
        """
        cursor.execute(query, (id, name))
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
create_missing_tables(connection)
# insert_activity_type(connection, "1", "Type A")
# insert_activity_type(connection, "2", "Type B")
# insert_activity_type(connection, "3", "Type C")
# insert_enterprise(connection, "1", "Enterprise 1", "1")
# insert_enterprise(connection, "2", "Enterprise 2", "2")
# insert_enterprise(connection, "3", "Enterprise 3", "3")
# Вывод данных из таблицы ActivityType
print("Data from ActivityType table:")
select_all_activity_types(connection)

# Вывод данных из таблицы Enterprises
print("\nData from Enterprises table:")
select_all_enterprises(connection)

insert_enterprise_contact(connection, "1", "123-454а56-7890", "2024-04-15", None)
fetch_enterprise_contacts(connection, "1")
connection.close()
