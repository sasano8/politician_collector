import httpx
from bs4 import BeautifulSoup
from fastapi_di import DI
from fastapi import Depends
from ..firestorage import get_storage, Bucket
import json
from .. import es
from fastapi import Depends
from elasticsearch.helpers import async_streaming_bulk
from urllib.parse import urljoin

# from ..cleaner import normalize_html
from ja_text_cleaner.normalizer import normalize_html

di = DI()


async def get_contents():
    urls = ["https://www.sangiin.go.jp/japanese/joho1/kousei/giin/204/giin.htm"]

    for url in urls:
        async for x in parse_page(url):
            yield x


async def parse_page(url):
    async with httpx.AsyncClient() as client:
        html = await client.get(url)

    soup = BeautifulSoup(html, "html.parser")
    table = soup.select("#ContentsBox table")[1]

    for row in table.select("tr")[1:]:
        el = row.select("td")
        name = el[0].select_one("a").text
        names = name.split("[")

        if len(names) == 1:
            議員氏名 = names[0]
            本名 = None
        elif len(names) == 2:
            議員氏名 = names[0]
            本名 = names[1].replace("]", "")
        else:
            raise Exception()

        data = {
            "link": el[0].select_one("a")["href"],
            "議員氏名": normalize_html(議員氏名),
            "本名": normalize_html(本名),
            "読み方": normalize_html(el[1].text),
            "会派": normalize_html(el[2].text),
            "選挙区": normalize_html(el[3].text),
            "任期満了": normalize_html(el[4].text),
        }
        data["link"] = urljoin(url, data["link"])

        if tag := el[5].select_one("a"):
            data["正字"] = tag["href"]
        else:
            data["正字"] = None

        yield data


@di.task()
async def download_content(bucket: Bucket = Depends(get_storage)):
    blob = bucket.blob(f"politics/20210401_現在の参議院議員一覧.json")
    if not blob.exists():
        data = []
        async for x in get_contents():
            data.append(x)
        content = json.dumps(data, ensure_ascii=False)
        blob.upload_from_string(content, content_type="application/json")
    else:
        content = blob.download_as_string()

    data = json.loads(content)
    return data


@di.task()
async def index_content(
    data=Depends(download_content),
    loader=Depends(es.AsyncBulkInsert("共通スキーマ")),
):
    mapper = ({"最新参議院議員一覧": x} for x in data)

    async for ok, result in loader(actions=mapper):
        print(result)
