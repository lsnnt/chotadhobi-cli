#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import qrcode
import requests
from dotenv import load_dotenv, set_key

BASE_URL = "https://apichotadhobi.rdgroupco.com"
ENV_FILE = Path.cwd() / ".env"
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
}

# Load environment variables
load_dotenv(ENV_FILE)


def print_qr_code(data: str) -> None:
    qr = qrcode.QRCode(border=2)
    qr.add_data(data)
    qr.make(fit=True)
    matrix = qr.get_matrix()

    print("\nQR code for:", data)
    for row in matrix:
        line = "".join("██" if cell else "  " for cell in row)
        print(line)
    print()


def save_credentials(token: str, email: str) -> None:
    """Save token and email to .env file."""
    set_key(str(ENV_FILE), "CHOTADHOBI_TOKEN", token)
    set_key(str(ENV_FILE), "CHOTADHOBI_EMAIL", email)
    print("Credentials saved to .env file.")


def load_credentials():
    """Load token and email from .env file."""
    token = os.getenv("CHOTADHOBI_TOKEN")
    email = os.getenv("CHOTADHOBI_EMAIL")
    return token, email


def request_json(session: requests.Session, method: str, endpoint: str, payload=None, params=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = session.get(url, params=params, timeout=20)
        else:
            response = session.post(url, json=payload, timeout=20)
    except requests.exceptions.RequestException as exc:
        print("Network error:", exc)
        return None

    try:
        data = response.json()
    except ValueError:
        print("Invalid response from server:", response.text)
        return None

    if not response.ok:
        print(f"Request failed ({response.status_code}):", data)
        return None

    return data


def login_flow(session: requests.Session):
    print("=== ChotaDhobi CLI Login ===")
    email = input("Enter your VIT email: ").strip()
    if not email:
        print("Email is required.")
        return False

    otp_request = request_json(
        session,
        "POST",
        "/dhobi/v2/common/generateLoginOtp",
        payload={"role": "user", "email_address": email},
    )
    if otp_request is None:
        return False

    print("OTP request succeeded. Check your email and enter the OTP below.")
    otp = input("Enter OTP: ").strip()
    if not otp:
        print("OTP is required.")
        return False

    verify = request_json(
        session,
        "POST",
        "/dhobi/v2/common/verifyLoginOtp",
        payload={"email_address": email, "otp": otp},
    )
    if verify is None or "token" not in verify:
        print("Login failed. Please try again.")
        return False

    token = verify["token"]
    session.headers.update({"Authorization": f"Bearer {token}"})
    save_credentials(token, email)
    print("Login successful.")
    return True


def fetch_user_details(session: requests.Session):
    data = request_json(session, "GET", "/dhobi/v2/common/userDetails")
    if data is None:
        return
    print("\n=== User Details ===")
    for field in ["name", "email_address", "org_id", "role", "is_active", "created_at"]:
        if field in data:
            print(f"{field}: {data[field]}")
    print("====================\n")


def request_wash(session: requests.Session):
    print("\n=== Request Clothes Wash ===")
    
    # Check for existing requested washes
    params = {
        "pageSize": 30,
        "pageNumber": 1,
        "wash_status": "requested",
    }
    existing_washes = request_json(session, "GET", "/dhobi/v2/wash/searchWash", params=params)
    
    if existing_washes and existing_washes.get("data"):
        washes_list = existing_washes.get("data", [])
        print(f"\nFound {len(washes_list)} existing wash request(s) with status 'requested':")
        for index, wash in enumerate(washes_list, start=1):
            requested_date = wash.get("wash_requested_date", "-")
            count = wash.get("clothes_count", "-")
            wash_id = wash.get("wash_id", "-")
            print(f"\n{index}. Wash ID: {wash_id}")
            print(f"   Clothes Count: {count}")
            print(f"   Requested Date: {requested_date}")
            print(f"   Full Details:")
            print(json.dumps(wash, indent=6))
            print(f"\n   QR Code:")
            print_qr_code(wash_id)
        
        create_new = input("Do you want to create a new wash request anyway? (y/n): ").strip().lower()
        if create_new != 'y':
            print("Exiting without creating a new request.")
            return
    
    # Proceed with creating a new wash request
    clothes_count = input("\nHow many clothes do you want to send? ").strip()
    if not clothes_count.isdigit() or int(clothes_count) <= 0:
        print("Please enter a positive integer for clothes count.")
        return

    user_comment = input("Optional comment for the wash request: ").strip()
    payload = {"clothes_count": str(clothes_count), "user_comment": user_comment}
    result = request_json(session, "POST", "/dhobi/v2/wash/requestWash", payload=payload)
    if result is None:
        return

    wash_id = result.get("wash_id")
    if not wash_id:
        print("No wash_id returned.")
        return

    print("Wash request created successfully.")
    print(json.dumps(result, indent=2))
    print_qr_code(wash_id)
    print(f"Saved QR code for wash_id: {wash_id}\n")


def search_recent_washes(session: requests.Session):
    params = {
        "pageSize": 10,
        "pageNumber": 1,
        "wash_status": "washing,requested,completed",
    }
    result = request_json(session, "GET", "/dhobi/v2/wash/searchWash", params=params)
    if result is None:
        return []

    return result.get("data", [])

def show_history(session: requests.Session):
    params = {
        "pageSize": 30,
        "pageNumber":1,
    }
    result = request_json(session, "GET", "/dhobi/v2/wash/searchWash", params=params)
    if result is None:
        return []
    return result.get("data",[])


def view_wash_history(session: requests.Session):
    print("\n=== View Wash History ===")
    washes = show_history(session)
    if not washes:
        print("No wash history found.")
        return

    print(f"Found {len(washes)} wash records.")
    for index, wash in enumerate(washes, start=1):
        requested_date = wash.get("wash_requested_date", "-")
        status = wash.get("wash_status", "-")
        count = wash.get("clothes_count", "-")
        wash_id = wash.get("wash_id", "-")
        print(f"{index}. {wash_id} | status={status} | clothes={count} | requested={requested_date}")

    while True:
        choice = input(
            "\nEnter the number of a wash to show its QR code, or 'q' to return to main menu: "
        ).strip()
        
        if choice.lower() == 'q':
            return
        
        if choice.isdigit():
            selected_index = int(choice)
            if 1 <= selected_index <= len(washes):
                selected_wash = washes[selected_index - 1]
                wash_id = selected_wash.get("wash_id")
                if wash_id:
                    print("\nDisplaying QR code for the selected wash record:")
                    print_qr_code(wash_id)
                else:
                    print("Selected record has no wash_id.")
            else:
                print("Invalid selection. Please try again.")
        else:
            print("Invalid input. Please enter a number or 'q' to go back.")


def receive_clothes(session: requests.Session):
    print("\n=== Receive / Collect Clothes ===")
    washes = search_recent_washes(session)
    if not washes:
        print("No recent washes found with status washing, requested, or completed.")
        return

    print(f"Found {len(washes)} recent wash records.")
    for index, wash in enumerate(washes, start=1):
        requested_date = wash.get("wash_requested_date", "-")
        status = wash.get("wash_status", "-")
        count = wash.get("clothes_count", "-")
        wash_id = wash.get("wash_id", "-")
        print(f"{index}. {wash_id} | status={status} | clothes={count} | requested={requested_date}")

    choice = input(
        "Enter the number of a wash to show its QR code, or press Enter to show the most recent: "
    ).strip()
    selected = 1
    if choice.isdigit():
        selected_index = int(choice)
        if 1 <= selected_index <= len(washes):
            selected = selected_index
        else:
            print("Invalid selection, showing the most recent record.")

    selected_wash = washes[selected - 1]
    wash_id = selected_wash.get("wash_id")
    if not wash_id:
        print("Selected record has no wash_id.")
        return

    print("\nDisplaying QR code for the selected wash record:")
    print_qr_code(wash_id)
    print("Ask the user to show this QR code while collecting their clothes.")


def main():
    session = requests.Session()
    session.headers.update(HEADERS)

    print("Welcome to ChotaDhobi CLI")
    
    # Try to load existing credentials
    token, email = load_credentials()
    if token and email:
        print(f"Found existing session for {email}")
        use_existing = input("Use existing credentials? (y/n): ").strip().lower()
        if use_existing == 'y':
            session.headers.update({"Authorization": f"Bearer {token}"})
            print("Session restored.")
        else:
            print("Please complete the login flow.")
            if not login_flow(session):
                return
    else:
        print("Please complete the login flow first.")
        if not login_flow(session):
            return

    while True:
        print("\nSelect an action:")
        print("1. Send clothes (request wash)")
        print("2. Receive clothes (show recent wash QR code)")
        print("3. Show user details")
        print("4. View wash history")
        print("5. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            request_wash(session)
        elif choice == "2":
            receive_clothes(session)
        elif choice == "3":
            fetch_user_details(session)
        elif choice == "4":
            view_wash_history(session)
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)
