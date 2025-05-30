<div align="center">
    <img src=".github/seer.webp" width="300">
</div>

<h1 align="center">Kahin Bot</h1>

[![Chat with @ozetcibot on Telegram](https://img.shields.io/badge/Telegram-%40ozetcibot-blue)](https://t.me/ozetcibot)
[![MIT License](https://img.shields.io/github/license/Seymapro/Kahinbot)](https://opensource.org/licenses/MIT)

Kahin Bot is a Telegram bot that analyzes your data — like birth date and selfies — to reveal insights about your personality, career path, and even potential health traits. Whether you're curious about your personality, exploring career options, or looking for health-related predictions, Kahin Bot provides engaging and thought-provoking analyses in a user-friendly chat interface.

> [!CAUTION]
> ⚠️ This project is still under active development. Expect frequent updates and changes to the structure and functionality of the codebase. Use with caution, and regularly check for updates or modifications.

## Features

- Provides detailed information about your personality traits from both Dan Millman's and Douglas Forbes' perspectives
- Offers different content formats including:
  - Full text
  - Summarized text
  - Bullet points
- Utilizes Google Gemini for paraphrasing and summarizing content in Turkish
- Provides personality traits based on astrological analysis

## Installation

1. **Clone the repository:**

   ```bash
   git clone --depth=1 -b main https://github.com/Seymapro/Kahinbot.git kahin-bot
   cd kahin-bot
   ```

2. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
    - Add the following environment variables to your environment, replacing the placeholders with your actual API keys and tokens:

     ```desktop
     KAHIN_BOT_API_ID=your_telegram_api_id
     KAHIN_BOT_API_HASH=your_telegram_api_hash
     KAHIN_BOT_BOT_TOKEN=your_telegram_bot_token
     GEMINI_API_KEY=your_google_gemini_api_key
     ```

### Testing

1. **Go to the tests directory:**

    ```bash
    cd ./tests/
    ```

2. **Run all of the tests:**

    ```bash
    python -m unittest
    ```

## Deployment

1. **Copy the systemd service file to systemd folder:**

    ```bash
    cp ./kahin-bot.service /etc/systemd/system/
    ```

2. **Start the service:**

    ```bash
    sudo systemctl start kahin-bot
    ```

3. **To stop the service:**

    ```bash
    sudo systemctl stop kahin-bot
    ```

## Usage

1. **Run the bot:**

   ```bash
   python bot.py
   ```

2. **Start a conversation with the bot ([@ozetcibot](https://t.me/ozetcibot)) on Telegram**
3. **Follow the bot's instructions to choose the desired content**

## Data

We use the following books for our data:

- [The Life You Were Born to Live](https://www.peacefulwarrior.com/the-life-you-were-born-to-live/) by Dan Millman
  - **SHA256 Hash**: `DD579B23FAAAF0017C06FCFD8BBDD6937D1BF4F1601EE8C44941D4E5348D9149`
- [Human Pin Code](https://humanpincode.com/) by Douglas Forbes
  - **SHA256 Hash**: `839048F70036CFEE0B446B183F6579D39A376FD07E7511FE1BD12950FDE7C2ED`

The data directory (`data/`) is structured as follows:

```raw
data/
├── enneagrams
├── forbes
│   └── tr
│       ├── MDs
│       ├── PDFs
│       └── Summarizations
└── millman
    ├── en
    │   ├── JSONs
    │   ├── MDs
    │   ├── PDFs
    │   └── Summarizations
    └── tr
        ├── JSONs
        ├── JSONs_Extended
        ├── MDs
        └── Summarizations
```

## Contributing

Contributions are always welcome! Please open an issue or submit a pull request if you would like to contribute to the project. See [CONTRIBUTING](.github/CONTRIBUTING.md) for ways to get started. Please adhere to this project's [CODE OF CONDUCT](.github/CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Dan Millman for his insightful book [The Life You Were Born to Live](https://www.peacefulwarrior.com/the-life-you-were-born-to-live/).
- Douglas Forbes for his book titled [Human Pin Code](https://humanpincode.com/).
- Google for providing the Gemini API.
- @ozefe for his assistance and guidance.

## Contact

If you have any questions or suggestions, feel free to contact me at [@Seymapro](https://github.com/Seymapro).
