"""Create Polymarket API credentials from your private key.

Run with: python -m src.create_api_keys
Add the output to your .env file.
"""

import os
from dotenv import load_dotenv
from py_clob_client.client import ClobClient

load_dotenv()


def main():
    host = "https://clob.polymarket.com"
    key = os.getenv("POLYMARKET_PRIVATE_KEY")
    chain_id = 137  # Polygon Mainnet

    if not key:
        raise ValueError(
            "Private key not found. Set POLYMARKET_PRIVATE_KEY in .env or environment."
        )

    client = ClobClient(host, key=key, chain_id=chain_id)
    try:
        api_creds = client.create_or_derive_api_creds()
        print("API Key:", api_creds.api_key)
        print("Secret:", api_creds.api_secret)
        print("Passphrase:", api_creds.api_passphrase)
        print()
        print("Add these to your .env file:")
        print("  POLYMARKET_API_KEY=" + api_creds.api_key)
        print("  POLYMARKET_API_SECRET=" + api_creds.api_secret)
        print("  POLYMARKET_API_PASSPHRASE=" + api_creds.api_passphrase)
    except Exception as e:
        print("Error creating API credentials:", e)


if __name__ == "__main__":
    main()
