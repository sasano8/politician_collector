from . import params

disable = {"enabled": False}
keyword = {"type": "keyword"}
const = {"type": "constant_keyword", "value": ""}
text = {"type": "text"}
integer = {"type": "integer"}

text_url = {**text, "analyzer": params.analyzer_url.key}

text_ja = {
    **text,
    "analyzer": params.analyzer_index_ja_kuromoji.key,
    "search_analyzer": params.analyzer_search_ja_kuromoji.key,
    "fielddata": True,
}

text_ja_ngram = {
    **text,
    "analyzer": params.analyzer_index_ja_ngram.key,
    "search_analyzer": params.analyzer_search_ja_ngram.key,
}
