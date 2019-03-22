import collections
import enum


class BlockType(enum.Enum):
    regular = 1
    irregular = 2


WordBlock = collections.namedtuple('WordBlock', ['content', 'type'])

Conjugation = collections.namedtuple('Conjugation', ['name', 'forms'])

ConjugationTable = collections.namedtuple('ConjugationTable', ['name', 'conjugations'])

Paradigm = collections.namedtuple('Paradigm', [
    'infinitive',
    'past_participle',
    'present_participle',
    'conjugation_tables',
])
