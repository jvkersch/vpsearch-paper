.PHONY: blast-query ggsearch-query vpsearch-query time-commands all

blast-query:
	blastn -outfmt 6 -query mothur-sop-asv_232.fasta -db ../data/silva-all.fa -max_target_seqs 4 -num_threads 4 -task blastn -reward 1 | tee blast-232.txt

ggsearch-query:
	ggsearch36 -3 -b 4 -m 8C -T 4 mothur-sop-asv_232.fasta ../data/silva-all.fa | tee ggsearch-232.txt

vpsearch-query:
	vpsearch query -j4 ../data/silva-all.db/ mothur-sop-asv_232.fasta | tee vpsearch-232.txt

nmslib-query:
	python ../scripts/vpsearch-nmslib.py ../data/silva-all.fa mothur-sop-asv_232.fasta -r 1 | tee nmslib-232.txt

time-commands:
	for db in silva-100 silva-1000 silva-10000 silva-100000 silva-all; do \
		python time-command.py ggsearch ../data/$${db}.fa --query mothur-sop-asv_232.fasta --timings-file timings-ggsearch-$${db}.txt ; \
		python time-command.py blast ../data/$${db}.fa --query mothur-sop-asv_232.fasta --timings-file timings-blast-$${db}.txt ; \
		python time-command.py vpsearch ../data/$${db}.db --query mothur-sop-asv_232.fasta --timings-file timings-vpsearch-$${db}.txt ; \
		python ../scripts/vpsearch-nmslib.py ../data/$${db}.fa mothur-sop-asv_232.fasta --timings-file timings-nmslib-$${db}.txt ; \
	done

all: vpsearch-query ggsearch-query blast-query nmslib-query
