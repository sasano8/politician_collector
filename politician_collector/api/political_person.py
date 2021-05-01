from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from .. import es
from ..firebase import get_db, FirestoreTransaction
from .query_builder import build_for_name_search

router = APIRouter()


class Person(BaseModel):
    name: str
    real_name: str
    birth_at: str
    socials: list


@router.get("/get")
def get_person(db: FirestoreTransaction = Depends(get_db), *, id: str):
    """政治家のプロフィールを取得する"""
    collection = db.collection("political_persons")
    ref = collection.document(id)
    doc = ref.get()
    if not doc.exists:
        raise Exception()
    else:
        return doc.to_dict()


@router.post("/create")
def create_person(db: FirestoreTransaction = Depends(get_db), *, person: Person):
    """政治家のプロフィールを作成する"""
    collection = db.collection("political_persons")
    dic = {"id": str(uuid4()), **person.dict()}
    ref = collection.document(dic["id"])
    ref.set(dic)
    result = collection.document(dic["id"]).get()
    return result.to_dict()


@router.put("/update")
def update_person(
    db: FirestoreTransaction = Depends(get_db), *, id: str, person: Person
):
    """政治家のプロフィールを更新する"""
    collection = db.collection("political_persons")
    ref = collection.document(id)
    ref.set(person.dict(exclude_unset=True), merge=True)
    result = collection.document(id).get()
    return result.to_dict()


@router.delete("/delete")
def delete_person(db: FirestoreTransaction = Depends(get_db), *, id: str):
    """政治家のプロフィールを削除する"""
    collection = db.collection("political_persons")
    ref = collection.document(id)
    doc = ref.get()
    if not doc.exists:
        return 0
    else:
        ref.delete()
        return 1


@router.get("/search_profile")
async def search_profile(
    db: es.AsyncElasticsearch = Depends(es.get_instance),
    *,
    議員氏名: str,
    size: int = 10,
):
    """名前にマッチする政治家のプロフィール一覧を返す"""
    query = build_for_name_search(
        index="共通スキーマ", fields=["identity.person_name"], size=size, phrase=議員氏名
    )
    result = await db.search(**query)
    return result


@router.get("/suggest_name")
async def suggest_name(
    db: es.AsyncElasticsearch = Depends(es.get_instance), *, phrase: str, size: int = 10
):
    """フレーズにマッチする政治家の名前一覧を返す"""
    result = await search_profile(db=db, 議員氏名=phrase, size=size)
    names = set()
    for hit in result["hits"]["hits"]:
        for item in hit["fields"]["identity.person_name"]:
            names.add(item)

    return names


@router.get("/search_documents")
async def search_documents(
    db: es.AsyncElasticsearch = Depends(es.get_instance),
    *,
    freeword: str,
    size: int = 50,
):
    """条件にヒットするドキュメントを返す。
    ダブルクオーテーションで囲むとフレーズマッチとなり、囲まないと曖昧検索となる。
    AND OR - () などがクエリで使えます。
    例：
    "人物1" AND ("政治" OR "経済" OR -"社会")
    """
    query = dict(
        index="共通スキーマ",
        body={
            "size": size,
            "fields": ["identity.*"],
            "_source": False,
            "query": {
                "query_string": {
                    "type": "phrase",
                    "fields": ["identity.*"],
                    "query": freeword,
                }
            },
        },
    )
    return await db.search(**query)


# -で除外
# OR AND
