import sqlite3
from faker import Faker
import random

fake = Faker()
NUMBER_USERS = 10
NUMBER_TASKS = 20

def generate_fake_data(number_users, number_tasks):
    fake_users = []
    for _ in range(number_users):
        fake_users.append((fake.name(), fake.email()))
    
    statuses = [('new',), ('in progress',), ('completed',)]
    
    fake_tasks = []
    for _ in range(number_tasks):
        title = fake.sentence(nb_words=5)
        description = fake.paragraph(nb_sentences=2)
        status_id = random.randint(1, 3) # 1:new, 2:in progress, 3:completed
        user_id = random.randint(1, number_users)
        fake_tasks.append((title, description, status_id, user_id))
    
    return fake_users, statuses, fake_tasks

def seed_database():
    try:
        with sqlite3.connect('task_management.db') as con:
            cur = con.cursor()
            
            # Заповнення таблиці status
            statuses = [('new',), ('in progress',), ('completed',)]
            cur.executemany("INSERT INTO status (name) VALUES (?)", statuses)
            
            # Генерація та заповнення fake даних
            fake_users, _, fake_tasks = generate_fake_data(NUMBER_USERS, NUMBER_TASKS)
            
            # Заповнення таблиці users
            cur.executemany("INSERT INTO users (fullname, email) VALUES (?, ?)", fake_users)
            
            # Заповнення таблиці tasks
            cur.executemany("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)", fake_tasks)
            
            con.commit()
            print("База даних успішно заповнена.")
            
    except sqlite3.Error as e:
        print(f"Помилка SQLite: {e}")

if __name__ == '__main__':
    seed_database()