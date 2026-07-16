from sklearn.model_selection import train_test_split

from logistics_ml.config import RANDOM_STATE


from logistics_ml.config import FEATURES, TARGET, RANDOM_STATE

TARGET = "trip_duration_minutes"


def prepare_data(df):
    X = df[FEATURES]
    y = df[TARGET]

    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
    )
