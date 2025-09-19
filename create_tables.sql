-- Таблиця для користувачів
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Таблиця для статусів
CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Таблиця для завдань
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (status_id) REFERENCES status (id),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);