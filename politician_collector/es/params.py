from elasticsearch_dsl import analyzer, tokenizer
from typing import Dict, Any
from typing import Any
from . import dictionaries

# https://www.elastic.co/jp/blog/how-to-implement-japanese-full-text-search-in-elasticsearch


class A(tuple):
    def __init__(self, iterable):
        pass


# class KeyValuePair(MappingProxyType):
#     def __init__(self, key: str, value):
#         super().__init__({key: value})
#         self.key = key
#         # self[key] = dic

#     @property
#     def value(self):
#         return self[self.key]


from collections.abc import MutableMapping


class KeyValuePair(MutableMapping):
    def __init__(self, key, value):
        self.mapping = {key: value}
        self.key = key

    def __setitem__(self, k, v) -> None:
        raise NotImplementedError()

    def __getitem__(self, key):
        return self.mapping[key]

    def __delitem__(self, key):
        raise NotImplementedError()

    def __iter__(self):
        return self.mapping.keys()

    def keys(self):
        return self.mapping.keys()

    def __len__(self):
        return len(self.mapping)

    @property
    def value(self):
        return self[self.key]


# K = TypeVar("K")
# V = TypeVar("V")


# class KeyValuePairBase(NamedTuple, Mapping[K, V]):
#     key: K
#     value: V

#     @property
#     def item(self):
#         return (self.key, self.value)

#     def __getitem__(self, key):
#         if self.key != key:
#             raise KeyError(key)
#         return self.value

#     def keys(self):
#         yield self.key

#     def values(self):
#         yield self.value

#     def items(self):
#         yield self


# def KeyValuePair(key: K, value: V) -> KeyValuePairBase[K, V]:
#     return KeyValuePairBase(key=key, value=value)  # type: ignore
charfilter_blank = KeyValuePair(
    "charfilter_blank",
    # {"type": "mapping", "mappings": dictionaries.char_mappings_blank},
    {"type": "mapping", "mappings": ["\u3000 => \s"]},  # TODO: 現在の定義では空文字は駄目だと怒られてしまう
)

charfilter_異体字 = KeyValuePair(
    "charfilter_異体字",
    {"type": "mapping", "mappings": dictionaries.char_mappings_異体字},
)

char_filter_ignore_blank = KeyValuePair(
    "char_filter_ignore_blank",
    {
        "type": "pattern_replace",
        "pattern": "(?<=[\\s\\p{P}])",
        # "pattern": "(?<=\\p{Lower})(?=\\p{Upper})",
        "replace": "",
    },
)

char_filter_normalize_blank = KeyValuePair(
    "char_filter_normalize_blank",
    {"type": "pattern_replace", "pattern": "(?<=[\\s\\p{P}])", "replace": " "},
)

charfilter_normalize = KeyValuePair(
    "charfilter_normalize",
    {
        "type": "icu_normalizer",
        "name": "nfkc",
        "mode": "compose",
    },
)

tokenizer_ja_kuromoji = KeyValuePair(
    "tokenizer_ja_kuromoji",
    {
        "mode": "search",
        "type": "kuromoji_tokenizer",
        "discard_compound_token": True,
        "user_dictionary_rules": dictionaries.dic_ja_popular
        + dictionaries.dic_ja_political,
    },
)

tokenizer_ja_ngram = KeyValuePair(
    "tokenizer_ja_ngram",
    {
        "type": "ngram",
        "min_gram": 2,
        "max_gram": 2,
        "token_chars": ["letter", "digit"],
    },
)

filter_ja_stopwords = KeyValuePair(
    "filter_ja_stopwords",
    {
        "type": "stop",
        "ignore_case": True,
        "stopwords": dictionaries.stopwords_ja_tag_cloud,
    },
)

filter_ja_index_synonym = KeyValuePair(
    "filter_ja_index_synonym",
    {
        "type": "synonym",
        "lenient": False,
        "synonyms": [],
    },
)

