from functools import partial
from elasticsearch import AsyncElasticsearch
from ..config import ElasticSearchConfig
from elasticsearch.helpers import async_streaming_bulk

config = ElasticSearchConfig()
cloud_id = config.ES_CLOUD_ID
user = config.ES_USER
secret = config.ES_SECRET


def AsyncBulkInsert(index: str):
    async def get_bulk(cloud_id, user, secret):
        try:
            instance = AsyncElasticsearch(cloud_id=cloud_id, http_auth=(user, secret))
            yield partial(async_streaming_bulk, client=instance, index=index)
        except:
            raise
        finally:
            await instance.close()

    return partial(get_bulk, cloud_id=cloud_id, user=user, secret=secret)


async def get_instance():
    try:
        instance = AsyncElasticsearch(cloud_id=cloud_id, http_auth=(user, secret))
        yield instance
    except:
        raise
    finally:
        await instance.close()


async def helth():
    async for es in get_instance():
        return await es.cluster.health()


async def put_index(index: str, settings: dict = None, mappings: dict = None):
    settings = settings or {}
    mappings = mappings or {}

    body = {
        "settings": settings,
        "mappings": mappings,
    }

    with open("esmapping.json", "w") as f:
        import json

        s = json.dumps(body, ensure_ascii=False)
        f.write(s)

    async for es in get_instance():
        try:
            if exists := await es.indices.exists(index=index):
                await es.indices.delete(index=index)

            await es.indices.create(index=index, body=body)
        except Exception as e:
            raise

        #     try:
        #         # await es.indices.close(index)
        #         await es.indices.put_settings(index=index, body=body)
        #     finally:
        #         pass
        #         await es.indices.open(index)
        # else:
        #     await es.indices.create(index=index, body=body)


async def query(index: str):
    async for es in get_instance():
        es.search(index=index)
