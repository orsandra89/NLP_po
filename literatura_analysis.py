
import os
import pandas as pd
import re
from pathlib import Path
from collections import Counter
import nltk

# Ensure required nltk data is downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# === Function: count syllables in a word (approximation) ===
def count_syllables(word):
    word = word.lower()
    return len(re.findall(r'[aeiouy]+', word))

# === Function: analyze poetic structure ===
def analyze_poem(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    num_lines = len(lines)
    line_lengths = [len(line.split()) for line in lines]
    syllables_per_line = [sum(count_syllables(w) for w in line.split()) for line in lines]

    # Detect anaphora: repeated first word in consecutive lines
    starters = [line.split()[0] for line in lines if len(line.split()) > 0]
    anaphora_count = sum(1 for i in range(1, len(starters)) if starters[i] == starters[i-1])

    # POS tagging for entire text
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    pos_counts = dict(Counter(tag for word, tag in pos_tags))

    return {
        "num_lines": num_lines,
        "avg_line_length": sum(line_lengths) / num_lines if num_lines else 0,
        "avg_syllables_per_line": sum(syllables_per_line) / num_lines if num_lines else 0,
        "anaphora_count": anaphora_count,
        "pos_counts": pos_counts
    }

# === Analyze all poems in directory ===
books_path = Path("poetry_books")
results = []

for file_path in books_path.glob("*.txt"):
    with open(file_path, encoding="utf-8") as f:
        text = f.read()
    analysis = analyze_poem(text)
    flat_result = {
        "filename": file_path.name,
        "num_lines": analysis["num_lines"],
        "avg_line_length": analysis["avg_line_length"],
        "avg_syllables_per_line": analysis["avg_syllables_per_line"],
        "anaphora_count": analysis["anaphora_count"],
    }
    # Flatten POS counts
    for tag, count in analysis["pos_counts"].items():
        flat_result[f"pos_{tag}"] = count
    results.append(flat_result)

# === Save results to CSV ===
df = pd.DataFrame(results)
df.to_csv("poetry_analysis_results.csv", index=False)
print("✅ Analysis complete. Results saved to poetry_analysis_results.csv")
