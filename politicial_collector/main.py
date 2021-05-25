from politicial_collector.crawlers.衆議院議員一覧 import index_content
import asy

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .queues import queue_default, queue_extract, queue_transform
from . import es

app = FastAPI(title="政治家検索API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # 追記により追加
    allow_methods=["*"],  # 追記により追加
    allow_headers=["*"],  # 追記により追加
)

# supervisor = asy.supervise(queue_default, queue_extract, queue_transform)
supervisor = asy.supervise()


from .api import political_person

app.include_router(political_person.router, prefix="/person")


@app.on_event("startup")
async def startup_worker():
    """ワーカーを起動します"""

    await supervisor.start()

    from . import es

    print(await es.helth())

    await recreate_index()


async def recreate_index():

    from . import indices
    from .crawlers import 質問主意書, 衆議院議員一覧, 史料編纂所データベース異体字同定一覧, 最新参議院議員一覧, 政治家一覧

    # await 史料編纂所データベース異体字同定一覧.get_content()
    # await 史料編纂所データベース異体字同定一覧.upload_dictionaries.do()

    # await es.put_index(**indices.共通スキーマ)
    # await 政治家一覧.index_content.do()
    # await 質問主意書.stream_content()
    # await 衆議院議員一覧.download_20190101_歴代参議院議員一覧.do()
    # await 衆議院議員一覧.download_20190101_衆議院議員一覧.do()
    # await 最新参議院議員一覧.index_content.do()


@app.on_event("shutdown")
async def shutdown_worker():
    """ワーカーを終了します"""
    await supervisor.stop()
