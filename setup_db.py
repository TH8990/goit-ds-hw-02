import sqlite3

def execute_sql_from_file(db_file, sql_file):
    with open(sql_file, 'r') as f:
        sql_script = f.read()

    with sqlite3.connect(db_file) as con:
        cur = con.cursor()
        cur.executescript(sql_script)

if __name__ == "__main__":
    db_name = 'task_management.db'
    sql_script_file = 'create_tables.sql'
    execute_sql_from_file(db_name, sql_script_file)
    print("Таблиці успішно створено.")