# Briefly Telegram Bot

Briefly is a Telegram bot that summarizes audio files, voice messages, and YouTube videos. It uses OpenAI's GPT-4o model for generating summaries and transcriptions.

## Features

- Summarizes audio files and voice messages.
- Summarizes YouTube videos by extracting subtitles or transcribing audio.
- Supports multiple languages.
- Allows users to ask questions about the summarized content.

## Installation

### Prerequisites

- Python 3.10+
- Docker
- Docker Compose

### Clone the Repository

```sh
git clone https://github.com/yourusername/briefly.git
cd briefly
```

### Create and Activate Virtual Environment

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

### Install Dependencies

```sh
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a `.env` file in the root directory and add the following variables:

```
API_KEY=your_telegram_bot_api_key
OPENAI_API_KEY=your_openai_api_key
```

### Initialize the Database

```sh
python -m database.models
```

### Run the Bot

```sh
python main.py
```

## Usage

1. Start the bot on Telegram.
2. Send an audio file, voice message, or YouTube link to the bot.
3. The bot will transcribe and summarize the content.
4. You can ask questions about the summarized content.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License.