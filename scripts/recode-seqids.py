import argparse
import os

from Bio import SeqIO


def parse_filename(input_fasta):
    base, ext = os.path.splitext(input_fasta)
    return f"{base}-recoded{ext}", "seqids.tsv"


def foo(input_fasta):
    seqs = SeqIO.parse(input_fasta, "fasta")
    for n, seq in enumerate(seqs):
        name = seq.name
        seq.name = seq.id = str(n)
        seq.description = ""
        yield (seq, name)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input_fasta")
    ns = p.parse_args()

    output_fasta, seqids = parse_filename(ns.input_fasta)

    print(output_fasta, seqids)

    with open(output_fasta, "w") as output_fp:
        with open(seqids, "w") as seqids_fp:
            for seq, name in foo(ns.input_fasta):
                SeqIO.write(seq, output_fp, "fasta-2line")
                seqids_fp.write(name + "\n")


if __name__ == "__main__":
    main()
