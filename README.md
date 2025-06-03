# Aissistant# Audio Q&A Assistant

A sophisticated Python application that continuously listens to audio, detects questions, and provides intelligent answers using language models.

## Features

- **Continuous Audio Listening**: Real-time audio transcription with automatic question detection
- **Subject-Specific Responses**: Select from 10 school subjects for contextual answers
- **Smart Question Detection**: Advanced pattern matching to identify questions in speech
- **LLM Integration**: Uses OpenAI's GPT models for intelligent responses
- **Visualization Mode**: Special mode for requesting and displaying visualizations
- **Clean Modern UI**: Built with PyQt6 for a responsive, professional interface
- **Answer Queue System**: Review answers before displaying them
- **Multi-threaded Performance**: Smooth operation with background processing

## Project Structure

```
audio-qa-assistant/
├── main.py                 # Application entry point
├── ui/
│   ├── __init__.py
│   └── main_window.py      # Main GUI window
├── audio/
│   ├── __init__.py
│   └── audio_handler.py    # Audio recording and transcription
├── ai/
│   ├── __init__.py
│   ├── llm_handler.py      # Language model integration
│   └── question_detector.py # Question detection logic
├── requirements.txt        # Python dependencies
├── setup.py               # Setup script
├── .env.template          # Environment variables template
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Microphone access
- OpenAI API key (for GPT integration)

### Setup Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd audio-qa-assistant
```

2. Run the setup script:
```bash
python setup.py
```

3. Configure your OpenAI API key:
   - Copy `.env.template` to `.env`
   - Add your OpenAI API key to the `.env` file
   
   OR set it as an environment variable:
   ```bash
   export OPENAI_API_KEY='your-key-here'
   ```

4. Install audio dependencies:
   - **Windows**: PyAudio should install automatically
   - **macOS**: `brew install portaudio`
   - **Linux**: `sudo apt-get install portaudio19-dev`

## Usage

1. Start the application:
```bash
python main.py
```

2. Select a subject from the list when prompted

3. Click "Start Listening" to begin continuous audio monitoring

4. Speak naturally - the system will detect questions automatically

5. When a question is detected:
   - The "ANSWER" button will highlight
   - Click it to see the response
   - Or click "Ignore" to skip

6. For visualizations:
   - Click the "Visualize" button
   - Speak your visualization request
   - Release to process the request

## Configuration

### What You Need to Provide

1. **OpenAI API Key** (Required):
   - Sign up at https://platform.openai.com
   - Generate an API key
   - Add it to your `.env` file or `ai/llm_handler.py`

2. **Audio Device** (Required):
   - Ensure your microphone is connected and working
   - Grant microphone permissions if prompted

### Optional Enhancements

1. **Better Speech Recognition**:
   - Use Google Cloud Speech-to-Text for improved accuracy
   - Add credentials to `.env` file

2. **Local LLM Alternative**:
   - Use Hugging Face Transformers for offline operation
   - Uncomment the relevant code in `llm_handler.py`

3. **Custom Models**:
   - Change `gpt-3.5-turbo` to `gpt-4` in `llm_handler.py`
   - Adjust temperature and max_tokens for different responses

## Performance Optimization

The application is designed for optimal performance:

- **Multi-threading**: Audio processing and LLM queries run in separate threads
- **Queue System**: Prevents UI freezing during processing
- **Dynamic Energy Threshold**: Adapts to ambient noise levels
- **Efficient Question Detection**: Pattern matching without LLM calls

### Tips for Best Performance

1. Use a good quality microphone
2. Speak clearly and pause briefly after questions
3. Minimize background noise
4. Close unnecessary applications to free up resources

## Troubleshooting

### Common Issues

1. **"No module named 'pyaudio'"**:
   - Install system audio libraries (see Installation)
   - Run `pip install pyaudio`

2. **"API key not configured"**:
   - Check your `.env` file
   - Ensure the environment variable is set

3. **No audio detected**:
   - Check microphone permissions
   - Test microphone in system settings
   - Adjust `ENERGY_THRESHOLD` in code

4. **Slow responses**:
   - Check internet connection
   - Consider using GPT-3.5 instead of GPT-4
   - Reduce `max_tokens` in LLM calls

## Future Enhancements

- Image generation for visualizations (DALL-E integration)
- Export Q&A sessions to PDF
- Voice synthesis for answers
- Multiple language support
- Offline mode with local models
- Custom wake words
- Integration with educational APIs

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Ensure all dependencies are installed correctly
