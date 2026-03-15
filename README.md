# Simple Semantic WER Benchmark

A simple tool for benchmarking speech-to-text systems with semantic Word Error Rate (WER) evaluation. This repository helps you accurately evaluate transcription quality by applying normalization and semantic equivalence rules before calculating WER metrics.

## Why This Tool?

Modern speech-to-text models like AssemblyAI's Universal-3 Pro are incredibly accurate—sometimes **more accurate than human transcription**. This creates challenges when evaluating with traditional WER metrics:

1. **Insertions**: The AI correctly transcribes words that human transcribers missed
2. **Substitutions**: The AI uses different but semantically equivalent formatting (e.g., "all right" vs "alright", "off site" vs "offsite")

This tool addresses both issues by:
- Applying **Whisper normalization** to standardize formatting
- Supporting **semantic word equivalence** to treat variants as identical
- Calculating accurate WER metrics with **jiwer**

Read more about this challenge in our [blog post](#) (coming soon).

## Features

- ✅ Transcribe audio files via AssemblyAI
- ✅ Whisper normalization for both truth and predictions
- ✅ Semantic word replacement (treat "all right" and "alright" as equivalent)
- ✅ Comprehensive WER metrics (WER, MER, WIL, WIP)
- ✅ Detailed error breakdown (insertions, deletions, substitutions)
- ✅ CSV export for analysis
- ✅ Simple directory-based workflow

**Note**: This tool does NOT support speaker diarization. Truth files and predictions are plain text only.

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/AssemblyAI-Solutions/simple-semantic-wer-benchmark.git
cd simple-semantic-wer-benchmark

# Install dependencies
pip install -r requirements.txt

# Set up your API key
cp .env.example .env
# Edit .env and add your AssemblyAI API key
```

Get your API key from https://www.assemblyai.com/app/api-keys

### 2. Add Your Files

```bash
# Add audio files
cp /path/to/your/audio/* audio/

# Add ground truth transcriptions (plain text, one per audio file)
# File names should match: audio/meeting.mp3 → truth/meeting.txt
cp /path/to/your/truth/* truth/
```

### 3. Run the Benchmark

```bash
# Option 1: Run everything at once
python run_all.py

# Option 2: Run steps separately
python transcribe.py  # Transcribe audio files
python benchmark.py   # Evaluate WER metrics
```

### 4. View Results

Results are saved to `results/benchmark_results.csv` with the following columns:

- `file_name` - Audio file name (without extension)
- `wer` - Word Error Rate (0.0 to 1.0)
- `mer` - Match Error Rate
- `wil` - Word Information Lost
- `wip` - Word Information Preserved
- `insertions` - Count of inserted words
- `deletions` - Count of deleted words
- `substitutions` - Count of substituted words
- `hits` - Count of correct words
- `truth_original` - Original ground truth text
- `prediction_original` - Original prediction from AssemblyAI
- `truth_normalized` - Normalized ground truth
- `prediction_normalized` - Normalized prediction

## Directory Structure

```
simple-semantic-wer-benchmark/
├── audio/                     # Input audio files (add your files here)
├── truth/                     # Ground truth transcriptions (add your files here)
├── predictions/
│   ├── raw/                   # Raw predictions from AssemblyAI
│   └── normalized/            # Normalized predictions
├── results/                   # Benchmark CSV output
├── config.json                # AssemblyAI configuration
├── semantic_wer_list.json     # Semantic word equivalence rules
├── .env                       # Your API key (create from .env.example)
├── transcribe.py              # Transcription script
├── benchmark.py               # Benchmark evaluation script
└── run_all.py                 # Run both scripts in sequence
```

## Configuration

### AssemblyAI Configuration (`config.json`)

The `config.json` file exposes all AssemblyAI transcription parameters. By default, it uses:

```json
{
  "assemblyai": {
    "speech_models": ["universal-3-pro"],
    "language_detection": true
  }
}
```

**Recommended for benchmarking**: Use the `[masked]` prompt to reduce hallucinations:

```json
{
  "assemblyai": {
    "speech_models": ["universal-3-pro"],
    "language_detection": true,
    "prompt": "Always: Transcribe speech exactly as heard. If uncertain or audio is unclear, mark as [masked]. After the first output, review the transcript again. Pay close attention to hallucinations, misspellings, or errors, and revise them like a computer performing spell and grammar checks. Ensure words and phrases make grammatical sense in sentences."
  }
}
```

For more prompting guidance, see:
- [Full Prompting Guide](https://www.assemblyai.com/docs/pre-recorded-audio/prompting)
- [Handling Unclear Audio with [masked]](https://www.assemblyai.com/docs/pre-recorded-audio/prompting#handling-unclear-audio-with-masked)

Other available parameters (see `config.json` for full list):
- `keyterms_prompt` - Boost specific words/phrases
- `temperature` - Control randomness (0.0 = deterministic)
- `remove_audio_tags` - Remove audio event tags like [music], [laughter]
- `language_code` - Force specific language
- `punctuate`, `format_text` - Control text formatting
- `filter_profanity` - Filter profanity
- And many more...

### Semantic WER List (`semantic_wer_list.json`)

Define word groups that should be treated as equivalent. The **first word** in each array is the canonical form that all variants will be replaced with.

```json
[
  [
    "all right",    // Canonical form (everything becomes this)
    "alright"       // Variant (will be replaced)
  ],
  [
    "off site",     // Canonical form
    "offsite",      // Variant 1
    "off-site"      // Variant 2
  ]
]
```

**How it works**: Before calculating WER, both truth and prediction are normalized:
1. Apply Whisper normalization (lowercase, remove punctuation, etc.)
2. Replace all variants with the canonical form
3. Calculate WER metrics on the normalized text

This ensures "all right" in truth and "alright" in prediction are treated as identical.

## File Naming Convention

Audio files and truth files must have matching names (excluding extension):

```
audio/meeting.mp3     → truth/meeting.txt
audio/interview.wav   → truth/interview.txt
audio/podcast.m4a     → truth/podcast.txt
```

## Example Workflow

1. **Add files**:
   ```bash
   # audio/call_recording.mp3
   # truth/call_recording.txt (contains: "That's all right, we can meet off site")
   ```

2. **Configure** semantic WER list:
   ```json
   [
     ["all right", "alright"],
     ["off site", "offsite"]
   ]
   ```

3. **Run benchmark**:
   ```bash
   python run_all.py
   ```

4. **Results**:
   - Raw prediction: "That's alright, we can meet offsite"
   - After normalization: Both become "that's all right we can meet off site"
   - WER: 0.0 (perfect match after semantic normalization)

## Understanding the Metrics

- **WER (Word Error Rate)**: `(I + D + S) / N` where I=insertions, D=deletions, S=substitutions, N=total words. Lower is better (0.0 = perfect).
- **MER (Match Error Rate)**: `(I + D + S) / (I + D + S + H)` where H=hits. Alternative to WER.
- **WIL (Word Information Lost)**: Weighted error rate giving more weight to content words.
- **WIP (Word Information Preserved)**: `1 - WIL`. Higher is better.

Good WER scores:
- < 5% - Excellent
- 5-10% - Good
- 10-20% - Acceptable
- \> 20% - Needs improvement

## Limitations

- **No diarization support**: This tool uses plain text transcriptions only. Speaker labels are not preserved in the benchmark.
- **Text-only**: Does not evaluate timing, confidence scores, or other metadata.

**Note**: The default normalizer is configured for English (`EnglishTextNormalizer`). For other languages, use `BasicTextNormalizer` instead. See [Custom Normalization](#custom-normalization) for details.

## Advanced Usage

### Running Individual Steps

```bash
# Step 1: Transcribe only
python transcribe.py

# Step 2: Benchmark only (requires existing predictions)
python benchmark.py
```

### Custom Normalization

The tool uses **Whisper normalization** by default to standardize text before calculating WER. You can customize which normalizer to use by editing `benchmark.py`.

#### Available Normalizers

1. **EnglishTextNormalizer** (Default)
   - Best for: English audio
   - Features: Language-specific rules, handles contractions, standardizes formatting
   - Example: "don't" → "do not", removes punctuation, lowercases

2. **BasicTextNormalizer**
   - Best for: Non-English languages, minimal processing
   - Features: Basic lowercasing and punctuation removal
   - More permissive than EnglishTextNormalizer

#### How to Change the Normalizer

Open `benchmark.py` and modify lines 16-25:

**Option 1: Use BasicTextNormalizer (for non-English)**

```python
# Comment out the English normalizer import
# from whisper_normalizer.english import EnglishTextNormalizer
from whisper_normalizer.basic import BasicTextNormalizer

# Change the normalizer initialization
normalizer = BasicTextNormalizer()
```

**Option 2: Use EnglishTextNormalizer (default)**

```python
from whisper_normalizer.english import EnglishTextNormalizer

normalizer = EnglishTextNormalizer()
```

**Option 3: Disable normalization (not recommended)**

If you want to skip Whisper normalization entirely:

```python
# Define a no-op normalizer
def normalizer(text):
    return text.lower()  # Only lowercase
```

#### When to Change the Normalizer

- **Use BasicTextNormalizer** if:
  - Your audio is in a non-English language
  - You're getting unexpected normalization results
  - You want minimal text processing

- **Use EnglishTextNormalizer** if:
  - Your audio is in English (default)
  - You want standard WER evaluation
  - You need contraction handling ("don't" → "do not")

- **Disable normalization** if:
  - You've already normalized your truth files
  - You want to control normalization yourself
  - You're testing raw transcription quality

#### Example: Spanish Audio

For Spanish audio, use BasicTextNormalizer:

```python
from whisper_normalizer.basic import BasicTextNormalizer

normalizer = BasicTextNormalizer()
```

Then run your benchmark as usual:

```bash
python benchmark.py
```

### Analyzing Results

The CSV output can be analyzed with pandas:

```python
import pandas as pd

df = pd.read_csv("results/benchmark_results.csv")

# Average WER
print(f"Average WER: {df['wer'].mean():.4f}")

# Files with highest error rates
print(df.nlargest(5, 'wer')[['file_name', 'wer']])

# Error distribution
print(f"Total insertions: {df['insertions'].sum()}")
print(f"Total deletions: {df['deletions'].sum()}")
print(f"Total substitutions: {df['substitutions'].sum()}")
```

## Troubleshooting

### "No audio files found"
- Make sure audio files are in the `audio/` directory
- Check that files are not hidden (don't start with `.`)

### "No truth files found"
- Add `.txt` files to the `truth/` directory
- Ensure file names match audio files (e.g., `audio/test.mp3` → `truth/test.txt`)

### "ASSEMBLYAI_API_KEY not found"
- Copy `.env.example` to `.env`
- Add your API key from https://www.assemblyai.com/app/api-keys

### Transcription fails
- Check your API key is valid
- Ensure audio files are in a supported format (mp3, wav, m4a, etc.)
- Check the error message in the console output

### High WER despite good transcription
- Review the `truth_normalized` and `prediction_normalized` columns in the CSV
- Add more semantic equivalences to `semantic_wer_list.json`
- Check if Whisper normalization is working as expected

## Related Resources

- [AssemblyAI Universal-3 Pro](https://www.assemblyai.com/docs/pre-recorded-audio/universal-3-pro)
- [Prompting Guide](https://www.assemblyai.com/docs/pre-recorded-audio/prompting)
- [Whisper Normalizer](https://github.com/kurianbenoy/whisper_normalizer)
- [jiwer Documentation](https://jitsi.github.io/jiwer/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Support

For issues or questions:
- Open an issue on GitHub
- Contact AssemblyAI support: support@assemblyai.com
- Read the docs: https://www.assemblyai.com/docs
