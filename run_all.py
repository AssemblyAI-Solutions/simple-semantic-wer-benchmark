#!/usr/bin/env python3
"""
Run complete benchmarking workflow.

This script runs both transcription and benchmarking in sequence:
1. Transcribe audio files using AssemblyAI (transcribe.py)
2. Evaluate WER metrics with normalization (benchmark.py)
"""

import sys
from pathlib import Path

# Import the main functions from each script
import transcribe
import benchmark


def main():
    """Run the complete workflow."""
    print("=" * 60)
    print("Complete Semantic WER Benchmark Workflow")
    print("=" * 60)

    # Check if audio files exist
    audio_dir = Path("audio")
    audio_files = list(audio_dir.glob("*"))
    audio_files = [f for f in audio_files if f.is_file() and not f.name.startswith('.')]

    if not audio_files:
        print(f"\n✗ No audio files found in {audio_dir}/")
        print("Please add audio files to the audio/ directory and try again.")
        return 1

    # Check if truth files exist
    truth_dir = Path("truth")
    truth_files = list(truth_dir.glob("*.txt"))

    if not truth_files:
        print(f"\n✗ No truth files found in {truth_dir}/")
        print("Please add ground truth transcriptions to the truth/ directory.")
        return 1

    print("\n" + "=" * 60)
    print("STEP 1: Transcription")
    print("=" * 60)

    # Run transcription
    try:
        transcribe.main()
    except Exception as e:
        print(f"\n✗ Transcription failed: {e}")
        return 1

    print("\n" + "=" * 60)
    print("STEP 2: Benchmark Evaluation")
    print("=" * 60)

    # Run benchmark
    try:
        benchmark.main()
    except Exception as e:
        print(f"\n✗ Benchmark evaluation failed: {e}")
        return 1

    print("\n" + "=" * 60)
    print("Complete Workflow Finished!")
    print("=" * 60)
    print("\nResults saved to:")
    print("  - predictions/raw/         (raw transcriptions)")
    print("  - predictions/normalized/  (normalized transcriptions)")
    print("  - results/                 (benchmark CSV)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
