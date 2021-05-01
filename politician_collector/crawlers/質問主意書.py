import asyncio
from urllib.parse import urljoin


import logging

import httpx
from bs4 import BeautifulSoup
from ..queues import queue_default, queue_extract, queue_transform
from .. import es
from fastapi import Depends
from elasticsearch.helpers import async_streaming_bulk
import json
from ..storage import datalake

# from ..cleaner import normalize_ja
from ja_text_cleaner.name import Wakachi

logger = logging.getLogger(__name__)


storage = datalake.foler("質問主意書")
storage.mkdir()


@queue_extract.task
async def get_all_content_govement_question():
    return
    page_max = "204"
    url = "https://www.sangiin.go.jp/japanese/joho1/kousei/syuisyo/{page}/syuisyo.htm"

    async with httpx.AsyncClient() as client:
        content = await client.get(url.format(page=page_max))

    soup = BeautifulSoup(content, "html.parser")
    pages = soup.select("select[title='国会回次指定'] > option")
    page_numbers = [x["value"].split("/")[5] for x in pages]
    page_numbers = sorted(page_numbers, reverse=True)

    for no in page_numbers:
        await asyncio.sleep(3)
        page_url = url.format(page=no)
        async with httpx.AsyncClient() as client:
            page_content = await client.get(page_url)

        result = {"no": int(no), "url": page_url, "content": page_content.text}

        with open(f"datalake/質問主意書/{no}", mode="w") as f:
            data = json.dumps(result)
            f.write(data)

        get_content_govement_question.delay(**result)


async def stream_content():
    for content in storage:
        dic = json.loads(content)
        await asyncio.sleep(0)
        await get_content_govement_question.do(**dic)


@queue_transform.task
async def get_content_govement_question(
    es: es.AsyncElasticsearch = Depends(es.get_instance),
    loader=Depends(es.AsyncBulkInsert("共通スキーマ")),
    *,
    no: int,
    url: str,
    content: str,
):

    soup = BeautifulSoup(content, "html.parser")
    table = soup.select_one("#ContentsBox > .list_c")
    rows = list(table.select("tr"))
    # row_count = len(rows)

    def parse(rows):
        row_count = len(rows)
        current_row = 0
        content_row = 0
        while current_row < row_count:
            el = rows[current_row]
            if el.select("th")[0].text != "提出番号":
                raise Exception()

            try:

                title = el.select_one("td > a").text
                link = el.select_one("td > a")["href"]

                current_row += 1

                el = rows[current_row]
                提出者 = el.select_one("td.ta_l").text
                links = el.select("td > a")

                try:
                    質問本文 = None
                    質問本文 = links[0]["href"]
                    質問本文 = urljoin(url, 質問本文)
                except IndexError:
                    pass

                try:
                    答弁本文 = None
                    答弁本文 = links[1]["href"]
                    答弁本文 = urljoin(url, 答弁本文)
                except IndexError:
                    pass

                current_row += 2
                content_row += 1
            except Exception as e:
                raise

            提出者 = 提出者[:-1]  # 最後に「君：がついているので削除
            提出者 = Wakachi(提出者)

            result = {
                "row": content_row,
                "title": title,
                "提出者": 提出者,  # 最後に「君：がついているので削除
                "link_title": urljoin(url, link),
                "link_質問本文": 質問本文,
                "link_答弁本文": 答弁本文,
            }
            result = clean_text(result)
            # result["hash"] = hash("_".join(str(x) for x in result.values()))

            yield result

            logger.info(result)

    # async for ok, result in async_streaming_bulk(
    #     client=es, index="質問主意書", actions=parse(rows)
    # ):
    #     print(result)

    mapper = ({"質問主意書": x} for x in parse(rows))

    async for ok, result in loader(actions=mapper):
        print(result)


def clean_text(dic):
    title: str = dic["title"]
    title = title.replace("についての", "に関する")
    title = title.replace("に関しての", "に関する")
    title = title.replace("に対する", "に関する")
    title = title.replace("に対しての", "に関する")
    title = title.replace("再質問", "質問")
    title = title.replace("第三回質問", "質問")
    title = title.replace("第二回質問", "質問")

    title = title.replace("に関する質問主意書", "")
    title = title.replace("に関する質問", "")
    title = title.replace("に関する主意書", "")

    # title = title.replace("に関する再質問主意書", "")
    # title = title.replace("に関する質問", "")
    # title = title.replace("に関する再質問", "")
    # title = title.replace("に関する第三回質問主意書", "")
    # title = title.replace("に関しての質問主意書", "")
    # title = title.replace("に対する主意書", "")
    # title = title.replace("に対する質問主意書", "")
    # title = title.replace("に対する再質問主意書", "")
    # "に関する第三回質問"
    dic["title"] = title
    return dic
