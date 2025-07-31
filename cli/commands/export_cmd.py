import click
import csv
from datetime import datetime
from storage.sqlite_store import get_all_requests_sqlite

@click.command()
@click.option('--operation', type=click.Choice(['pow', 'fibonacci', 'factorial', 'all']), default='all',
              help="Which operation to export (default: all)")
@click.option('--output', default=None, help='Output CSV file path (optional)')
def export(operation, output):
    """Export operation history from SQLite to a CSV file."""
    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"history_export_{operation}_{timestamp}.csv"

    all_records = get_all_requests_sqlite()
    records = [r for r in all_records if r[1] == operation] if operation != 'all' else all_records

    with open(output, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "operation", "input_data", "result", "timestamp"])
        for row in records:
            writer.writerow(row)

    click.secho(f"Exported {len(records)} records to '{output}'.", fg="yellow")
