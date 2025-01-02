from pypdf import PdfReader, PdfWriter
import sys
from typing import List, Tuple

output_path = "output.pdf"


def parse_recipe_file(recipe_path: str) -> List[Tuple[int, str, int]]:
    """
    Parse the recipe file and return a list of (page_number, title, level) tuples.
    Level indicates the indentation level (0 for root level).
    """
    outlines = []
    with open(recipe_path, "r") as f:
        for line in f:
            # Count leading spaces to determine level
            leading_spaces = len(line) - len(line.lstrip())
            level = leading_spaces // 2  # Assuming 2 spaces per indent level

            # Remove leading spaces
            line = line.strip()

            # Split into page number and title
            try:
                page_str, title = line.split(": ", 1)
                page = int(page_str)
                outlines.append(
                    (page - 1, title, level)
                )  # Convert to 0-based page numbering
            except ValueError:
                print(f"Warning: Skipping invalid line: {line}")
                continue

    return outlines


def add_outlines_to_pdf(pdf_path: str, recipe_path: str):
    """
    Add outlines to the PDF file based on the recipe file.
    """
    # Read the PDF
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Copy all pages from reader to writer
    for page in reader.pages:
        writer.add_page(page)

    # Parse the recipe file
    outlines = parse_recipe_file(recipe_path)

    # Create the outline structure
    parent_bookmarks = [None] * 10  # Support up to 10 levels of nesting

    for page_num, title, level in outlines:
        if page_num >= len(writer.pages):
            print(
                f"Warning: Page {page_num + 1} doesn't exist in PDF. Skipping outline: {title}"
            )
            continue

        # Create bookmark
        if level == 0:
            # Root level bookmark
            parent_bookmarks[0] = writer.add_outline_item(title, page_number=page_num)
        else:
            # Add as child of parent bookmark
            parent_bookmarks[level] = writer.add_outline_item(
                title, page_number=page_num, parent=parent_bookmarks[level - 1]
            )

    # Write the output file
    with open(output_path, "wb") as output_file:
        writer.write(output_file)


def main():
    if len(sys.argv) != 3:
        print("Usage: uv run main.py input.pdf recipe.txt")
        sys.exit(1)

    input_pdf = sys.argv[1]
    recipe_file = sys.argv[2]

    try:
        add_outlines_to_pdf(
            input_pdf,
            recipe_file,
        )
        print(f"Successfully created PDF with outlines to {output_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
