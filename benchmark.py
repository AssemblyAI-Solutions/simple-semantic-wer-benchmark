#!/usr/bin/env python3
"""
Benchmark WER evaluation with semantic normalization.

This script:
1. Loads truth files and raw predictions
2. Applies Whisper normalization to both
3. Applies semantic WER replacements
4. Calculates WER metrics using jiwer
5. Saves normalized texts and exports results to CSV
"""

import json
import csv
from pathlib import Path
from jiwer import wer, mer, wil, wip, compute_measures

# Import available normalizers
# You can change which normalizer to use by uncommenting one of these:
from whisper_normalizer.english import EnglishTextNormalizer  # Default: English-specific normalization
# from whisper_normalizer.basic import BasicTextNormalizer    # Alternative: Basic normalization (good for non-English)

# Configuration
TRUTH_DIR = Path("truth")
PREDICTIONS_RAW_DIR = Path("predictions/raw")
PREDICTIONS_NORMALIZED_DIR = Path("predictions/normalized")
RESULTS_DIR = Path("results")
SEMANTIC_WER_LIST_PATH = Path("semantic_wer_list.json")

# Ensure directories exist
PREDICTIONS_NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Initialize normalizer
# Change this line to use a different normalizer:
normalizer = EnglishTextNormalizer()  # Default: English normalization
# normalizer = BasicTextNormalizer()  # Alternative: Basic normalization


