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

di = DI()


@di.task()
async def download_20190101_衆議院議員一覧(bucket: Bucket = Depends(get_storage)):
    urls = {
        "自由民主党・無所属の会": "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/011kaiha.htm",
        "立憲民主党・無所属": "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/025kaiha.htm",
        "公明党": "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/040kaiha.htm",
        "日本共産党": "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/050kaiha.htm",
        "日本維新の会・無所属の会": "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/065kaiha.htm",
        "国民民主党・無所属クラブ": "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/066kaiha.htm",
        "無所属": "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/110kaiha.htm",
    }

    results = []

    for group, url in urls.items():
        async with httpx.AsyncClient() as client:
            content = await client.get(url)

        results += parse(url, group, content)

    blob = bucket.blob(f"politics/20210401_衆議院議員一覧.json")
    s = json.dumps(results, ensure_ascii=False)
    blob.upload_from_string(s, content_type="application/json")

    await index_content.do()


def parse(url, group, html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select("#shu2bdy table")[1]

    results = []

    for row in table.select("tr")[2:]:
        try:
            if a_tag := row.select_one("a"):
                link = a_tag["href"]
                link = urljoin(url, link)
            else:
                link = None
            el = row.select("td")
            data = {
                "link": link,
                "氏名": el[0].text[:-2],  # TODO: 最後に「君：がついているので削除 あと多分改行文字が含まれているので削除
                "ふりがな": el[1].text,
                "会派": group,
                "選挙区": el[2].text,
                "当選回数": el[3].text,
            }
            results.append(data)
        except Exception as e:
            pass

    return results


@di.task()
async def index_content(
    bucket: Bucket = Depends(get_storage),
    loader=Depends(es.AsyncBulkInsert("共通スキーマ")),
):
    blob = bucket.blob(f"politics/20210401_衆議院議員一覧.json")
    data = blob.download_as_string()
    data = json.loads(data)
    mapper = ({"衆議院議員一覧": x} for x in data)

    async for ok, result in loader(actions=mapper):
        print(result)


@di.task()
async def download_20190101_歴代参議院議員一覧(db: Bucket = Depends(get_storage)):
    from ..es import dictionaries
    import pandas as pd
    import numpy as np

    blob = db.blob(f"politics/20190101_歴代参議院議員一覧.xls")
    excel = blob.download_as_bytes()

    df = pd.read_excel(excel, sheet_name="議員一覧")
    df = df.rename(columns={"選挙区\n（最終）": "選挙区（最終）", "議員氏名\n（本名）": "本名", "会派（最終）": "会派"})
    del df["Unnamed: 0"]
    data = df.replace([np.nan], [None]).to_dict("records")

    blob = db.blob(f"politics/20190101_歴代参議院議員一覧.json")
    s = json.dumps(data, ensure_ascii=False)
    blob.upload_from_string(s, content_type="application/json")

    await index_content2.do()


@di.task()
async def index_content2(
    # loader=Depends(es.AsyncBulkInsert("歴代参議院議員一覧")),
    loader=Depends(es.AsyncBulkInsert("共通スキーマ")),
    bucket: Bucket = Depends(get_storage),
):
    blob = bucket.blob("politics/20190101_歴代参議院議員一覧.json")
    text = blob.download_as_string()
    data = json.loads(text)

    mapper = ({"参議院議員一覧": x} for x in data)

    async for ok, result in loader(actions=mapper):
        print(result)
