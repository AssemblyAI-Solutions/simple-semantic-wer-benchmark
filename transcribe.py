#!/usr/bin/env python3
"""
Transcribe audio files using AssemblyAI.

This script:
1. Reads audio files from the audio/ directory
2. Uploads them to AssemblyAI
3. Transcribes them using configuration from config.json
4. Saves raw transcriptions to predictions/raw/
"""

import os
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not API_KEY:
    raise ValueError("ASSEMBLYAI_API_KEY not found in .env file")

BASE_URL = "https://api.assemblyai.com"
AUDIO_DIR = Path("audio")
PREDICTIONS_RAW_DIR = Path("predictions/raw")

# Ensure directories exist
PREDICTIONS_RAW_DIR.mkdir(parents=True, exist_ok=True)


def load_config():
    """Load AssemblyAI configuration from config.json."""
    with open("config.json", "r") as f:
        # Remove comments from JSON (simple implementation)
        content = f.read()
        lines = []
        for line in content.split('\n'):
            # Remove lines that start with //
            stripped = line.strip()
            if not stripped.startswith('//'):
                lines.append(line)
        clean_content = '\n'.join(lines)
        config = json.loads(clean_content)
    return config["assemblyai"]


def upload_file(file_path):
    """Upload an audio file to AssemblyAI."""
    print(f"  Uploading {file_path.name}...")

    headers = {"authorization": API_KEY}

    with open(file_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/v2/upload",
            headers=headers,
            data=f
        )

    response.raise_for_status()
    upload_url = response.json()["upload_url"]
    print(f"  Upload complete: {upload_url}")
    return upload_url


def submit_transcription(audio_url, config):
    """Submit a transcription request to AssemblyAI."""
    print("  Submitting transcription request...")

    headers = {
        "authorization": API_KEY,
        "content-type": "application/json"
    }

    data = {
        "audio_url": audio_url,
        **config  # Merge in all config options
    }

    response = requests.post(
        f"{BASE_URL}/v2/transcript",
        headers=headers,
        json=data
    )

    response.raise_for_status()
    transcript_id = response.json()["id"]
    print(f"  Transcript ID: {transcript_id}")
    return transcript_id


def poll_transcription(transcript_id):
    """Poll for transcription completion."""
    print("  Waiting for transcription to complete...")

    headers = {"authorization": API_KEY}
    polling_url = f"{BASE_URL}/v2/transcript/{transcript_id}"

    while True:
        response = requests.get(polling_url, headers=headers)
        response.raise_for_status()
        result = response.json()

        status = result["status"]

        if status == "completed":
            print("  ✓ Transcription completed!")
            return result
        elif status == "error":
            error_msg = result.get("error", "Unknown error")
            raise RuntimeError(f"Transcription failed: {error_msg}")
        else:
            print(f"  Status: {status}...")
            time.sleep(3)


def transcribe_file(file_path, config):
    """Transcribe a single audio file."""
    print(f"\nProcessing: {file_path.name}")

    # Upload file
    audio_url = upload_file(file_path)

    # Submit transcription
    transcript_id = submit_transcription(audio_url, config)

    # Poll for completion
    result = poll_transcription(transcript_id)

    # Extract text
    transcript_text = result.get("text", "")

    if not transcript_text:
        print(f"  ⚠ Warning: No transcript text returned for {file_path.name}")

    return transcript_text


def save_prediction(file_name, text):
    """Save prediction to predictions/raw/ directory."""
    # Get base name without extension
    base_name = Path(file_name).stem
    output_path = PREDICTIONS_RAW_DIR / f"{base_name}.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"  Saved to: {output_path}")


def main():
    """Main transcription workflow."""
    print("=" * 60)
    print("AssemblyAI Transcription Script")
    print("=" * 60)

    # Load configuration
    print("\nLoading configuration from config.json...")
    config = load_config()
    print(f"Config loaded: speech_models={config.get('speech_models')}")

    # Get all audio files
    audio_files = list(AUDIO_DIR.glob("*"))
    # Filter out hidden files and directories
    audio_files = [f for f in audio_files if f.is_file() and not f.name.startswith('.')]

    if not audio_files:
        print(f"\n⚠ No audio files found in {AUDIO_DIR}/")
        print("Please add audio files to the audio/ directory and try again.")
        return

    print(f"\nFound {len(audio_files)} audio file(s) to transcribe:")
    for f in audio_files:
        print(f"  - {f.name}")

    # Process each file
    print("\n" + "=" * 60)
    print("Starting Transcription")
    print("=" * 60)

    for audio_file in audio_files:
        try:
            transcript_text = transcribe_file(audio_file, config)
            save_prediction(audio_file.name, transcript_text)
        except Exception as e:
            print(f"\n✗ Error processing {audio_file.name}: {e}")
            continue

    print("\n" + "=" * 60)
    print("Transcription Complete!")
    print("=" * 60)
    print(f"\nRaw predictions saved to: {PREDICTIONS_RAW_DIR}/")
    print("Next step: Run benchmark.py to evaluate WER metrics")


if __name__ == "__main__":
    main()
