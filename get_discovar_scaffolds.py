import sys
num_scaffolds = 0

with open("/home/joao_nunes/nucmer4_alignment/out.delta.show-tiling") as f:
    lines = f.readlines()
    for line in lines:
        if ">" not in line:
            scaffold_id = line.split("\t")[-1]
            sys.stdout.write(scaffold_id)
        else:
            num_scaffolds += 1
        if num_scaffolds >= 13:
            break
