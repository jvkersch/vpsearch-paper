import argparse
import logging
import subprocess
import time

CMDS = {
    "vpsearch": "vpsearch query -j1 {db} {query}",
    "ggsearch": "ggsearch36 -3 -b 4 -m 8C -T 1 {query} {db}",
    "blast": "blastn -outfmt 6 -query {query} -db {db} -max_target_seqs 4 -num_threads 4 -task blastn -reward 1",  # noqa
}

logger = logging.getLogger(__name__)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("tool")
    p.add_argument("database")
    p.add_argument("--query", default="mothur-sop-asv_232.fasta")
    p.add_argument("--number", default=7, type=int)
    p.add_argument("--timings-file", default="timings.txt")
    ns = p.parse_args()
    return ns.tool, ns.database, ns.query, ns.number, ns.timings_file


def run_tool(tool, db, query):
    cmd = CMDS[tool].format(db=db, query=query)

    try:
        start = time.monotonic()
        subprocess.run(cmd, shell=True, check=True)
        delta = time.monotonic() - start
    except subprocess.CalledProcessError:
        logger.exception("Exception during command execution:")
        delta = -1

    return delta


def save_deltas(fname):
    with open(fname, "w", encoding="utf-8") as fp:
        while True:
            try:
                delta = yield
                fp.write(f"{delta}\n")
                fp.flush()
            except StopIteration:
                break


def main():
    logging.basicConfig()

    tool, db, query, n, timings_file = parse_args()
    output = save_deltas(timings_file)
    next(output)

    for _ in range(n):
        delta = run_tool(tool, db, query)
        output.send(delta)

    output.close()


if __name__ == "__main__":
    main()
