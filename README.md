# DemoQA BDD Test Automation

Automated browser tests for DemoQA using Behave (Cucumber-style BDD), Selenium WebDriver, and Faker-generated data. The test suite covers the Practice Form, Browser Windows, and Web Tables workflows.

## Requirements

- Python 3.11+ (Python 3.13 recommended)
- Google Chrome browser
- Git

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-org>/<your-repo>.git
   cd <your-repo>
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

