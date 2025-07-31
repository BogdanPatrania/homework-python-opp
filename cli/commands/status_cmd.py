import click
from storage.task_store import get_task

@click.command()
@click.option('--task-id', required=True, help='Task ID to check status for')
def status(task_id):
    """Check the status and result of a background task."""
    task = get_task(task_id)
    if not task:
        click.secho(f"No task found with ID: {task_id}", fg="red")
    else:
        click.secho(f"Task ID: {task['task_id']}", fg="cyan")
        click.secho(f"Status: {task['status']}", fg="yellow")
        click.secho(f"Result: {task['result']}", fg="green" if task['status'] == "done" else "white")
