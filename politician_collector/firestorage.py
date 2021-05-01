from google.cloud import storage
from google.cloud.storage.bucket import Bucket
from politician_collector.config import FirebaseConfig

config = FirebaseConfig()
config.set_env()
app = storage.Client()


def get_instance() -> Bucket:
    app = storage.Client()
    bucket = app.bucket(config.DEFAULT_BUCKET)
    bucket.storage_class = "STANDARD"
    return bucket


async def get_storage():
    instance = get_instance()
    try:
        yield instance
    except:
        raise
    finally:
        ...
