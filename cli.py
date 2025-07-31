import click
from services.math_ops import compute_pow, compute_fibonacci, compute_factorial
from storage.sqlite_store import store_request_sqlite, get_all_requests_sqlite
from datetime import datetime
import csv

@click.group()
def cli():
    """Math Microservice CLI – Perform math ops and export history."""
    pass


@cli.command()
@click.option('--base', required=True, type=float, help='Base number (e.g., 2)')
@click.option('--exp', required=True, type=float, help='Exponent (e.g., 5)')
def pow(base, exp):
    """Calculate base raised to exponent and store the result."""
    result = compute_pow(base, exp)
    click.secho(f"→ {base}^{exp} = {result}", fg="cyan")
    store_request_sqlite("pow", {"base": base, "exp": exp}, result)
    click.secho("Stored in SQLite.", fg="green")


@cli.command()
@click.option('--n', required=True, type=int, help='Index of the Fibonacci number (e.g., 8)')
def fibonacci(n):
    """Calculate the nth Fibonacci number and store the result."""
    result = compute_fibonacci(n)
    click.secho(f"→ Fibonacci({n}) = {result}", fg="cyan")
    store_request_sqlite("fibonacci", {"n": n}, result)
    click.secho("Stored in SQLite.", fg="green")


@cli.command()
@click.option('--n', required=True, type=int, help='Number to calculate factorial of (e.g., 5)')
def factorial(n):
    """Calculate the factorial of n and store the result."""
    result = compute_factorial(n)
    click.secho(f"→ {n}! = {result}", fg="cyan")
    store_request_sqlite("factorial", {"n": n}, result)
    click.secho("Stored in SQLite.", fg="green")


@cli.command()
@click.option('--operation', type=click.Choice(['pow', 'fibonacci', 'factorial', 'all']), default='all',
              help="Which operation to export (default: all)")
@click.option('--output', default=None, help='Output CSV file path (optional)')
def export(operation, output):
    """Export operation history from SQLite to a CSV file."""
    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"history_export_{operation}_{timestamp}.csv"

    all_records = get_all_requests_sqlite()

    if operation != 'all':
        records = [r for r in all_records if r[1] == operation]
    else:
        records = all_records

    with open(output, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "operation", "input_data", "result", "timestamp"])
        for row in records:
            writer.writerow(row)

    click.secho(f"Exported {len(records)} records to '{output}'.", fg="yellow")


if __name__ == "__main__":
    cli()
