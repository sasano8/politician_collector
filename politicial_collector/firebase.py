import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Use a service account
cred = credentials.Certificate("secret_firebase.json")
firebase_admin.initialize_app(cred)


class FirestoreTransaction:
    """
    トランザクションは最大500件
    コレクションはドキュメントを１つずつ削除しなければいけない
    """

    def __init__(self):
        self.db = firestore.client()
        self.batch = self.db.batch()

    def collection(self, collection):
        return self.db.collection(collection)

    def document(self, document):
        return self.db.document(document)

    def get(self, collection, document):
        return self.db.collection(collection).document(document)

    def add(self, collection, doc: dict):
        return self.db.collection(collection).add(doc)

    def set(self, ref, **kwargs):
        return self.batch.set(ref, kwargs)

    def update(self, ref, **kwargs):
        return self.batch.update(ref, kwargs)

    def delete(self, ref):
        return self.batch.delete(ref)

    def commit(self):
        self.batch.commit()

    def rollback(self):
        # 存在しないリソースを指定して無理やり例外を発生させる
        try:
            self.batch.update("rollback", {})
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if not exc:
            self.db.commit()
        else:
            self.db.rollback()

    @classmethod
    def transaction(cls):
        instance = cls()
        try:
            yield instance
            instance.commit()
        except:
            raise
        finally:
            instance.rollback()


async def get_db():
    client = firestore.client()
    try:
        db = FirestoreTransaction()
        yield db
        db.commit()
    except:
        raise
    finally:
        db.rollback()
