import typer
from .dictionary import app as dictionary
from .etl import app as etl

app = typer.Typer()
app.add_typer(dictionary, name="dictionary")
app.add_typer(etl, name="etl")
