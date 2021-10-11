SHELL := bash

.PHONY: v4-database sample-databases indices

RDPTOOLS="${HOME}/src/RDPTools/ProbeMatch.jar"

v4-database:
	python ../scripts/recode-seqids.py silva_nr99_v138.1_wSpecies_train_set.fa
	java -jar ${RDPTOOLS} v4-primers-rev.fa silva_nr99_v138.1_wSpecies_train_set-recoded.fa > primer-locs.tsv
	python ../scripts/cut-primers.py primer-locs.tsv silva_nr99_v138.1_wSpecies_train_set-recoded.fa > silva-all.fa
	python ../scripts/dedup.py silva-all.fa > silva-dedup.fa
	gzip -c silva-dedup.fa > silva-all.fa.gz

sample-databases:
	seqtk sample -s 1234 silva-all.fa.gz 100 | gzip -f > silva-100.fa.gz
	seqtk sample -s 1234 silva-all.fa.gz 1000 | gzip -f > silva-1000.fa.gz
	seqtk sample -s 1234 silva-all.fa.gz 10000 | gzip -f > silva-10000.fa.gz
	seqtk sample -s 1234 silva-all.fa.gz 100000 | gzip -f > silva-100000.fa.gz

indices:
	for db in silva-100 silva-1000 silva-10000 silva-100000 silva-all; do \
		echo $${db} ; \
		gunzip -c $${db}.fa.gz > $${db}.fa ; \
		vpsearch build --force $${db}.fa ; \
		makeblastdb -in $${db}.fa -dbtype nucl ; \
	done
