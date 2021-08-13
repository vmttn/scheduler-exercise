# `Event-based Scheduler`

## Documentation

### Project

    .
    ├── data/               # Our persisted data
    ├── src/scheduler/      # The scheduler app packaged
    |   ├── adapters/       # Abstractions of the persistence layer
    |   ├── domain/         # Domain modelling of the problem
    |   ├── service_layer/  # Usecase of that domain
    |   └── entrypoints/    # Entrypoint to our usecases (an Flask API)
    ├── tests/
    └── example.sh          # High-level example

### About the persistence

The persistence layer simply consists of CSV files, which is enough for our simple usecase (1 user, no isolation needed).

## Usage

### Installing the dependencies

```sh
python3.8 -m venv --prompt scheduler .venv
source .venv/bin/activate
pip install -rrequirements/base.txt
```

### Running the test suite

Make sure `tox` is available (either through the newly created venv or with `pipx`).

```sh
tox
```

### Running the api

```sh
docker-compose up -d
```

### Playing an example

```sh
./example.sh
```

### Changing the configurations

Edit the `data/configurations.csv` and `data/dependencies.csv` files.

#### `data/configurations.csv`

| name | last_execution               |
|------|------------------------------|
| ...  | (Optional) iso8601 timestamp |

#### `data/dependencies.csv`

| config_name            | type                                  | resource_id | life_duration | timestamp                                                                  |
|------------------------|---------------------------------------|-------------|---------------|----------------------------------------------------------------------------|
| associated config name | `FILE` or `TIME_BASED` or `BIG_QUERY` | ...         | in seconds    | (Optional) iso8601 timestamp for the last event validating this dependency |
