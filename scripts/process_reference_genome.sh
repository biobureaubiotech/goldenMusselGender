while read p; do
  samtools faidx /home/joao_nunes/genomes/LF.genome.fasta "$p"
done <13_reference_scaffolds.txt
