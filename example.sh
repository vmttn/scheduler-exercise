# Exit immediately if a command exits with a non-zero status.
set -e

# Trace execution
set -x

HEADERS="Content-Type: application/json"
URL="http://localhost:8000/events"
DATE_COMMAND="date -Is -u"

curl -X POST "${URL}" -H "${HEADERS}" \
    -d "{\"eventType\":\"FILE\",\"eventResourceId\":\"/scheduling_configuraiton_1/directory/path/file_1.txt\",\"eventTimestamp\":\"$(${DATE_COMMAND})\"}"

curl -X POST "${URL}" -H "${HEADERS}" \
    -d "{\"eventType\":\"TIME_BASED\",\"eventResourceId\":\"cron\",\"eventTimestamp\":\"$(${DATE_COMMAND})\"}"