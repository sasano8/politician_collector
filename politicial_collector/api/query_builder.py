def build_for_name_search(
    *, index: str, size: int = 10, fields=["identity.person_name"], phrase: str
):
    return dict(
        index=index,
        body={
            "size": size,
            "fields": fields,
            "_source": False,
            "query": {
                "bool": {
                    "must": {"exists": {"field": "identity.person_id"}},
                    "filter": {
                        "multi_match": {
                            "fields": [
                                "identity.person_name.*",
                                "identity.person_name_kana.*",
                            ],
                            "type": "phrase",
                            "query": phrase,
                            "lenient": True,
                        }
                    },
                }
            },
        },
    )


def get_profile(*, index: str, id: str):
    return dict(
        index=index,
        body={
            "fields": [],
            "_source": True,
            "query": {"term": {"profile.id": id}},
        },
    )
