# Input and output files
input_file = "../../utils/wydarzenia_input.txt"
output_file = "wydarzenia_copy_ready.txt"

with (
    open(input_file, "r", encoding="utf-8") as f_in,
    open(output_file, "w", encoding="utf-8") as f_out,
):
    for line in f_in:
        line = line.rstrip("\n")
        columns = line.split("\t")

        # Ensure third column (opis) is '""' if empty
        if len(columns) < 3 or columns[2].strip() == "":
            if len(columns) < 3:
                # pad columns if needed
                while len(columns) < 3:
                    columns.append('""')
            else:
                columns[2] = '""'

        # Ensure fifth column (link) exists and is '""' if missing
        if len(columns) < 5:
            while len(columns) < 5:
                columns.append('""')

        f_out.write("\t".join(columns[:5]) + "\n")

print(f"Processed {input_file} -> {output_file}")
