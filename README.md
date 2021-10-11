# Getting started

## Creating the Python environment

We assume that you have the Conda or EDM Python package manager available. This
repository comes with environment files that will let you install a Conda or
EDM environment to reproduce the results in the paper.

### Conda setup

From the root of the repository, create a new environment via
```console
conda env create --file scripts/environment.yml
```

This will create a Python environment called `vpsearch-testbed` that can be
activated via `conda activate vpsearch-testbed`. For the remainer of this file,
all instructions should be run from within this environment.

### EDM setup

An alternative to Conda is to use the [Enthought Deployment
Manager](https://assets.enthought.com/downloads/edm/). To create a Python
environment using EDM, run the following command:
```console
edm envs import -f scripts/vpsearch-testbed.json vpsearch-testbed

```

This Python environment can be activated via `edm shell -e vpsearch-testbed`.

## Installing Parasail

Parasail is a C++ library for fast sequence alignment. To install it, follow
the instructions in the [GitHub
repository](https://github.com/jeffdaily/parasail). The EDM environment comes
with Parasail already installed.

Note that Parasail relies on the presence of specific CPU instruction sets for
SIMD (most notably AVX2 and AVX512). The benchmarks were obtained on a
reasonably modern CPU with some subset of the AVX512 instructions.

## Installing vpsearch

Assuming that Parasail has been installed, vpsearch can installed from source via
```console
pip install vpsearch
```

## Installing NMSLIB

Some of the benchmark scripts use a customized version of the NMSLIB
package. To install this version of the library, first ensure that Parasail is
installed in a standard location (e.g. `/usr/local/`). It should then be
sufficient to install NMSLIB by cloning our forked repository and installing
the Python bindings:

```console
git clone https://github.com/jvkersch/nmslib
cd nmslib/python_bindings
git checkout space-nw
python setup.py install

```

# Preparing the input databases

## Generating the database indices

From within the activated Python environment, run the following command:

```console
    (cd data && make indices)
```

## Regenerating the v4 database (optional)

The benchmark scripts rely on specially prepared versions of the Silva
database, containing deduplicated v4 regions of the full 16S sequences. This
prepared database has been checked in to this repository and can be used
as-is.

To regenerate the databases, download the v138 version of the Silva database
from [Zenodo](https://zenodo.org/record/4587955) and place it in the `data/`
directory. Also install the [RDPTools](https://github.com/rdpstaff/RDPTools)
suite. Once this is done, modify the `RDPTOOLS` variable in `data/Makefile` to
point to your RDPTools installation. To regenerate the v4 database, run

```console
    (cd data && make v4-database)
```

# Running the benchmark suite

The benchmark tool suite is driven by a Makefile in the query directory. It is
entirely text based, and relies for its interpretation on a number of Jupyter
notebooks described in the next section.

Note that the data obtained to produce the figures in the paper is already
checked in to this repository.

## Running the timing scripts

From within the activated Python environment, run
```console
    (cd query && make time-commands)
```

This command runs all tools (vpsearch, Blast+, ggsearch36, and nmslib) in
single-threaded mode on each subsampled database. Each command is invoked 7
times and for each run the total execution time is recorded in a text file in
the `query/` directory.

This command takes 6-10 hours to run to completion.

## Running the taxonomic accuracy scripts

From within the activated Python environment, run
```console
    (cd query && make all)
```

This command will run each tool to look up all 232 ASV on the full Silva
database, and store the results of the lookup in a text file.

# Running the comparison notebooks

There are 3 Jupyter notebooks available to regenerate the figures and results
from the paper and supplementary information. From within the Python
environment, run `jupyter notebook` to start the notebook server

## compare-timings.ipynb

Creates the figures with timing information (figure (1) in the paper and figure
(1) in the supplementary information) based on timing results obtained from the
benchmark scripts.

## compare-taxonomy.ipynb

Analyzes the results of the taxonomic lookup benchmark step, and reports on the
number of differently-assigned sequences.

## analyze-reduced-database.ipynb (optional)

This is a quality-control notebook to inspect the reduced v4 database that is
used by vpsearch. In particular, the notebook reports the number of sequences
that did not have the v4 primers in the expected location, a number that is
also reported in the paper (9.50%).
