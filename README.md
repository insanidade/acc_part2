# DemoQA BDD Test Automation

End-to-end browser automation suite for the DemoQA playground, built with Behave (Cucumber-style BDD), Selenium WebDriver, and Faker-driven data generation. It demonstrates modern UI testing practices—including form submissions, multi-window handling, dynamic tables, and time-based widgets—using readable scenarios and maintainable step definitions.

## Requirements

- Python 3.11+ (Python 3.13 recommended)
- Google Chrome browser
- Git

## Getting Started

1. **Clone the repository**

   ```bash
   git clone git@github.com:insanidade/acc_part2.git
   cd acc_part2
   ```

2. **Create (optional) and activate a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Running the Tests

- **Run the full suite**

  ```bash
  behave
  ```

- **Run a specific feature**

  ```bash
  behave features/practice_form.feature
  ```

## Test Coverage

- `features/practice_form.feature` – fills out DemoQA Practice Form with Faker data, uploads a file, asserts modal popup handling.
- `features/browser_windows.feature` – exercises multiple window handling by opening, validating, and closing a new browser window.
- `features/web_tables.feature` – creates, edits, and deletes table entries, including bulk creation of 12 records and cleanup verification.
- `features/progress_bar.feature` – manages the dynamic progress bar by pausing below 25%, waiting for completion, and validating reset behavior.

WebDriver binaries are managed automatically by `webdriver-manager`. Ensure Chrome is installed and up to date—the matching ChromeDriver will be downloaded into your user cache on the first run.

## Project Structure

- `features/` – Gherkin feature files and step definitions
- `features/environment.py` – Behave hooks for WebDriver setup/teardown
- `resources/` – Static assets such as uploaded files
- `requirements.txt` – Python dependencies

## Troubleshooting

- **ChromeDriver mismatches**: Update Chrome to the latest version and rerun the tests.
- **Stale browser sessions**: If a test aborts mid-run, manually close any remaining Chrome windows before rerunning.

## License

This project is provided under the MIT License. Adjust the license section if your repository uses a different license.

