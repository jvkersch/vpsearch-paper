import argparse
import contextlib
import logging
import os
import time
import sys

from Bio import SeqIO
import nmslib  # Requires a custom build of nmslib with parasail support


from vpsearch._vpsearch import MatchRecord  # For BLAST-6 output


def _safe_rm(fname):
    try:
        os.remove(fname)
    except FileNotFoundError:
        pass


@contextlib.contextmanager
def timing():
    class Ctx:
        pass

    c = Ctx()
    try:
        start = time.time()
        yield c
    finally:
        c.delta = time.time() - start


def main():
    p = argparse.ArgumentParser()
    p.add_argument("seqdb")
    p.add_argument("query")
    p.add_argument("--timings-file")
    p.add_argument("-r", type=int, default=7, help="Number of repeats")
    ns = p.parse_args()

    _safe_rm(ns.timings_file)

    sequences = parse_sequences(ns.seqdb)
    queries = parse_sequences(ns.query)

    index = build_index(sequences)

    for _ in range(ns.r):
        with timing() as ctx:
            for (_, query_id), query in queries:
                for match in lookup_sequences(index, query, sequences):
                    print(f"{query_id.decode()}\t{match}")

        if ns.timings_file:
            with open(ns.timings_file, "a") as fp:
                fp.write(f"{ctx.delta}\n")

        print(ctx.delta)


def _enc(d):
    return str(d).encode("ascii")


def parse_sequences(seqdb):
    """Read in sequence database in similar format as Parasail."""
    return [((None, _enc(s.id)), _enc(s.seq)) for s in SeqIO.parse(seqdb, "fasta")]


def build_index(sequences):
    """Build VPTree search index."""
    index = nmslib.init(
        method="vptree",
        space="nw",
        dtype=nmslib.DistType.INT,
        data_type=nmslib.DataType.OBJECT_AS_STRING,
    )
    index.addDataPointBatch([seq[1] for seq in sequences])

    with timing() as ctx:
        index.createIndex(
            print_progress=True,
            index_params={"bucketSize": 1, "selectPivotAttempts": 1},
        )
    print(ctx.delta)

    # index.saveIndex("vptree.bin", save_data=True)  # Not supported for VPTree
    return index


def lookup_sequences(index, query, sequences, k=4):
    """Run k-nearest neighbors on a pre-built index."""
    match_idxs, distances = index.knnQuery(query, k=k)
    matches = [sequences[i] for i in match_idxs]
    records = [MatchRecord.align(_enc(query), seq) for seq in matches]
    records.sort(key=lambda r: -r.matchpct)
    return records


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
