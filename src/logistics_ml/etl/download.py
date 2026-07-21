import urllib.request

from logistics_ml.config import data as data_config


def download_data():
    data_config.raw_data_dir.mkdir(parents=True, exist_ok=True)

    if data_config.raw_data_file.exists():
        print(f"✓ {data_config.raw_data_file} already exists.")
        return

    print(f"Downloading {data_config.raw_data_url}")
    urllib.request.urlretrieve(data_config.raw_data_url, data_config.raw_data_file)

    print(f"✓ Saved to {data_config.raw_data_file}")


def main():
    download_data()


if __name__ == "__main__":
    main()