def load_semantic_wer_list():
    """Load semantic WER replacement list."""
    if not SEMANTIC_WER_LIST_PATH.exists():
        print(f"⚠ No semantic_wer_list.json found. Skipping semantic replacements.")
        return []

    with open(SEMANTIC_WER_LIST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def apply_semantic_replacements(text, semantic_list):
    """
    Apply semantic replacements to text.

    For each array in semantic_list, replace all variants (index 1+)
    with the canonical form (index 0).
    """
    for word_group in semantic_list:
        if len(word_group) < 2:
            continue

        canonical = word_group[0]
        variants = word_group[1:]

        for variant in variants:
            # Case-insensitive replacement
            text = text.replace(variant.lower(), canonical.lower())

    return text


def normalize_text(text, semantic_list):
    """
    Normalize text using Whisper normalizer and semantic replacements.

    Steps:
    1. Apply Whisper normalization (lowercasing, punctuation removal, etc.)
    2. Apply semantic replacements
    """
    # Step 1: Whisper normalization
    normalized = normalizer(text)

    # Step 2: Semantic replacements
    normalized = apply_semantic_replacements(normalized, semantic_list)

    return normalized


def calculate_wer_metrics(truth, prediction):
    """Calculate WER metrics using jiwer."""
    # Compute detailed measures
    measures = compute_measures(truth, prediction)

    return {
        "wer": measures["wer"],
        "mer": measures["mer"],
        "wil": measures["wil"],
        "wip": measures["wip"],
        "insertions": measures["insertions"],
        "deletions": measures["deletions"],
        "substitutions": measures["substitutions"],
        "hits": measures["hits"]
    }


def process_file_pair(truth_file, prediction_file, semantic_list):
    """Process a truth/prediction file pair."""
    file_name = truth_file.stem

    # Load files
    with open(truth_file, "r", encoding="utf-8") as f:
        truth_text = f.read().strip()

    with open(prediction_file, "r", encoding="utf-8") as f:
        prediction_text = f.read().strip()

    # Normalize both texts
    truth_normalized = normalize_text(truth_text, semantic_list)
    prediction_normalized = normalize_text(prediction_text, semantic_list)

    # Save normalized prediction
    normalized_output = PREDICTIONS_NORMALIZED_DIR / f"{file_name}.txt"
    with open(normalized_output, "w", encoding="utf-8") as f:
        f.write(prediction_normalized)

    # Calculate metrics
    if not truth_normalized or not prediction_normalized:
        print(f"  ⚠ Warning: Empty text for {file_name}")
        metrics = {
            "wer": 1.0,
            "mer": 1.0,
            "wil": 1.0,
            "wip": 0.0,
            "insertions": 0,
            "deletions": 0,
            "substitutions": 0,
            "hits": 0
        }
    else:
        metrics = calculate_wer_metrics(truth_normalized, prediction_normalized)

    return {
        "file_name": file_name,
        "truth_original": truth_text,
        "prediction_original": prediction_text,
        "truth_normalized": truth_normalized,
        "prediction_normalized": prediction_normalized,
        **metrics
    }


def export_to_csv(results):
    """Export results to CSV."""
    output_path = RESULTS_DIR / "benchmark_results.csv"

    fieldnames = [
        "file_name",
        "wer",
        "mer",
        "wil",
        "wip",
        "insertions",
        "deletions",
        "substitutions",
        "hits",
        "truth_original",
        "prediction_original",
        "truth_normalized",
        "prediction_normalized"
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✓ Results exported to: {output_path}")


def print_summary(results):
    """Print summary statistics."""
    if not results:
        return

    avg_wer = sum(r["wer"] for r in results) / len(results)
    avg_mer = sum(r["mer"] for r in results) / len(results)
    avg_wil = sum(r["wil"] for r in results) / len(results)
    avg_wip = sum(r["wip"] for r in results) / len(results)

    total_insertions = sum(r["insertions"] for r in results)
    total_deletions = sum(r["deletions"] for r in results)
    total_substitutions = sum(r["substitutions"] for r in results)
    total_hits = sum(r["hits"] for r in results)

    print("\n" + "=" * 60)
    print("Summary Statistics")
    print("=" * 60)
    print(f"Files processed: {len(results)}")
    print(f"\nAverage Metrics:")
    print(f"  WER: {avg_wer:.4f} ({avg_wer*100:.2f}%)")
    print(f"  MER: {avg_mer:.4f} ({avg_mer*100:.2f}%)")
    print(f"  WIL: {avg_wil:.4f} ({avg_wil*100:.2f}%)")
    print(f"  WIP: {avg_wip:.4f} ({avg_wip*100:.2f}%)")
    print(f"\nTotal Counts:")
    print(f"  Insertions: {total_insertions}")
    print(f"  Deletions: {total_deletions}")
    print(f"  Substitutions: {total_substitutions}")
    print(f"  Hits: {total_hits}")


def main():
    """Main benchmark workflow."""
    print("=" * 60)
    print("WER Benchmark Evaluation")
    print("=" * 60)

    # Load semantic WER list
    print("\nLoading semantic WER list...")
    semantic_list = load_semantic_wer_list()
    if semantic_list:
        print(f"Loaded {len(semantic_list)} semantic word groups")

    # Get truth files
    truth_files = list(TRUTH_DIR.glob("*.txt"))
    if not truth_files:
        print(f"\n✗ No truth files found in {TRUTH_DIR}/")
        print("Please add ground truth files to the truth/ directory.")
        return

    print(f"\nFound {len(truth_files)} truth file(s)")

    # Process each file pair
    results = []
    print("\n" + "=" * 60)
    print("Processing Files")
    print("=" * 60)

    for truth_file in truth_files:
        file_name = truth_file.stem
        prediction_file = PREDICTIONS_RAW_DIR / f"{file_name}.txt"

        if not prediction_file.exists():
            print(f"\n⚠ Skipping {file_name}: No prediction file found")
            continue

        print(f"\nProcessing: {file_name}")

        try:
            result = process_file_pair(truth_file, prediction_file, semantic_list)
            results.append(result)

            # Print individual file metrics
            print(f"  WER: {result['wer']:.4f} ({result['wer']*100:.2f}%)")
            print(f"  Insertions: {result['insertions']}, "
                  f"Deletions: {result['deletions']}, "
                  f"Substitutions: {result['substitutions']}")

        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue

    # Export results
    if results:
        export_to_csv(results)
        print_summary(results)
    else:
        print("\n✗ No results to export")

    print("\n" + "=" * 60)
    print("Benchmark Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
