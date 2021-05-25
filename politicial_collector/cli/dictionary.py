import typer

from ..crawlers import 史料編纂所データベース異体字同定一覧
from .utils import to_sync

app = typer.Typer()


@app.command()
@to_sync
async def update(
    output: str = "./politicial_collector/es/dictionaries/char_mappings_異体字.py",
):
    """史料編纂所データベース異体字同定一覧を取得し、ソースファイルを更新します。"""
    # await 史料編纂所データベース異体字同定一覧.get_content()
    # await 史料編纂所データベース異体字同定一覧.upload_dictionaries.do()

    result = await 史料編纂所データベース異体字同定一覧.download_dictionaries.do()

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
