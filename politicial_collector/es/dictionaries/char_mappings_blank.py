import ja_text_cleaner


_tmp = {
    *ja_text_cleaner.mappings.blank,
    *ja_text_cleaner.mappings.tab,
    *ja_text_cleaner.mappings.newline,
}

_tmp.remove(" ")


def str_to_raw(val):
    v = repr(val)  # repr("\t")  => "'\\t'"
    v = v[1:-1]
    return v


char_mappings_blank = [(f"{str_to_raw(x)} => \\s") for x in _tmp]
