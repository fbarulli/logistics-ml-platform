from pathlib import Path
import urllib.request

URL = (
    "https://d37ci6vzurychx.cloudfront.net/"
    "trip-data/yellow_tripdata_2024-01.parquet"
)

DATA_DIR = Path("data/raw")
OUTPUT_FILE = DATA_DIR / "yellow_tripdata_2024-01.parquet"


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if OUTPUT_FILE.exists():
        print(f"✓ {OUTPUT_FILE} already exists.")
        return

    print(f"Downloading {URL}")
    urllib.request.urlretrieve(URL, OUTPUT_FILE)

    print(f"✓ Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
