import urllib.request

from logistics_ml.config import data as data_config


def download_data():
    data_config.raw_data_dir.mkdir(parents=True, exist_ok=True)

    for url in data_config.taxi_urls:
        filename = url.split("/")[-1]
        target = data_config.raw_data_dir / filename

        if target.exists():
            print(f"✓ {target} already exists.")
            continue

        print(f"Downloading {url}")
        urllib.request.urlretrieve(url, target)

        print(f"✓ Saved to {target}")


def main():
    download_data()


if __name__ == "__main__":
    main()
