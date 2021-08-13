from scheduler.utils.time import get_tz_time


def test_can_trigger_job(api_client, scheduling_configuration_1):
    data = {
        "eventType": "FILE",
        "eventResourceId": "/scheduling_configuraiton_1/directory/path/file_1.txt",
        "eventTimestamp": get_tz_time().isoformat(),
    }

    response = api_client.post("/events", json=data)

    assert response.status_code == 202
    assert response.json["configurations_validated"] == []

    data = {
        "eventType": "TIME_BASED",
        "eventResourceId": "cron",
        "eventTimestamp": get_tz_time().isoformat(),
    }

    response = api_client.post("/events", json=data)

    assert response.status_code == 202
    assert response.json["configurations_validated"] == ["SCHEDULING_CONFIGURATION_1"]
