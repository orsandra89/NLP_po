import pandas as pd
import re
from pathlib import Path


df = pd.read_csv("poetry_analysis_results.csv")


author_map = {}

books_path = Path("poetry_books")
for file_path in books_path.glob("*.txt"):
    with open(file_path, encoding="utf-8") as f:
        text = f.read()

    match = re.search(r'\bby ([A-Z][a-z]+(?: [A-Z][a-z]+)+)', text, re.IGNORECASE)

    if match:
        author = match.group(1).strip()
        author_map[file_path.name] = author
    else:
        author_map[file_path.name] = "Unknown"


df["author"] = df["filename"].map(author_map)


df.to_csv("poetry_analysis_with_authors.csv", index=False)

