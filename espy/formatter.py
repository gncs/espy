from typing import List

from .data import BlockType, WordBlock, Conjugation


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


def format_conjugation(conjugation: Conjugation) -> str:
    forms = []
    for word in conjugation.forms:
        forms.append(format_word(word))

    return conjugation.name + ': ' + ', '.join(forms)
