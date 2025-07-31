import click
from services.math_ops import compute_factorial
from storage.sqlite_store import store_request_sqlite

@click.command()
@click.option('--n', required=True, type=int, help='Number to calculate factorial of (e.g., 5)')
def factorial(n):
    """Calculate the factorial of n and store the result."""
    result = compute_factorial(n)
    click.secho(f"→ {n}! = {result}", fg="cyan")
    store_request_sqlite("factorial", {"n": n}, result)
    click.secho("Stored in SQLite.", fg="green")
