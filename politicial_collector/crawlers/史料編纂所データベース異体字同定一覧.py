import httpx
from bs4 import BeautifulSoup
from fastapi_di import DI
from fastapi import Depends
from ..firestorage import get_storage, Bucket
import json

# from ..cleaner import normalize_html
from ja_text_cleaner.normalizer import normalize_html


di = DI()


async def get_content():
    url = "https://wwwap.hi.u-tokyo.ac.jp/ships/itaiji_list.jsp"
    async with httpx.AsyncClient() as client:
        content = await client.get(url)

    soup = BeautifulSoup(content, "html.parser")

    # table_html = str.maketrans(
    #     {
    #         "\u3000": " ",  # htmlのスペース
    #         "\xa0": " ",  # ノーブレークスペース
    #         "\r": " ",
    #         "\n": " ",
    #     }
    # )

    results = []

    # 先頭行はタイトルなので除外
    for el in soup.select_one(".ITAIJI").select("tr.w,tr.g")[0:]:
        row = el.select("td")
        no = normalize_html(row[0].text)
        base = normalize_html(row[1].text)
        synonym = normalize_html(row[2].text)

        results.append({"no": int(no), "base": base, "synonym": synonym})

    await load.do(rows=results)


@di.task()
async def load(db: Bucket = Depends(get_storage), *, rows):
    blob = db.blob("dictionaries/異体字同定一覧.json")
    blob.upload_from_string(
        json.dumps(rows, ensure_ascii=False), content_type="application/json"
    )


@di.task()
async def upload_dictionaries(db: Bucket = Depends(get_storage)):
    from ..es import dictionaries

    names = {
        "synonym_graph_ja",
        "dic_ja_popular",
        "dic_ja_political",
        "stopwords_ja_tag_cloud",
    }

    for name in names:
        data = getattr(dictionaries, name)
        blob = db.blob(f"dictionaries/{name}.json")
        s = json.dumps(data, ensure_ascii=False)
        blob.upload_from_string(s, content_type="application/json")


@di.task()
async def download_dictionaries(db: Bucket = Depends(get_storage)):
    blob = db.blob("dictionaries/異体字同定一覧.json")
    text = blob.download_as_string()
    data = json.loads(text)
    return data
