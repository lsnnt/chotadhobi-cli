# ChotaDhobi CLI

A command-line interface for managing laundry services through the ChotaDhobi API.

## Demo

[![demo demonstrating the use](https://asciinema.org/a/1YYtxGLpH6JvTj7Y.svg)](https://asciinema.org/a/1YYtxGLpH6JvTj7Y)

## Installation

### Desktop (Linux / macOS / Windows)

1. Clone the repository:
   ```bash
   git clone https://github.com/lsnnt/chotadhobi-cli
   cd chotadhobi-cli
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate       # macOS / Linux
   # venv\Scripts\activate        # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Mobile (Termux on Android)

For a fresh Termux install, run these commands in order:

```bash
# 1. Update package lists and upgrade existing packages
pkg update && pkg upgrade -y

# 2. Install required system packages
pkg install -y python git

# 3. Clone the repository
git clone https://github.com/lsnnt/chotadhobi-cli
cd chotadhobi-cli

# 4. Install Python dependencies
pip install -r requirements.txt
```

> **Tip:** If you see QR codes rendering incorrectly, install a Termux-compatible font
> or try increasing your terminal font size. The [Termux:Styling](https://f-droid.org/en/packages/com.termux.styling/) add-on can help.

## Usage

```bash
python3 main.py
```

## Features

- **Login** — Authenticate using your VIT email and OTP
- **Send Clothes** — Request a wash with a specified number of clothes
- **Receive Clothes** — View recent washes and display QR codes for collection
- **View History** — Browse your complete wash history and show the QR code for any record
- **User Details** — Display your account information
- **Credential Storage** — Securely store and reuse login credentials via a local `.env` file

## How It Works

1. On first run, you'll be prompted to log in with your VIT email.
2. An OTP will be sent to your email — enter it to authenticate.
3. Your credentials (token and email) are saved locally in a `.env` file.
4. On subsequent runs, you can reuse saved credentials or log in again.
5. Use the menu to perform actions like sending or collecting clothes.

## QR Code for Collection

When sending or collecting clothes, a QR code is displayed in the terminal containing the `wash_id`. Show this QR code to the laundry staff for verification.

## Security

- The `.env` file is git-ignored and never committed to version control.
- Your token and email are stored locally only.
- All requests are made over HTTPS.

## Responsible AI Disclosure

`main.py` was generated with AI assistance based on the [reverse-engineered API docs](REVERSE_ENGINEERED_API_DOCS.md). The API documentation itself was independently researched and written by the author.

## Credits

Reverse engineered by [@lsnnt](https://github.com/lsnnt)
