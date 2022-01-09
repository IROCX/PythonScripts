from rich.color import Color
import typer

from rich.console import Console
from rich.table import Table

from model import Todo
from db import (
    getAllTodos,
    deleteTodo,
    updateTodo,
    completeTodo,
    changePosition,
    insertTodo,
)

console = Console()
app = typer.Typer()


@app.command(short_help="Adds a todo task")
def add(task: str, category: str):
    typer.echo(f"adding {task} with {category} category.")

    todo = Todo(task, category)
    insertTodo(todo)
    show()


@app.command(short_help="Deleted a todo task specified by number")
def delete(position: int):
    typer.echo(f"deleteing task {position}.")
    deleteTodo(position)
    show()


@app.command(short_help="Updates a todo task specified by number")
def update(position: int, task: str = None, category: str = None):
    typer.echo(f"updating task {position} with {task} and {category}.")
    updateTodo(position, task, category)
    show()


@app.command(short_help="Marks a todo task specified by number completed")
def complete(position: int):
    typer.echo(f"Marking task {position} as complete.")
    completeTodo(position)
    show()


def getCategoryColor(category):
    COLORS = {"Learn": "cyan", "Youtube": "red", "Study": "green", "General": "teal"}

    if category in COLORS:
        return COLORS[category]
    return "white"


@app.command()
def show():
    tasks = getAllTodos()

    console.print("[bold magenta]TODOS[/bold magenta]")
    table = Table(show_header=True, header_style="bold blue")

    table.add_column("#", style="dim", width=10)
    table.add_column("Todo", min_width=25)
    table.add_column("Category", min_width=15, justify="right")
    table.add_column("Done", min_width=15, justify="right")

    for id, task in enumerate(tasks, start=1):

        c = getCategoryColor(task.category)
        isDone = "✅" if task.status else "❌"
        table.add_row(str(id), task.task, f"[{c}]{task.category}[/{c}]", isDone)
    console.print(table)


if __name__ == "__main__":
    app()
