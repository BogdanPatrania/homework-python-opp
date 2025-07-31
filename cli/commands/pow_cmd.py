import click
from services.math_ops import compute_pow
from storage.sqlite_store import store_request_sqlite

@click.command()
@click.option('--base', required=True, type=float, help='Base number (e.g., 2)')
@click.option('--exp', required=True, type=float, help='Exponent (e.g., 5)')
def pow(base, exp):
    """Calculate base raised to exponent and store the result."""
    result = compute_pow(base, exp)
    click.secho(f"→ {base}^{exp} = {result}", fg="cyan")
    store_request_sqlite("pow", {"base": base, "exp": exp}, result)
    click.secho("Stored in SQLite.", fg="green")
