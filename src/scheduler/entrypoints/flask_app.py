from flask import Flask, jsonify, request

from scheduler.adapters.configurations import CsvConfigurationRepository
from scheduler.bootstrap import bootstrap
from scheduler.domain.model import Event
from scheduler.service_layer.services import process_event

app = Flask(__name__)
bootstrap()


@app.route("/events", methods=["POST"])
def events_endpoint():
    config_repository = CsvConfigurationRepository()
    event = Event.from_json(request.json)

    configurations_validated = process_event(config_repository, event)

    config_repository.dump()

    return jsonify({"configurations_validated": [c.name for c in configurations_validated]}), 202
