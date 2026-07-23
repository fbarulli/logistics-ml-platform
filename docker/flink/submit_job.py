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

expanded = []
for line in sql.splitlines():
    line = line.strip()
    if line.startswith("SOURCE"):
        path = line.split("'")[1]
        expanded.append(pathlib.Path(path).read_text())
    else:
        expanded.append(line)

sql = "\n".join(expanded)

for stmt in [x.strip() for x in sql.split(";") if x.strip()]:
    print(stmt)

    r = requests.post(
        f"{gateway}/v1/sessions/{session_id}/statements",
        json={"statement": stmt},
    )

    response = r.json()
    print(response)

    if "operationHandle" in response:
        operation = response["operationHandle"]

        while True:
            status = requests.get(
                f"{gateway}/v1/sessions/{session_id}/operations/{operation}/status"
            ).json()

            print(status)

            if status.get("status") in ["FINISHED", "ERROR"]:
                break

            time.sleep(5)
