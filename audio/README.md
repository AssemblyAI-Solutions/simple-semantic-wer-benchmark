# Audio Files

Place your audio files in this directory.

## Supported Formats

AssemblyAI supports many audio formats including:
- MP3
- WAV
- M4A
- FLAC
- MP4 (audio track)
- And more...

## File Naming

Your audio file names should match your truth file names (excluding extension):

```
audio/meeting.mp3     → truth/meeting.txt
audio/interview.wav   → truth/interview.txt
audio/podcast.m4a     → truth/podcast.txt
```

## Example

```bash
# Add your audio files
cp /path/to/your/audio/*.mp3 .

# Make sure you have corresponding truth files
ls ../truth/
```
