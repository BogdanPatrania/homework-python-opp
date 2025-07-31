import click
from services.math_ops import compute_fibonacci
from storage.sqlite_store import store_request_sqlite

@click.command()
@click.option('--n', required=True, type=int, help='Index of the Fibonacci number (e.g., 8)')
def fibonacci(n):
    """Calculate the nth Fibonacci number and store the result."""
    result = compute_fibonacci(n)
    click.secho(f"→ Fibonacci({n}) = {result}", fg="cyan")
    store_request_sqlite("fibonacci", {"n": n}, result)
    click.secho("Stored in SQLite.", fg="green")
