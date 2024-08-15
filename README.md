# Mechanism Institute Library Scraper

This Python script automates the process of scraping data from the Mechanism Institute's library. It uses Selenium to control a Brave browser instance and extract data from web pages. The data is saved in both CSV and JSON formats.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Output](#output)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- Automatically scrolls to the bottom of the page to ensure all elements are loaded.
- Scrapes data and saves it to both CSV and JSON files.
- Configurable via environment variables, allowing easy setup on different machines.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.8 or higher
- Brave Browser
- Google ChromeDriver (compatible with your Brave version)
- [pip](https://pip.pypa.io/en/stable/)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/mechanism-scraper.git
   cd mechanism-scraper
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

   If the `requirements.txt` does not exist, you can install the dependencies manually:

   ```bash
   pip install selenium webdriver_manager python-dotenv pandas
   ```

## Setup

### Environment Variables

Create a `.env` file in the root of the project directory to store your environment-specific variables:

```bash
touch .env
```

Add the following lines to the `.env` file, replacing the placeholder paths with your actual paths:

```env
CHROMEDRIVER_PATH=/path/to/your/chromedriver
BRAVE_BROWSER_PATH=/Applications/Brave Browser.app/Contents/MacOS/Brave Browser
```

### Example `.env` File

```env
CHROMEDRIVER_PATH=/Users/your-username/Downloads/chromedriver
BRAVE_BROWSER_PATH=/Applications/Brave Browser.app/Contents/MacOS/Brave Browser
```

### Note

- Ensure that the ChromeDriver version matches the Brave browser version installed on your machine.
- Make the `chromedriver` binary executable if needed:

  ```bash
  chmod +x /path/to/your/chromedriver
  ```

## Usage

To run the script, use the following command:

```bash
python mechanism_scrape.py
```

The script will launch a headless Brave browser, navigate to the specified page, and scrape the data. The scraped data will be saved as both CSV and JSON files in the current directory.

## Output

The script generates two output files:

- `mechanism_institute_library.csv`: A CSV file containing the scraped data.
- `mechanism_institute_library.json`: A JSON file containing the scraped data.

## Troubleshooting

- **SessionNotCreatedException**: Ensure the ChromeDriver version matches the installed Brave browser version.
- **No Chrome Binary Error**: Check the `BRAVE_BROWSER_PATH` in the `.env` file to ensure it points to the correct location of the Brave binary.
- **Permission Denied Error**: Make sure that `chromedriver` is executable. Use `chmod +x /path/to/your/chromedriver`.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
