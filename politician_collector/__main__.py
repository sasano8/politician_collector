import typer
import asyncio

from .crawlers import 史料編纂所データベース異体字同定一覧

app = typer.Typer()
dictionary = typer.Typer()


@dictionary.command()
def update(output: str = "./politician_collector/es/dictionaries/char_mappings_異体字.py"):
    result = asyncio.run(史料編纂所データベース異体字同定一覧.download_dictionaries.do())

    def write_python_file(data):
        yield "# auto generate\n"
        yield "char_mappings_異体字 = [\n"
        for item in result:
            base = item["base"]
            synonyms = item["synonym"]

            for synomym in synonyms.split(" "):
                yield f'"{synomym} => {base}",\n'
        yield "]\n"

    with open(output, "w") as f:
        f.writelines(write_python_file(result))


app.add_typer(dictionary, name="dictionary")
app()
