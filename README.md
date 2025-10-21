# Auto Timestamp

![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.13-g.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

**Automated Python tool to modify file timestamps based on date/time patterns extracted from filenames. Supports auto-detection and manual mode.**

---

## Table of Contents

- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Changelog](#changelog)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

---

## How It Works

The script uses **intelligent pattern matching** to extract date and time from ANY filename format.

### Detection Algorithm

The script searches for two specific patterns in the filename:
- **8 consecutive digits** → Date format `YYYYMMDD`
- **6 consecutive digits** → Time format `HHMMSS`

If **both patterns are found**, the script will modify:
- Creation date
- Modification date  
- Last access date

### Example

For a file named `document_20251011_153000.pdf`:
1. Extracts `20251011` (date) → October 11, 2025
2. Extracts `153000` (time) → 15:30:00
3. Returns a datetime: `2025-10-11 15:30:00`
4. Applies to the file's timestamps

**As long as the filename contains 8 digits for date and 6 digits for time, it will work.**

---

## Installation

Clone the repository and navigate to the script:

```bash
git clone https://github.com/Airbank1/auto-timestamp.git
cd auto-timestamp
```

### Prerequisites

- Python 3.13 installed
- Windows OS (for creation date modification)

---

## Usage

### Automatic Mode

Place the script in a folder with files to process and run it:

```bash
python auto_timestamp.py
```

The script will:
1. Scan all files in the current directory
2. Extract date/time patterns automatically using regex
3. Modify file timestamps accordingly
4. Display a colored progress bar during processing
5. Show summary of processed and unprocessed files

### Manual Mode

If some files don't match the automatic pattern (no YYYYMMDD + HHMMSS found), the script enters **manual mode**:

1. Select a file from the list (by number or filename)
2. Enter the desired date and time (without seconds)
3. The file timestamp is updated instantly

**Supported manual input formats:**
```
24/08/2025 17:36     → Full date and time
Hier à 20:29         → Yesterday at specific time (French)
20:29                → Today at specific time
[Empty]              → Cancel operation
```

---

## Project Structure

```
auto-timestamp/
├── auto_timestamp.py          # Main script
├── README.md                  # Documentation
├── LICENSE                    # AGPL-3.0 License
└── .gitignore                 # Git ignore rules
```

---

## Architecture

The script is organized into **12 main classes** for maintainability and extensibility:

**Configuration & System:**
- `Config` - Global configuration and constants
- `SystemUtils` - System-level utilities (screen clear, CMD maximize)
- `FileSystemUtils` - File operations and timestamp modification

**Data Processing:**
- `DateTimeParser` - Date/time extraction using regex and parsing
- `TextFormatter` - Text and filename formatting utilities

**User Interface:**
- `HeaderRenderer` - ASCII art headers
- `ProgressBarRenderer` - Real-time progress visualization
- `BoxRenderer` - Colored terminal boxes for results

**Business Logic:**
- `AutoProcessor` - Automatic file processing workflow
- `ManualProcessor` - Manual timestamp modification workflow
- `ResultsDisplayManager` - Results display and formatting
- `ApplicationManager` - Main application orchestration

---

## Changelog

See the [commit history](../../commits/main) for detailed changes.

---

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

### What does this mean?

**You can:**
- Use this code for free (personal, education, commercial)
- Modify it however you want
- Keep it private on your computer (no need to share)
- Integrate parts of it in your own projects

**If you share/publish your code** (GitHub, website, app):
- Mention the original repo in a comment:  
```# Based on: https://github.com/Airbank1/auto-timestamp```
- If it's a public service/SaaS, your code must be open source too (AGPL requirement)

### Important Notice

**For developers using this code:**

- **Using code snippets?** Just add a comment linking to this repo
- **Using the whole script?** Keep the copyright header in the main file
- **Private modifications?** Do whatever you want, no restrictions
- **Public project?** Mention this repo somewhere (README, code comment, etc.)

### Commercial Use

If you want to use this code in a **closed-source commercial product** (including SaaS/cloud services), you need a commercial license.

For commercial licensing inquiries, please contact me.

**Note:** Fair use in internal company tools (not redistributed) is acceptable. When in doubt, just ask.

---

## Acknowledgments

This project was developed to solve a real-world problem: managing thousands of downloaded files with incorrect timestamps.

**This project is currently in active development.** Ideas, issues, and feature requests are welcome!

Special thanks to the Python community for the excellent documentation and tools.

---

## Contact

- **GitHub:** [@Airbank1](https://github.com/Airbank1)
- **Issues:** [Report a bug or request a feature](../../issues)

---

<div align="right">

**Made with care by Airbank1**

</div>
