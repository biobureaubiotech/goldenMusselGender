import argparse 

parser = argparse.ArgumentParser(description='Process delta files to extract target scaffold')
parser.add_argument('--input_file')
parser.add_argument('--scaffold_id')
parser.add_argument('--output_file')

args = parser.parse_args()

target_scaffold = False
line_counter = 1

with open (args.input_file) as f:
    lines = f.readlines()

with open(args.output_file, "w") as f_output:    
    for line in lines:
        if ">" in line and args.scaffold_id in line:
            target_scaffold = True
        if ">" in line and args.scaffold_id not in line:
            target_scaffold = False
        if target_scaffold or line_counter <=2:
            f_output.write(line)
        line_counter +=1

f_output.close()
f.close()
        
