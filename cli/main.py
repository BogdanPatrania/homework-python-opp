import click
from cli.commands.pow_cmd import pow
from cli.commands.fibonacci_cmd import fibonacci
from cli.commands.factorial_cmd import factorial
from cli.commands.export_cmd import export
from cli.commands.status_cmd import status

@click.group()
def cli():
    """Math Microservice CLI – Perform math ops and export history."""
    pass

cli.add_command(pow)
cli.add_command(fibonacci)
cli.add_command(factorial)
cli.add_command(export)
cli.add_command(status)

if __name__ == "__main__":
    cli()
