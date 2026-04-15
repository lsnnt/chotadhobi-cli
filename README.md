# ChotaDhobi CLI

A command-line interface for managing laundry services through the ChotaDhobi API.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd chotadhobi-cli
```

2. Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the CLI:
```bash
python3 main.py
```

## Features

- **Login**: Authenticate using VIT email and OTP
- **Send Clothes**: Request a wash with a specified number of clothes
- **Receive Clothes**: View recent washes and show QR codes for collection
- **View History**: Browse complete wash history and select any record to display QR code
- **User Details**: Display your account information
- **Credential Storage**: Securely store and reuse login credentials in `.env`

## How It Works

1. On first run, you'll be prompted to login with your VIT email
2. An OTP will be sent to your email - enter it to authenticate
3. Your credentials (token and email) are securely stored in `.env`
4. On subsequent runs, you can reuse saved credentials or login again
5. Use the menu to perform various actions

## QR Code for Collection

When sending or collecting clothes, a QR code will be displayed in the terminal containing the `wash_id`. Show this QR code to the laundry staff for verification.

## Security

- `.env` file is ignored and never committed to version control
- Token and email are stored locally only
- Requests are made over HTTPS only
