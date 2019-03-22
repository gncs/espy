from typing import List

import bs4

from .data import WordBlock, BlockType, Conjugation, ConjugationTable, Paradigm


def parse_word(tag: bs4.Tag) -> List[WordBlock]:
    blocks = []

    for child in tag.children:
        if isinstance(child, bs4.element.NavigableString):
            blocks.append(WordBlock(content=str(child), type=BlockType.regular))
        else:
            blocks.append(WordBlock(content=''.join(child.contents), type=BlockType.irregular))

    return blocks


def parse_infinitive(soup: bs4.BeautifulSoup) -> List[WordBlock]:
    return parse_word(soup.find('div', id='headword-es'))


def parse_present_participle(soup: bs4.BeautifulSoup) -> List[WordBlock]:
    return parse_word(soup.find('span', attrs={'data-tense': 'presentParticiple'}))


def parse_past_participle(soup: bs4.BeautifulSoup) -> List[WordBlock]:
    return parse_word(soup.find('span', attrs={'data-tense': 'pastParticiple'}))


def parse_table_names(soup: bs4.BeautifulSoup) -> List[str]:
    names = []
    for item in soup.find_all('span', attrs={'class': 'vtable-label-link-text'}):
        names.append(''.join(item.contents))
    return names


def parse_head_row(row: bs4.Tag) -> List[str]:
    empty = row.find('td', attrs={'class': 'vtable-empty'})
    assert empty

    tenses = []
    for column in row.find_all('td', attrs={'class': 'vtable-title'}):
        tense = column.find('span', attrs={'class': 'vtable-title-link-text'})
        tenses.append(''.join(tense.contents))

    return tenses


DASH_SYMBOL = '-'
dash_block = WordBlock(content=DASH_SYMBOL, type=BlockType.regular)


def parse_body_row(row: bs4.Tag) -> List[List[WordBlock]]:
    pronoun = row.find('td', attrs={'class': 'vtable-pronoun'})
    assert pronoun

    words = []
    for item in row.find_all('td', attrs={'class': 'vtable-word'}):
        element = item.find('div', attrs={'class': 'vtable-word-contents'})

        if element.contents == [DASH_SYMBOL]:
            words.append([dash_block])

        else:
            word = element.find(['a', 'div'], attrs={'class': 'vtable-word-text'})
            words.append(parse_word(word))

    return words


def parse_table(table: bs4.Tag) -> List[Conjugation]:
    head_row = table.find('tr', attrs={'class': 'vtable-head-row'})
    headers = parse_head_row(head_row)

    rows = []
    for row in table.find_all('tr', attrs={'class': 'vtable-body-row'}):
        rows.append(parse_body_row(row))

    assert all([len(headers) == len(row) for row in rows])

    conjugations = []
    for column, head in enumerate(headers):
        conjugations.append(Conjugation(
            name=head,
            forms=[row[column] for row in rows],
        ))

    return conjugations


def parse_tables(soup: bs4.BeautifulSoup) -> List[List[Conjugation]]:
    tables = []

    for table_tag in soup.find_all('div', attrs={'class': 'vtable-wrapper'}):
        tables.append(parse_table(table_tag))

    return tables


def parse_paradigm(soup: bs4.BeautifulSoup) -> Paradigm:
    table_names = parse_table_names(soup)
    tables = parse_tables(soup)
    assert len(table_names) == len(tables)

    conjugation_tables = []
    for table_name, conjugations in zip(table_names, tables):
        conjugation_tables.append(ConjugationTable(
            name=table_name,
            conjugations=conjugations,
        ))

    return Paradigm(
        infinitive=parse_infinitive(soup),
        past_participle=parse_past_participle(soup),
        present_participle=parse_present_participle(soup),
        conjugation_tables=conjugation_tables,
    )
