import os


def replace_spaces_in_filenames(directory):
    # Go through all files in the given directory
    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)

        # Skip directories
        if os.path.isdir(old_path):
            continue

        # Create new filename with spaces replaced by underscores
        new_filename = (
            filename.replace(" ", "_")
            .replace("–", "")
            .replace(",", "")
        )
        new_path = os.path.join(directory, new_filename)

        # Rename the file if needed
        if old_path != new_path:
            os.rename(src=old_path, dst=new_path)
            print(f'Renamed: "{filename}" -> "{new_filename}"')


# Example usage:
directory_path = "/home/szymon/Desktop/bcs/bcs/media/pdfs"
replace_spaces_in_filenames(directory_path)
