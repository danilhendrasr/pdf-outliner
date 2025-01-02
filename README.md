# PDF Outliner

A Python program to add outlines to a PDF file based on a recipe file.

## Usage

1. Create a recipe file with the desired outline structure.
2. Run the program with the recipe file and the PDF file as arguments.
3. The program will add outlines to the PDF file and save it as `output.pdf`.

## Getting Started

1. Install Python 3.12
2. Install UV
3. Clone the repo and `cd` into the directory
4. Create a recipe file
5. Run `uv run main.py <path/to/input/file>.pdf <path/to/recipe/file>.txt`
6. The output PDF will be saved as `output.pdf` in the directory of the program

## Recipe File Format

The recipe file should be a text file with the following format:

```
1: Introduction
  2: What is Machine Learning
  4: Types of Machine Learning
    5: Supervised Learning
    7: Unsupervised Learning
    9: Reinforcement Learning
10: Data Preprocessing
```

Each line starts with the target page number, followed by a colon, and then the title of the section
you want to associate with that page. To create a sub-section, just indent the line with two spaces.
