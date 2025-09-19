import sqlite3

# Функція для виконання SQL-запитів SELECT
def execute_select_query(query: str, params: tuple = ()) -> list:
    try:
        with sqlite3.connect('task_management.db') as con:
            cur = con.cursor()
            cur.execute(query, params)
            return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Помилка SQLite: {e}")
        return []

# Функція для виконання SQL-запитів INSERT, UPDATE, DELETE
def execute_non_select_query(query: str, params: tuple = ()) -> None:
    try:
        with sqlite3.connect('task_management.db') as con:
            cur = con.cursor()
            cur.execute(query, params)
            con.commit()
            print("Запит успішно виконано.")
    except sqlite3.Error as e:
        print(f"Помилка SQLite: {e}")

# Функція для отримання ID статусу за його назвою
def get_status_id(status_name: str) -> int:
    query = "SELECT id FROM status WHERE name = ?"
    result = execute_select_query(query, (status_name,))
    if result:
        return result[0][0]
    return None

# --- ЗАПИТИ ДЛЯ ВИКОНАННЯ ---

# 1. Отримати всі завдання певного користувача (user_id = 1)
def get_tasks_by_user(user_id: int):
    query = "SELECT * FROM tasks WHERE user_id = ?"
    print(f"\n1. Завдання користувача з ID={user_id}:")
    tasks = execute_select_query(query, (user_id,))
    print(tasks)

# 2. Вибрати завдання за певним статусом ('new')
def get_tasks_by_status(status_name: str):
    status_id = get_status_id(status_name)
    if status_id is not None:
        query = "SELECT * FROM tasks WHERE status_id = ?"
        print(f"\n2. Завдання зі статусом '{status_name}':")
        tasks = execute_select_query(query, (status_id,))
        print(tasks)

# 3. Оновити статус конкретного завдання (task_id = 1) на 'in progress'
def update_task_status(task_id: int, new_status_name: str):
    new_status_id = get_status_id(new_status_name)
    if new_status_id is not None:
        query = "UPDATE tasks SET status_id = ? WHERE id = ?"
        print(f"\n3. Оновлення статусу завдання ID={task_id} на '{new_status_name}':")
        execute_non_select_query(query, (new_status_id, task_id))

# 4. Отримати список користувачів, які не мають жодного завдання
def get_users_without_tasks():
    query = "SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks)"
    print("\n4. Користувачі без завдань:")
    users = execute_select_query(query)
    print(users)

# 5. Додати нове завдання для конкретного користувача (user_id = 1)
def add_new_task(user_id: int):
    query = "INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)"
    status_id = get_status_id('new')
    if status_id is not None:
        params = ("New Task from Script", "This is a new task added via Python script.", status_id, user_id)
        print(f"\n5. Додавання нового завдання для користувача ID={user_id}:")
        execute_non_select_query(query, params)

# 6. Отримати всі завдання, які ще не завершено
def get_unfinished_tasks():
    status_id = get_status_id('completed')
    if status_id is not None:
        query = "SELECT * FROM tasks WHERE status_id != ?"
        print("\n6. Незавершені завдання:")
        tasks = execute_select_query(query, (status_id,))
        print(tasks)

# 7. Видалити конкретне завдання (task_id = 5)
def delete_task(task_id: int):
    query = "DELETE FROM tasks WHERE id = ?"
    print(f"\n7. Видалення завдання ID={task_id}:")
    execute_non_select_query(query, (task_id,))

# 8. Знайти користувачів з певною електронною поштою
def find_users_by_email_domain(domain: str):
    query = "SELECT * FROM users WHERE email LIKE ?"
    print(f"\n8. Користувачі з e-mail '{domain}':")
    users = execute_select_query(query, (f"%{domain}",))
    print(users)

# 9. Оновити ім'я користувача (user_id = 2)
def update_user_name(user_id: int, new_name: str):
    query = "UPDATE users SET fullname = ? WHERE id = ?"
    print(f"\n9. Оновлення імені користувача ID={user_id}:")
    execute_non_select_query(query, (new_name, user_id))

# 10. Отримати кількість завдань для кожного статусу
def count_tasks_by_status():
    query = """
    SELECT s.name, COUNT(t.id) 
    FROM status s 
    LEFT JOIN tasks t ON s.id = t.status_id 
    GROUP BY s.name
    """
    print("\n10. Кількість завдань за статусом:")
    counts = execute_select_query(query)
    print(counts)

# 11. Отримати завдання, призначені користувачам з певною доменною частиною електронної пошти
def get_tasks_by_user_email_domain(domain: str):
    query = """
    SELECT t.*
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE ?
    """
    print(f"\n11. Завдання користувачів з e-mail '{domain}':")
    tasks = execute_select_query(query, (f"%{domain}",))
    print(tasks)

# 12. Отримати список завдань, що не мають опису
def get_tasks_without_description():
    query = "SELECT * FROM tasks WHERE description IS NULL OR description = ''"
    print("\n12. Завдання без опису:")
    tasks = execute_select_query(query)
    print(tasks)

# 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
def get_users_and_tasks_in_progress():
    query = """
    SELECT u.fullname, t.title, s.name
    FROM users u
    INNER JOIN tasks t ON u.id = t.user_id
    INNER JOIN status s ON t.status_id = s.id
    WHERE s.name = 'in progress'
    """
    print("\n13. Користувачі та їхні завдання зі статусом 'in progress':")
    users_tasks = execute_select_query(query)
    print(users_tasks)

# 14. Отримати користувачів та кількість їхніх завдань
def get_users_and_task_count():
    query = """
    SELECT u.fullname, COUNT(t.id) AS total_tasks
    FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.fullname
    ORDER BY total_tasks DESC
    """
    print("\n14. Кількість завдань у кожного користувача:")
    counts = execute_select_query(query)
    print(counts)

if __name__ == "__main__":
   
    # Виклик функцій для виконання запитів
    get_tasks_by_user(1)
    get_tasks_by_status('new')
    update_task_status(1, 'in progress')
    get_users_without_tasks()
    add_new_task(2)
    get_unfinished_tasks()
    delete_task(3)
    find_users_by_email_domain('example.com')
    update_user_name(4, 'Нове ім`я')
    count_tasks_by_status()
    get_tasks_by_user_email_domain('example.net')
    get_tasks_without_description()
    get_users_and_tasks_in_progress()
    get_users_and_task_count()