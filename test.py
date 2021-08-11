from argparse import ArgumentParser
from json import loads
from os.path import exists
from requests import post

if __name__ == "__main__":
    parser = ArgumentParser(description='Test API')
    parser.add_argument('events_file', help='Events JSON file', action='store')
    parser.add_argument('--api_url', help='API url', default='http://localhost:5000', action='store')
    args = parser.parse_args()

    if not exists(args.events_file):
        print(f"Events file does not exist: {args.events_file}")
        exit(1)

    with open(args.events_file, mode='r') as file:
        for line in file.readlines():
            payload = loads(line)
            response = post(args.api_url, json=payload)
            print(f"{response.status_code} {response.text}")
