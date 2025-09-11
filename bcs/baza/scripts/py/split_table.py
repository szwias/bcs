import sys


def split_columns(input_file, output_main, output_removed):
    """
    Reads a tab-separated file with extra columns and splits it into two:
    - output_main: id, data_zakonczenia, typ_wydarzenia_id, typ_wyjazdu_id, czy_to_wyjazd, czy_jednodniowe
    - output_removed: id, nazwa, opis, data_rozpoczecia, link
    """
    with (
        open(input_file, "r", encoding="utf-8") as infile,
        open(output_main, "w", encoding="utf-8") as mainfile,
        open(output_removed, "w", encoding="utf-8") as removedfile,
    ):

        for line in infile:
            line = line.strip()
            if not line or line.startswith("\\."):  # preserve COPY terminator
                mainfile.write(line + "\n")
                removedfile.write(line + "\n")
                continue

            parts = line.split("\t")

            try:
                id_col = parts[0]

                # Removed columns
                nazwa = parts[1] if len(parts) > 1 else ""
                opis = parts[2] if len(parts) > 2 else ""
                data_rozpoczecia = parts[3] if len(parts) > 3 else ""
                link = parts[5] if len(parts) > 5 else ""

                # Kept columns
                data_zakonczenia = parts[4] if len(parts) > 4 else ""
                typ_wydarzenia_id = parts[6] if len(parts) > 6 else ""
                typ_wyjazdu_id = parts[7] if len(parts) > 7 else ""
                czy_to_wyjazd = parts[8] if len(parts) > 8 else ""
                czy_jednodniowe = parts[9] if len(parts) > 9 else ""
            except IndexError:
                print(f"⚠️ Skipping malformed line: {line}", file=sys.stderr)
                continue

            # Write kept columns
            main_row = "\t".join(
                [
                    id_col,
                    data_zakonczenia,
                    typ_wydarzenia_id,
                    typ_wyjazdu_id,
                    czy_to_wyjazd,
                    czy_jednodniowe,
                ]
            )
            mainfile.write(main_row + "\n")

            # Write removed columns
            removed_row = "\t".join(
                [id_col, nazwa, opis, data_rozpoczecia, link]
            )
            removedfile.write(removed_row + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python split_cols.py input.txt output_main.txt output_removed.txt"
        )
        sys.exit(1)

    split_columns(sys.argv[1], sys.argv[2], sys.argv[3])
