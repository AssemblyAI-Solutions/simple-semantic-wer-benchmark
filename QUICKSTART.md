# Quick Start Guide

Get up and running in 5 minutes!

## 1. Install

```bash
# Clone the repository
git clone https://github.com/AssemblyAI-Solutions/simple-semantic-wer-benchmark.git
cd simple-semantic-wer-benchmark

# Install dependencies
pip install -r requirements.txt
```

## 2. Configure

```bash
# Set up your API key
cp .env.example .env
nano .env  # Add your AssemblyAI API key
```

Get your API key: https://www.assemblyai.com/app/api-keys

## 3. Add Your Files

```bash
# Add audio files to audio/
cp /path/to/your/*.mp3 audio/

# Add truth files to truth/
# Each truth file should match an audio file name
# Example: audio/meeting.mp3 → truth/meeting.txt
echo "Your ground truth transcription here" > truth/meeting.txt
```

## 4. Run

```bash
# Run everything
python run_all.py
```

## 5. View Results

Results are saved to `results/benchmark_results.csv`

```bash
# Quick look at results
head results/benchmark_results.csv
```

## Next Steps

- Read [EXAMPLE.md](EXAMPLE.md) for a detailed walkthrough
- Check [README.md](README.md) for full documentation
- Customize `semantic_wer_list.json` for your use case
- Explore `config.json` for advanced options

## Troubleshooting

### No audio files found
Add audio files to the `audio/` directory

### No truth files found
Add `.txt` files to the `truth/` directory with matching names

### API key error
Make sure you've created `.env` from `.env.example` and added your API key

### Need help?
See [README.md](README.md#troubleshooting) for common issues
