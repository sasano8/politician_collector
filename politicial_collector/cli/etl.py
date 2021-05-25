import typer
from .utils import to_sync

app = typer.Typer()


def crawlers():
    """実行可能なクローラの一覧を取得する"""
    ...


@app.command()
def extract():
    """指定したデータソース（デフォルトは全て）を元ソースサイトやAPIから取得し、データレイクに保存する"""
    ...


@app.command()
def transform():
    """指定したデータソースをデータレイクから取り出し、加工する"""


@app.command()
@to_sync
async def load():
    """指定したデータソースをインデクシングする"""
    from .. import indices
    from ..crawlers import 質問主意書, 衆議院議員一覧, 史料編纂所データベース異体字同定一覧, 最新参議院議員一覧, 政治家一覧

    # await 史料編纂所データベース異体字同定一覧.get_content()
    # await 史料編纂所データベース異体字同定一覧.upload_dictionaries.do()

    # await es.put_index(**indices.共通スキーマ)
    # await 政治家一覧.index_content.do()
    # await 質問主意書.stream_content()
    # await 衆議院議員一覧.download_20190101_歴代参議院議員一覧.do()
    # await 衆議院議員一覧.download_20190101_衆議院議員一覧.do()
    # await 最新参議院議員一覧.index_content.do()
