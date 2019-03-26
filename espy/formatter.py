from typing import List, Union

from .data import BlockType, WordBlock, Conjugation, Paradigm, ConjugationTable


class Format:
    RED = '\x1b[31m'
    END = '\033[0m'
    BOLD = '\033[1m'


def format_bold(string: str) -> str:
    return Format.BOLD + string + Format.END


def format_word(word: List[WordBlock]) -> str:
    string = ''
    for block in word:
        if block.type == BlockType.irregular:
            string += format_bold(block.content)
        else:
            string += block.content

    return string


def format_conjugation(conjugation: Conjugation, include_name: bool) -> str:
    forms = []
    for word in conjugation.forms:
        forms.append(format_word(word))

    if include_name:
        prefix = conjugation.name + ': '
    else:
        prefix = ''

    return prefix + ', '.join(forms)


def format_inf_participle(paradigm: Paradigm, conjugation_names: Union[None, List[str]],
                          include_names: bool) -> List[str]:
    lines = []
    if conjugation_names is None or paradigm.infinitive.name in conjugation_names:
        lines.append(format_conjugation(paradigm.infinitive, include_name=include_names))

    if conjugation_names is None or paradigm.present_participle.name in conjugation_names:
        lines.append(format_conjugation(paradigm.present_participle, include_name=include_names))

    if conjugation_names is None or paradigm.past_participle.name in conjugation_names:
        lines.append(format_conjugation(paradigm.past_participle, include_name=include_names))

    return lines


def format_table(table: ConjugationTable, conjugation_names: Union[None, List[str]], include_names: bool) -> List[str]:
    lines = []

    for conjugation in table.conjugations:
        if conjugation_names is None or conjugation.name in conjugation_names:
            lines.append(format_conjugation(conjugation, include_name=include_names))

    if include_names and len(lines):
        lines = [format_bold(table.name) + ':'] + lines

    return lines


def format_paradigm(paradigm: Paradigm, table_names: Union[None, List[str]], conjugation_names: Union[None, List[str]],
                    include_names: bool) -> List[List[str]]:
    blocks = []

    block = format_inf_participle(paradigm, conjugation_names=conjugation_names, include_names=include_names)
    if block:
        blocks.append(block)

    for table in paradigm.conjugation_tables:
        if table_names is None or table.name in table_names:
            block = format_table(table, conjugation_names=conjugation_names, include_names=include_names)
            if block:
                blocks.append(block)

    return blocks
