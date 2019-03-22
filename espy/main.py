import argparse
from typing import List

import bs4
import requests

from espy.data import Paradigm
from espy.formatter import format_conjugation, format_word, format_bold
from espy.parser import parse_paradigm
from espy.version import __version__

CONJUGATION_URL = 'https://www.spanishdict.com/conjugate/'


class EspyException(Exception):
    """Main exception thrown by this program"""


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='espy',
        description='Get Conjugation Tables of Spanish Verbs in Your Terminal',
    )

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    parser.add_argument('verb', type=str, help='verb to be conjugated')

    parser.add_argument(
        '--all',
        dest='print_all',
        action='store_true',
        default=False,
        required=False,
        help='print all conjugation tables')

    return parser


def get_url(verb: str) -> str:
    return CONJUGATION_URL + verb


def get_page(url: str) -> bytes:
    try:
        return requests.get(url).content
    except requests.exceptions.RequestException:
        raise EspyException('Cannot fetch page for ' + url)


def get_soup(response_content: bytes) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(response_content, features='html.parser')


def print_paradigm(paradigm: Paradigm, black_list: List[str]) -> None:
    print('Infinitive: ' + format_word(paradigm.infinitive))
    print('Present Participle: ' + format_word(paradigm.present_participle))
    print('Past Participle: ' + format_word(paradigm.past_participle))

    # Conjugation tables
    for table in paradigm.conjugation_tables:
        if table.name in black_list:
            continue

        print('\n' + format_bold(table.name) + ':')
        for conjugation in table.conjugations:
            print(format_conjugation(conjugation))


def hook() -> None:
    args = create_parser().parse_args()

    url = get_url(args.verb)
    page = get_page(url)
    soup = get_soup(page)

    paradigm = parse_paradigm(soup)

    if args.print_all:
        black_list = []  # type: List[str]
    else:
        black_list = ['Continuous (Progressive)', 'Perfect', 'Perfect Subjunctive']

    print_paradigm(paradigm, black_list=black_list)


if __name__ == '__main__':
    hook()
