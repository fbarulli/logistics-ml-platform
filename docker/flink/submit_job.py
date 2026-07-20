import pathlib
import time

import requests

gateway = "http://sql-gateway:8083"

while True:
    try:
        if requests.get(f"{gateway}/v1/info").ok:
            break
    except Exception:
        pass
    time.sleep(2)

session = requests.post(f"{gateway}/v1/sessions").json()

session_id = session["sessionHandle"]

sql = pathlib.Path("/opt/flink/sql/run.sql").read_text()

for stmt in [x.strip() for x in sql.split(";") if x.strip()]:
    print(stmt)

    r = requests.post(
        f"{gateway}/v1/sessions/{session_id}/statements",
        json={"statement": stmt},
    )

    print(r.json())
