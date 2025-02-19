<div align="center">

# Timewatch Automation Script

# ⏰💼🤖

This is a Python script to automate the process of logging work hours on the Timewatch platform.

</div>

## Features

- Automated login to Timewatch.
- Automated filling of work hours based on configuration.
- Handling of holidays and absence days.
- Configurable working hours and time thresholds.

## Prerequisites

- Python 3.8+
- Google Chrome browser
- ChromeDriver

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging. Follow the steps below to set up the project.

### Step 1: Install Poetry

If you haven't installed Poetry yet, you can do so by following the instructions on the [official Poetry documentation](https://python-poetry.org/docs/#installation).

### Step 2: Clone the Repository

```bash
git clone https://github.com/nirberko/TimeWatchAutomator.git
cd TimeWatchAutomator
```

### Step 3: Install Dependencies

```bash
poetry install
```

### Step 4: Set Up ChromeDriver

Download the version of ChromeDriver that matches your version of Google Chrome from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

Once downloaded, make sure that the `chromedriver` executable is in your PATH. For example, you can place it in `/usr/local/bin` or any directory that is included in your PATH.

## Usage

### Step 1: Generate Configuration

Run the script to generate the configuration file:

```bash
poetry run python timewatch_automation.py
```

Follow the prompts to enter your company ID, user ID, password, entrance hour, leaving hour, and time threshold. The configuration will be saved in a file named `config.json` in the `config` directory.

### Step 2: Run the Script

Once the configuration file is generated, you can run the script to automate the logging of your work hours:

```bash
poetry run python timewatch_automation.py
```

## Configuration

The configuration file `config.json` is generated during the initial setup and stored in the `config` directory. Here is an example of what the configuration file looks like:

```json
{
  "company_id": "your_company_id",
  "user_id": "your_user_id",
  "password": "your_password",
  "entrance_hour": "09:00",
  "leaving_hour": "18:00",
  "time_threshold_sec": 2
}
```

- `company_id`: Your company's ID for Timewatch.
- `user_id`: Your user ID for Timewatch.
- `password`: Your password for Timewatch (stored in plain text).
- `entrance_hour`: Default entrance hour (e.g., "09:00").
- `leaving_hour`: Default leaving hour (e.g., "18:00").
- `time_threshold_sec`: Time in seconds to wait between actions (default is 2 seconds).

## Troubleshooting

- Make sure that the `config.json` file is correctly generated and located in the `config` directory.
- Ensure that the ChromeDriver version matches your Google Chrome version.
- Check your internet connection and ensure that the Timewatch website is accessible.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Contact

If you have any questions or issues, feel free to open an issue on the repository or contact the maintainer.
