import argparse

def filter_by_gc_content(file, max_gc, newfile):
    next_line_is_nucleotide = False
    last_sequence_passed_test = False
    newfile = open(newfile, 'w')
    prev_line = ""
    with open(file, 'r') as file:
        for line in file:
            if next_line_is_nucleotide:
                sequence = line.replace('\n', '')
                next_line_is_nucleotide = False
                if get_gc_content(sequence) <= max_gc:
                    last_sequence_passed_test = True
                    newfile.write("".join((prev_line, sequence, '\n')))

            elif last_sequence_passed_test:
                newfile.write(line)
                if '+' not in line[0]:
                    # newfile.write(get_gc_content(sequence))
                    last_sequence_passed_test = False
            if '@' in line[0] and len(line.split(' ')) > 1:
                next_line_is_nucleotide = True
                prev_line = line

    newfile.close()

def get_gc_content(sequence):
    num_nucleotides = len(sequence)
    total_gc = 0
    for nucleotide in sequence:
        if nucleotide == 'G' or nucleotide == 'C':
            total_gc += 1
    return (float(total_gc)/num_nucleotides)*100


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-input", "--input_file", type=str, help="input file")
    parser.add_argument("-maxgc", "--max_gc", type=int, help="maximum gc accepted for a read")
    parser.add_argument("-output", "--output_file", type=str, help="output file")
    args = parser.parse_args()
    filter_by_gc_content(args.input_file, args.max_gc, args.output_file)
