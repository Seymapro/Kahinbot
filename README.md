<div align="center">
    <img src=".github/seer.webp" width="300">
</div>

<h1 align="center">Kahin Bot</h1>

[![Chat with @ozetcibot on Telegram](https://img.shields.io/badge/Telegram-%40ozetcibot-blue)](https://t.me/ozetcibot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Telegram bot that tells your life story based on your birthdate according to Dan Millman's `The Life You Were Born to Live`.

> [!CAUTION]
> ⚠️ This project is still under active development. Expect frequent updates and changes to the structure and functionality of the notebooks. Use with caution, and regularly check for updates or modifications.

## Features

- Calculates your Life Path number based on your birthdate.
- Provides detailed information about your Life Path from both Dan Millman's and Douglas Forbes' perspectives (**TODO**).
- Offers different content formats including:
  - Full text
  - Summarized text
  - Bullet points
- Utilizes Google Gemini for paraphrasing and summarizing content in Turkish (**TODO:** for Douglas Forbes).

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Seymapro/Kitap.git kahin-bot
   cd kahin-bot
   ```

2. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
    - Create a `.env` file in the root directory.
    - Add the following environment variables to the `.env` file, replacing the placeholders with your actual API keys and tokens:

     ```bash
     KAHIN_BOT_API_ID=your_telegram_api_id
     KAHIN_BOT_API_HASH=your_telegram_api_hash
     KAHIN_BOT_BOT_TOKEN=your_telegram_bot_token
     GEMINI_API_KEY=your_google_gemini_api_key
     ```

## Usage

1. **Run the bot:**

   ```bash
   python kahin_bot.py
   ```

2. **Start a conversation with the bot on Telegram.**
3. **Send your birthdate in the format DD.MM.YYYY (e.g., 22.12.2002).**
4. **Follow the bot's instructions to choose the desired content format and source.**

## Data

The data directory (`data/`) is structured as follows:

```raw
data/
  |-- millman/
  |   |-- tr/
  |   |   |-- JSONs/
  |   |   |-- MDs/
  |   |   |-- Summarizations/
  |   |   |-- translate_JSON.ipynb
  |   |   |-- translate_md.ipynb
  |   |   |-- translate_summ.ipynb
  |   |-- en/
  |       |-- JSONs/
  |       |-- MDs/
  |       |-- Summarizations/
  |       |-- md_to_json.ipynb
  |       |-- pdf_prep.ipynb
  |       |-- pdf_to_md.ipynb
  |       |-- summarize.ipynb
  |-- forbes/
      |-- tr/
          |-- (TODO: Same structure as millman)
```

### millman/tr/

- **translate_md.ipynb**
  This notebook translates English Markdown files into Turkish using Google Gemini 1.5 Pro.

- **translate_JSON.ipynb**
  This notebook translates JSON objects into Turkish using Google Gemini 1.5 Pro.

- **translate_summ.ipynb**
  This notebook translates Markdown summarizations into Turkish using Google Gemini 1.5 Pro.

### millman/en/

- **pdf_prep.ipynb**
  Prepares PDF files by splitting the whole book's PDF into life paths for easier management and processing.

- **pdf_to_md.ipynb**
  Converts PDF files into Markdown files using Google Gemini 1.5 Pro.

- **md_to_json.ipynb**
  Converts Markdown files into JSON objects using Google Gemini 1.5 Pro.

- **summarize.ipynb**
  Summarizes both Markdown and JSON files into a plain text format for streamlined comprehension.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you would like to contribute to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Dan Millman for his insightful book `The Life You Were Born to Live`.
- Douglas Forbes for his work on Human Pin Code numbers (**TODO**).
- Google for providing the Gemini API.

## TODOs

- Implement Douglas Forbes' interpretations and content.
- Add more tests.
- Implement robust error handling.
- Improve documentation.

## MeslekBot

**MeslekBot**, uses the personality traits from KahinBot to recommend the most suitable academic department to users.

### Features

- Lists personality traits based on KahinBot's report.
- Verifies KahinBot's listed personality traits with the user before making a recommendation.
- The order of personality traits plays an important role in the analysis.
- Allows the user to manually edit the personality traits and their order if they are dissatisfied with KahinBot's analysis.
- Recommends a single department that best fits the personality.
- Provides the top 10 (or more) most suitable departments as an option. The suggestions are listed starting from the most suitable academic department for one's personality to the least.
- Can generate recommendations based on user-provided information without requiring KahinBot.
- All proffessions on **kariyer.net** are appointed to the personality traits that is mentioned in KahinBot's analyses (e.g. if one wants to be a teacher they must have these features: ...)
- The bot can return those required features when a profession is given as an input.

## Contact

If you have any questions or suggestions, feel free to contact me at [@Seymapro](https://github.com/Seymapro).
