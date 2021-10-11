import argparse

import parasail

# The default scoring parameters were taken from fasta-36.3.7
#  match = +5
#  mismath = -4
#  gap_open = -12
#  gap_extend = -4


def breaks(s, length=75):
    for i in range(0, len(s), length):
        yield s[i : i + length]


def align(s1, s2):
    result = parasail.nw_trace(s1, s2, 12, 4, parasail.nuc44)
    traceback = result.traceback

    for q, c, r in zip(
        breaks(traceback.query), breaks(traceback.comp), breaks(traceback.ref)
    ):
        print(q)
        print(c)
        print(r)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("seq1")
    p.add_argument("seq2")
    ns = p.parse_args()

    align(ns.seq1, ns.seq2)


if __name__ == "__main__":
    main()
