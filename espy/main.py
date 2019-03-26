import argparse

import bs4
import requests

from espy.formatter import format_paradigm
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
        '--no-names',
        dest='no_names',
        action='store_true',
        default=False,
        help="don't print conjugation and table names")

    selection_group = parser.add_argument_group(title='selection')
    selection_group.add_argument(
        '--table',
        required=False,
        action='append',
        help='select conjugation table',
    )

    selection_group.add_argument(
        '--conjugation',
        required=False,
        action='append',
        help='select conjugation',
    )

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


def hook() -> None:
    args = create_parser().parse_args()

    url = get_url(args.verb)
    page = get_page(url)
    soup = get_soup(page)

    paradigm = parse_paradigm(soup)

    include_names = not args.no_names
    blocks = format_paradigm(
        paradigm, table_names=args.table, conjugation_names=args.conjugation, include_names=include_names)

    print('\n\n'.join(['\n'.join(block) for block in blocks]))


if __name__ == '__main__':
    hook()
