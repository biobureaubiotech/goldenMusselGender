while read p; do
  samtools faidx /home/joao_nunes/genomes/lf6_scaffolds.fasta "$p"
done <lf6_discovar_simplified_scaffolds.txt
