# Example Walkthrough

This guide walks through a complete example of using the Simple Semantic WER Benchmark tool.

## Scenario

You have a recording of a conversation where:
- The human transcriber wrote: "That's all right, we can meet off site tomorrow"
- AssemblyAI transcribes: "That's alright, we can meet offsite tomorrow"

Traditional WER would show 2 substitutions (all right → alright, off site → offsite), giving a WER of 2/8 = 25%.

With semantic normalization, WER is 0% because the words are equivalent.

## Step-by-Step Example

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
nano .env  # Add your API key
```

### 2. Prepare Files

Create a truth file at `truth/example_conversation.txt`:

```
That's all right, we can meet off site tomorrow
```

Add your audio file at `audio/example_conversation.mp3`

### 3. Configure Semantic WER List

Edit `semantic_wer_list.json`:

```json
[
  [
    "all right",
    "alright"
  ],
  [
    "off site",
    "offsite",
    "off-site"
  ]
]
```

### 4. Run Transcription

```bash
python transcribe.py
```

Output:
```
=============================================================
AssemblyAI Transcription Script
=============================================================

Loading configuration from config.json...
Config loaded: speech_models=['universal-3-pro']

Found 1 audio file(s) to transcribe:
  - example_conversation.mp3

=============================================================
Starting Transcription
=============================================================

Processing: example_conversation.mp3
  Uploading example_conversation.mp3...
  Upload complete: https://cdn.assemblyai.com/upload/...
  Submitting transcription request...
  Transcript ID: abc123...
  Waiting for transcription to complete...
  Status: processing...
  ✓ Transcription completed!
  Saved to: predictions/raw/example_conversation.txt

=============================================================
Transcription Complete!
=============================================================

Raw predictions saved to: predictions/raw/
Next step: Run benchmark.py to evaluate WER metrics
```

### 5. Run Benchmark

```bash
python benchmark.py
```

Output:
```
=============================================================
WER Benchmark Evaluation
=============================================================

Loading semantic WER list...
Loaded 2 semantic word groups

Found 1 truth file(s)

=============================================================
Processing Files
=============================================================

Processing: example_conversation
  WER: 0.0000 (0.00%)
  Insertions: 0, Deletions: 0, Substitutions: 0

✓ Results exported to: results/benchmark_results.csv

=============================================================
Summary Statistics
=============================================================
Files processed: 1

Average Metrics:
  WER: 0.0000 (0.00%)
  MER: 0.0000 (0.00%)
  WIL: 0.0000 (0.00%)
  WIP: 1.0000 (100.00%)

Total Counts:
  Insertions: 0
  Deletions: 0
  Substitutions: 0
  Hits: 8

=============================================================
Benchmark Complete!
=============================================================
```

### 6. Examine Results

Open `results/benchmark_results.csv`:

| file_name | wer | insertions | deletions | substitutions | truth_original | prediction_original | truth_normalized | prediction_normalized |
|-----------|-----|------------|-----------|---------------|----------------|---------------------|------------------|----------------------|
| example_conversation | 0.0 | 0 | 0 | 0 | That's all right, we can meet off site tomorrow | That's alright, we can meet offsite tomorrow | that s all right we can meet off site tomorrow | that s all right we can meet off site tomorrow |

## Understanding the Results

### Without Semantic Normalization

If we hadn't used semantic_wer_list.json:
- Truth (normalized): "that s all right we can meet off site tomorrow"
- Prediction (normalized): "that s alright we can meet offsite tomorrow"
- WER: 2/8 = 0.25 (25%)
- Substitutions: 2 (alright, offsite)

### With Semantic Normalization

With semantic_wer_list.json:
- Truth (normalized): "that s all right we can meet off site tomorrow"
- Prediction (normalized): "that s all right we can meet off site tomorrow"
- WER: 0/8 = 0.0 (0%)
- Substitutions: 0

The semantic replacements converted:
- "alright" → "all right"
- "offsite" → "off site"

Both truth and prediction now match perfectly!

## Advanced Example: Handling Insertions

### Scenario

Your audio has a faint word that the human transcriber missed but AssemblyAI caught.

Truth: `The patient is experiencing headaches`
Prediction: `The patient is experiencing severe headaches`

Without review, this shows as 1 insertion (severe), giving WER = 1/5 = 20%.

### Solution

1. Listen to the audio at the timestamps where "severe" appears
2. If AssemblyAI is correct, update your truth file:
   ```
   The patient is experiencing severe headaches
   ```
3. Re-run the benchmark to get accurate WER

This is where the tool shines - it helps you identify where your truth files need correction!

## Tips for Best Results

1. **Use the [masked] prompt** for difficult audio to reduce hallucinations:
   ```json
   {
     "prompt": "Always: Transcribe speech exactly as heard. If uncertain or audio is unclear, mark as [masked]..."
   }
   ```

2. **Build your semantic list iteratively**:
   - Run benchmark once
   - Review substitutions in CSV
   - Add semantic equivalences
   - Re-run benchmark

3. **Listen to insertions**:
   - Sort CSV by `insertions` column
   - Review high-insertion files
   - Check if insertions are correct
   - Update truth files if needed

4. **Track your progress**:
   ```bash
   # Keep old results for comparison
   cp results/benchmark_results.csv results/benchmark_results_2024_03_15.csv
   ```

## Next Steps

- Try with your own audio files
- Experiment with different prompts
- Build a comprehensive semantic word list for your domain
- Share your results and insights!
