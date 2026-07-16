from logistics_ml.etl.taxi_trips import load_taxi_trips
from logistics_ml.etl.download import download_data
from logistics_ml.etl.locations import load_locations
from logistics_ml.etl.training_view import create_training_view


def main():
    print("Starting ETL pipeline")

    download_data()
    load_taxi_trips()
    load_locations()
    create_training_view()

    print("ETL pipeline completed")


if __name__ == "__main__":
    main()
