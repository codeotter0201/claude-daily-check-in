#!/usr/bin/env python3
"""
Log Q&A check results to CSV file
Based on ADR-003 decision for simple Q&A health check feature
"""

import csv
import os
import argparse
from datetime import datetime, timezone, timedelta


def log_qa_check(token_id: str) -> None:
    """
    Log Q&A check result to monthly CSV file

    Args:
        token_id: Token identifier (e.g., TOKEN_1, TOKEN_2)
    """
    # Get current UTC time
    now_utc = datetime.now(timezone.utc)

    # Determine CSV filename in logs directory (logs/YYYYMM-session-log.csv)
    filename = f"logs/{now_utc.strftime('%Y%m-session-log.csv')}"

    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    # Check if file exists
    file_exists = os.path.exists(filename)

    # Write Q&A check record
    with open(filename, "a", newline="") as csvfile:
        if not file_exists:
            # Create header if file doesn't exist
            writer = csv.writer(csvfile)
            writer.writerow(["timestamp", "event_type", "token_id", "reset_time_utc8"])
            print(f"Created new CSV file: {filename}")

        # Write Q&A check record
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                now_utc.strftime("%Y-%m-%d %H:%M:%S"),
                "SESSION-RESET-TRIGGER",
                "TOKEN_1" if token_id == "TOKEN_1" else "TOKEN_2",
                (now_utc + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"),
            ]
        )

    print(f"Q&A check logged to {filename} - Token: {token_id}")


def main():
    """Main function to parse arguments and log Q&A check"""
    parser = argparse.ArgumentParser(description="Log Q&A check result to CSV")
    parser.add_argument(
        "--token", required=True, help="Token identifier (e.g., TOKEN_1)"
    )

    args = parser.parse_args()

    # Log the Q&A check
    log_qa_check(args.token)


if __name__ == "__main__":
    main()
