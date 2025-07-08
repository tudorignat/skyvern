import json
from typing import List

import typer
from tabulate import tabulate

from evaluation.core.utils import WebVoyagerTestCase, load_webvoyager_case_from_json

app = typer.Typer()

@app.command()
def preview(
    file_path: str = typer.Argument(..., help="Path to the JSONL file with WebVoyager tasks"),
    show_answers: bool = typer.Option(False, "--answers", "-a", help="Whether to display the answers as well"),
    max_rows: int = typer.Option(20, "--max", "-m", help="Max number of tasks to show"),
):
    tasks: List[WebVoyagerTestCase] = list(load_webvoyager_case_from_json(file_path))

    headers = ["#", "ID", "URL", "QUESTION", "UPDATED"]
    if show_answers:
        headers.append("ANSWER")

    table_data = []
    for i, task in enumerate(tasks[:max_rows]):
        row = [
            i + 1,
            task.id,
            task.url,
            task.question,
            "✅" if task.is_updated else "❌"
        ]
        if show_answers:
            answer_preview = task.answer[:80] + "..." if len(task.answer) > 80 else task.answer
            row.append(answer_preview)
        table_data.append(row)

    typer.echo(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

if __name__ == "__main__":
    app()
