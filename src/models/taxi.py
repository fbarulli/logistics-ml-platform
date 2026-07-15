from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import Base


class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True)
    borough = Column(String)
    zone = Column(String)

    pickup_trips = relationship(
        "TaxiTrip",
        foreign_keys="TaxiTrip.pickup_location_id"
    )

    dropoff_trips = relationship(
        "TaxiTrip",
        foreign_keys="TaxiTrip.dropoff_location_id"
    )


class TaxiTrip(Base):
    __tablename__ = "taxi_trips"

    id = Column(Integer, primary_key=True)

    vendor_id = Column(Integer)

    pickup_datetime = Column(DateTime)
    dropoff_datetime = Column(DateTime)

    passenger_count = Column(Integer)
    trip_distance = Column(Float)

    pickup_location_id = Column(
        Integer,
        ForeignKey("locations.location_id")
    )

    dropoff_location_id = Column(
        Integer,
        ForeignKey("locations.location_id")
    )

    fare_amount = Column(Float)
    tip_amount = Column(Float)
    total_amount = Column(Float)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)

    trip_id = Column(
        Integer,
        ForeignKey("taxi_trips.id")
    )

    model_version = Column(String)

    predicted_duration = Column(Float)

    prediction_time = Column(DateTime)