filter_ja_search_synonym = KeyValuePair(
    "filter_ja_search_synonym",
    {
        "type": "synonym_graph",
        "lenient": False,
        "synonyms": dictionaries.synonym_graph_ja,
    },
)

analyzer_index_name_ja_kuromoji = KeyValuePair(
    "analyzer_index_ja_kuromoji",
    {
        "type": "custom",
        "char_filter": [
            charfilter_normalize.key,
            charfilter_blank.key,
            charfilter_異体字.key,
        ],
        # "tokenizer": tokenizer_ja_kuromoji.key,
        "filter": [
            "trim",
            # "kuromoji_baseform",  # 動詞形容詞のノーマライズ（飲み⇛飲む）
            # "kuromoji_part_of_speech",  # 品詞のノーマライズ（おいしいね⇛おいしい）
            # filter_ja_index_synonym.key,
            "cjk_width",  # 全角半角等のノーマライズ
            # "ja_stop",
            # "kuromoji_stemmer",  # サーバー　⇛　サーバなど表記ゆれ対応は不要
            "lowercase",
            # filter_ja_stopwords.key,  # ゴミになりやすいキーワードの除去は不要
            # "kuromoji_readingform",  # ローマ字に正規化
        ],
    },
)

analyzer_search_name_ja_kuromoji = analyzer_index_name_ja_kuromoji


analyzer_index_ja_kuromoji = KeyValuePair(
    "analyzer_index_ja_kuromoji",
    {
        "type": "custom",
        "char_filter": [
            charfilter_normalize.key,
            charfilter_blank.key,
            charfilter_異体字.key,
        ],
        "tokenizer": tokenizer_ja_kuromoji.key,
        "filter": [
            "kuromoji_baseform",
            "kuromoji_part_of_speech",
            filter_ja_index_synonym.key,
            "cjk_width",
            "ja_stop",
            "kuromoji_stemmer",
            "lowercase",
            filter_ja_stopwords.key,
        ],
    },
)

analyzer_search_ja_kuromoji = KeyValuePair(
    "analyzer_search_ja_kuromoji",
    {
        "type": "custom",
        "char_filter": [
            charfilter_normalize.key,
            charfilter_blank.key,
            charfilter_異体字.key,
        ],
        "tokenizer": tokenizer_ja_kuromoji.key,
        "filter": [
            # "trim",
            "kuromoji_baseform",
            "kuromoji_part_of_speech",
            filter_ja_search_synonym.key,
            "cjk_width",
            "ja_stop",
            "kuromoji_stemmer",
            "lowercase",
            filter_ja_stopwords.key,
            # "kuromoji_readingform",  # ローマ字に正規化
        ],
    },
)

analyzer_index_ja_ngram = KeyValuePair(
    "analyzer_index_ja_ngram",
    {
        "type": "custom",
        "char_filter": [charfilter_normalize.key],
        "tokenizer": tokenizer_ja_ngram.key,
        "filter": ["lowercase"],
    },
)

analyzer_search_ja_ngram = KeyValuePair(
    "analyzer_search_ja_ngram",
    {
        "type": "custom",
        "char_filter": [charfilter_normalize.key],
        "tokenizer": tokenizer_ja_ngram.key,
        "filter": [filter_ja_search_synonym.key, "lowercase"],
    },
)


analyzer_url = KeyValuePair(
    # delimiter: /
    "analyzer_url",
    {"type": "custom", "tokenizer": "path_hierarchy"},
)


analysis_ja = {
    "analysis": {
        "char_filter": {**charfilter_normalize, **charfilter_blank, **charfilter_異体字},
        "tokenizer": {
            **tokenizer_ja_kuromoji,
            **tokenizer_ja_ngram,
        },
        "filter": {
            **filter_ja_stopwords,
            **filter_ja_index_synonym,
            **filter_ja_search_synonym,
        },
        "analyzer": {
            **analyzer_url,
            **analyzer_index_ja_kuromoji,
            **analyzer_search_ja_kuromoji,
            **analyzer_index_ja_ngram,
            **analyzer_search_ja_ngram,
        },
    }
}
