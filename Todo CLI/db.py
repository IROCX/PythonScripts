import sqlite3
from typing import List
from datetime import datetime
from model import Todo

conn = sqlite3.connect("todos.db")
c = conn.cursor()


def createTable():
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            todo text, 
            category text, 
            dateAdded text, 
            dateCompleted text,
            status integer,
            position integer
        )"""
    )


createTable()


def insertTodo(todo: Todo):
    c.execute("SELECT COUNT(*) FROM todos")
    print("COUNT COMMAND", c)
    count = c.fetchone()[0]

    todo.position = count + 1 if count else 1

    with conn:
        c.execute(
            "INSERT INTO todos VALUES (:task,:category,:dateAdded,:dateCompleted,:status,:position)",
            {
                "task": todo.task,
                "category": todo.category,
                "dateAdded": todo.dateAdded,
                "dateCompleted": todo.dateCompleted,
                "status": todo.status,
                "position": todo.position,
            },
        )


def getAllTodos() -> List[Todo]:
    c.execute("SELECT * FROM todos")
    print("COUNT COMMAND", c)
    results = c.fetchall()
    todos = []

    for result in results:
        todos.append(Todo(*result))

    return todos


def deleteTodo(position) -> None:
    c.execute("SELECT COUNT(*) FROM todos")

    count = c.fetchone()[0]

    if count >= position:
        with conn:
            c.execute(
                "DELETE FROM todos WHERE position=:position", {"position": position}
            )
            for pos in range(position + 1, count + 1):
                changePosition(pos, pos - 1, False)


def changePosition(oldPos, newPos, commit=True):
    c.execute(
        "UPDATE todos SET position = :position_new WHERE position = :position_old   ",
        {"position_new": newPos, "position_old": oldPos},
    )

    if commit:
        conn.commit()


def updateTodo(position, task, category) -> None:
    with conn:
        if task and category:
            c.execute(
                "UPDATE todos SET task = :task, category = :category WHERE position = :position",
                {"task": task, "position": position, "category": category},
            )
        elif task:
            c.execute(
                "UPDATE todos SET task = :task WHERE position = :position",
                {"task": task, "position": position, "category": category},
            )
        elif category:
            c.execute(
                "UPDATE todos SET category = :category WHERE position = :position",
                {"task": task, "position": position, "category": category},
            )


def completeTodo(position):
    with conn:
        c.execute(
            "UPDATE todos SET status = :status, dateCompleted = :dateCompleted WHERE position = :position",
            {
                "status": 1,
                "position": position,
                "dateCompleted": datetime.now().isoformat(),
            },
        )
