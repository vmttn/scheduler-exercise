from datetime import datetime


def test_can_trigger_job(api_client, scheduling_configuration_1):
    data = {
        "eventType": "FILE",
        "eventResourceId": "/scheduling_configuraiton_1/directory/path/file_1.txt",
        "eventTimestamp": datetime.utcnow().isoformat(),
    }

    response = api_client.post("/events", json=data)

    assert response.status_code == 202
    assert response.json["configurations_validated"] == []

    data = {
        "eventType": "TIME_BASED",
        "eventResourceId": "cron",
        "eventTimestamp": datetime.utcnow().isoformat(),
    }

    response = api_client.post("/events", json=data)

    assert response.status_code == 202
    assert response.json["configurations_validated"] == ["SCHEDULING_CONFIGURATION_1"]
