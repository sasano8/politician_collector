import httpx
from bs4 import BeautifulSoup
from fastapi_di import DI
from fastapi import Depends
from ..firestorage import get_storage, Bucket
import json
from .. import es
from fastapi import Depends
from urllib.parse import urljoin
import pandas as pd
import numpy as np

di = DI()


@di.task()
async def download_content(bucket: Bucket = Depends(get_storage)):
    import io

    blob = bucket.blob(f"politics/政治家一覧.csv")
    data = blob.download_as_string()
    df = pd.read_csv(io.StringIO(data.decode("utf-8")))
    data = df.replace([np.nan], [None]).to_dict("records")
    return data


@di.task()
async def index_content(
    loader=Depends(es.AsyncBulkInsert("共通スキーマ")), data=Depends(download_content)
):
    mapper = ({"profile": x} for x in data)
    async for ok, result in loader(actions=mapper):
        print(result)
