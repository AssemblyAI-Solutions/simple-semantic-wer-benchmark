# Contributing to Simple Semantic WER Benchmark

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the [Issues](https://github.com/AssemblyAI-Solutions/simple-semantic-wer-benchmark/issues) tab
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Python version and OS
   - Relevant error messages or logs

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/simple-semantic-wer-benchmark.git
   cd simple-semantic-wer-benchmark
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Test transcription
   python transcribe.py

   # Test benchmark
   python benchmark.py

   # Test full workflow
   python run_all.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Describe your changes

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and concise

### Adding New Features

When adding features, consider:
- **Simplicity**: This tool is designed to be simple and accessible
- **Documentation**: Update README.md with new features
- **Backwards compatibility**: Don't break existing workflows
- **Dependencies**: Minimize new dependencies

### Testing

Before submitting:
- Test with different audio files
- Test with different config options
- Verify CSV output is correct
- Check for edge cases (empty files, missing files, etc.)

## Feature Ideas

Some areas where contributions would be valuable:

### Normalization
- Support for additional languages beyond English
- Custom normalization rules
- Better handling of numbers, dates, times

### Metrics
- Additional evaluation metrics
- Per-word confidence tracking
- Audio duration-based metrics

### Output
- HTML report generation
- Visualization of errors
- Comparison across multiple models

### Workflow
- Batch processing improvements
- Resume interrupted transcriptions
- Parallel processing

### Integration
- Support for other STT providers
- Integration with other benchmarking tools
- Export to other formats (JSON, Excel, etc.)

## Questions?

If you have questions about contributing:
- Open a discussion in GitHub Discussions
- Email support@assemblyai.com
- Check the [README.md](README.md) for documentation

## Code of Conduct

This project follows a simple code of conduct:
- Be respectful and constructive
- Focus on what is best for the community
- Show empathy towards others

Thank you for contributing! 🎉
