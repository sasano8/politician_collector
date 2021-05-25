# type: ignore
from .. import es


class identity:
    source_title = "identity.source_title"
    title = "identity.title"
    link = "identity.link"
    person_id = "identity.person_id"
    person_name = "identity.person_name"
    person_name_kana = "identity.person_name_kana"
    political_party = "identity.political_party"
    sex = "identity.sex"


# fmt: off
schemas = {
    "identity": {
        "properties": {
            "source_title": {**es.type.keyword},
            "title": {**es.type.keyword, **es.fields.ja},
            "link": {**es.type.keyword, **es.fields.url},
            "person_id": es.type.keyword,
            "person_name": {**es.type.keyword, **es.fields.ja},
            "person_name_kana": {**es.type.keyword, **es.fields.ja},
            "political_party": {**es.type.keyword, **es.fields.ja},
            "sex": {**es.type.keyword, **es.fields.ja},
        }
    },
    "documents": {
        "properties": {
            "title": {**es.type.keyword, **es.fields.ja},
            "link": {**es.type.keyword, **es.fields.url},
            "body": {**es.type.keyword, **es.fields.ja},
            "memo": {**es.type.keyword},
        }
    },
    "profile": {
        "properties": {
            "id": {**es.type.keyword, "copy_to": identity.person_id},
            "議員氏名": {**es.type.keyword, "copy_to": identity.person_name},
            "議員氏名読み方": {**es.type.keyword, "copy_to": identity.person_name_kana},
            "会派": {**es.type.keyword,  "copy_to": identity.political_party},
            "性別": {**es.type.keyword, "copy_to": identity.sex},
            "本名": {**es.type.keyword, "copy_to": identity.person_name},
            "本名読み方": {**es.type.keyword, "copy_to": identity.person_name_kana},
            "別名": {**es.type.keyword, "copy_to": identity.person_name},
            "備考": es.type.keyword
        }
    },
    "衆議院議員一覧": {
        "properties":{
            # "source_title": {**es.type.const, "value": "衆議院議員一覧", "copy_to": identity.source_title},
            "link": {**es.type.keyword,  "copy_to": identity.link},
            "氏名": {**es.type.keyword, "copy_to": identity.person_name},
            "ふりがな": {**es.type.keyword,  "copy_to": identity.person_name_kana},
            # "本名": {**es.type.keyword,  "copy_to": identity.person_name},
            "会派": {**es.type.keyword,  "copy_to": identity.political_party},
            "選挙区": {**es.type.keyword},
            "当選回数": {**es.type.keyword},
        }
    },
    "参議院議員一覧": {
        "properties":{
            # "source_title": {**es.type.const, "value": "参議院議員一覧", "copy_to": identity.source_title},
            "議員氏名": {**es.type.keyword, "copy_to": identity.person_name},
            "読み方": {**es.type.keyword, "copy_to": identity.person_name_kana},
            "本名": {**es.type.keyword, "copy_to": identity.person_name},
            "性別": {**es.type.keyword, "copy_to": identity.sex},
            "会派": {**es.type.keyword, "copy_to": identity.political_party},
            "選挙回次等": {**es.type.keyword},
            "選挙区（最終）": {**es.type.keyword},
            "備考": {**es.type.keyword},
        }
    },
    "最新参議院議員一覧": {
        "properties":{
            # "source_title": {**es.type.const, "value": "参議院議員一覧", "copy_to": identity.source_title},
            "link": {**es.type.keyword,  "copy_to": identity.link},
            "議員氏名": {**es.type.keyword, "copy_to": identity.person_name},
            "本名": {**es.type.keyword, "copy_to": identity.person_name},
            "読み方": {**es.type.keyword, "copy_to": identity.person_name_kana},
            "会派": {**es.type.keyword, "copy_to": identity.political_party},
            "選挙区": {**es.type.keyword},
            "任期満了": {**es.type.keyword},
            "正字": {**es.type.keyword}
        }
    },
    "質問主意書": {
        "properties":{
            # "source_title": {**es.type.const, "value": "質問主意書", "copy_to": identity.source_title},
            "row": es.type.integer,
            # "title": {**es.type.keyword, **es.fields.ja},
            "title": {**es.type.keyword, "copy_to": identity.title},
            "提出者": {**es.type.keyword, "copy_to": identity.person_name},
            "link_title": {**es.type.keyword, "copy_to": identity.link},
            "link_質問本文": {**es.type.keyword, "copy_to": identity.link},
            "link_答弁本文": {**es.type.keyword, "copy_to": identity.link},
        }
    },
}

共通スキーマ = {
    "index": "共通スキーマ",
    "settings": es.params.analysis_ja,
    "mappings": {"dynamic": "strict", "properties": schemas},
}


political_profile ={
    "index": "political_profile",
    "settings": es.params.analysis_ja,
    "mappings": {"dynamic": "strict", "properties": schemas},
}

political_document ={
    "index": "political_document",
    "settings": es.params.analysis_ja,
    "mappings": {"dynamic": "strict", "properties": schemas},
}
