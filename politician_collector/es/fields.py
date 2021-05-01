from . import types

url = {
    "fields": {
        "analyzed": types.text_url,
    }
}


ja = {
    "fields": {
        # "raw": types.keyword,
        "ja": types.text_ja,
        "ja_ngram": types.text_ja_ngram,
    }
}
