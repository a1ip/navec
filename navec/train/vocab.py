
import sys

from .s3 import upload as vocab_upload  # noqa
from .s3 import download as vocab_download  # noqa
from .glove import (
    Glove,
    parse_glove_vocab
)


def vocab_count(args):
    glove = Glove.from_env()
    glove.vocab(sys.stdin.buffer, sys.stdout.buffer)


def vocab_quantile(args):
    records = vocab_quantile_(sys.stdin.buffer)
    for share, index in records:
        print('%0.3f\t%d' % (share, index))


SHARES = [
    0.5, 0.6, 0.7, 0.8, 0.9,
    0.91, 0.92, 0.93, 0.94,
    0.95, 0.96, 0.97, 0.98,
    0.99, 1.0
]


def pop(items):
    return items[0], items[1:]


def vocab_quantile_(lines, shares=SHARES):
    if not shares:
        return

    records = parse_glove_vocab(lines)
    counts = [count for _, count in records]

    total = sum(counts)
    accumulator = 0

    shares = sorted(shares)
    share, shares = pop(shares)

    counts = sorted(counts, reverse=True)
    for index, count in enumerate(counts):
        if accumulator / total >= share:
            yield share, index
            if not shares:
                break
            share, shares = pop(shares)
        accumulator += count