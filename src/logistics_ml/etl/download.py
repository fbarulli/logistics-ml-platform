import urllib.request

from logistics_ml.config import (
    DATA_DIR,
    RAW_DATA_FILE,
    RAW_DATA_URL,
)


def download_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if RAW_DATA_FILE.exists():
        print(f"✓ {RAW_DATA_FILE} already exists.")
        return

    print(f"Downloading {RAW_DATA_URL}")
    urllib.request.urlretrieve(RAW_DATA_URL, RAW_DATA_FILE)

    print(f"✓ Saved to {RAW_DATA_FILE}")


def main():
    download_data()


if __name__ == "__main__":
    main()
