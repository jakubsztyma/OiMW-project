import json
from collections import defaultdict

import requests
import websocket

# try:
#    import thread
# except ImportError:
#    import _thread as thread


def validate_response(response_data, response):
    if not response_data["success"]:
        raise NameError(f"UCI Server error: {response.content}")


def extract_engine_names(engines_info):
    test = engines_info[0]
    names = list(engine["name"] for engine in engines_info)
    return names


def select_engine_to_start(available_engine_names, engine_name):
    if len(available_engine_names) == 0:
        raise NameError("No engines available")

    if engine_name is not None:
        if engine_name in available_engine_names:
            selected_engine = engine_name
        else:
            raise NameError(f"No engine available with name {engine_name}")
    else:
        selected_engine = available_engine_names[0]

    return selected_engine


def process_response_lines(lines):
    response = defaultdict(list)
    meaningful_words = ["depth", "cp"]

    info_lines = [line for line in lines if "info depth" in line]
    for info_line in info_lines:
        if "multipv" not in info_line:
            continue
        info_dict = {}
        splitted_line = info_line.split(" ")
        for index, word in enumerate(splitted_line):
            if word in meaningful_words:
                info_dict[word] = splitted_line[index + 1]

        pvs = info_line.split(" pv ")[1]
        info_dict["pv"] = pvs.split(" ")[0]

        depth = int(info_dict.pop('depth'))
        response[depth].append(info_dict)
    return response


class UCIHttpClient:
    def __init__(self, alt, cpu_cores):
        configuration = self.get_config()
        self.uri = configuration["uci_server_url"]
        self.socket_uri = configuration["uci_server_socket_url"]
        self.username = configuration["login"]
        self.password = configuration["password"]
        self.token = ""
        self.socket = None
        self.log_in()
        self.start_engine()
        self.initialize_socket(alt, cpu_cores)

    def log_in(self):
        payload = {"login": self.username, "password": self.password}
        r = requests.post(
            self.uri + "user/login",
            data=json.dumps(payload),
            headers=self.get_default_headers(),
        )
        response = r.json()

        validate_response(response, r)

        self.token = response["token"]
        print("Logged successfully to UCI server")

    def get_default_headers(self):
        return {
            "content-type": "application/json; charset=UTF-8",
            "content-length": "36",
            "authorization": f"Bearer {self.token}",
        }

    def get_available_engine_names(self):
        r = requests.get(
            self.uri + "engine/available", headers=self.get_default_headers()
        )
        response = r.json()

        validate_response(response, r)

        engines_info = response["info"]
        engine_names = extract_engine_names(engines_info)
        return engine_names

    def start_engine(self, engine_name=None):
        available_engine_names = self.get_available_engine_names()
        selected_engine = select_engine_to_start(available_engine_names, engine_name)
        payload = {"engine": selected_engine}
        r = requests.post(
            self.uri + "engine/start",
            data=json.dumps(payload),
            headers=self.get_default_headers(),
        )
        response = r.json()
        validate_response(response, r)

        print(f"Engine {selected_engine} successfully started")

    def initialize_socket(self, alt, cpu_cores):
        self.socket = websocket.WebSocket(header=self.get_default_headers())
        self.socket.connect(self.socket_uri, header=self.get_default_headers())
        self.socket.send(f"setoption name Threads value {cpu_cores}")
        self.socket.send(f"setoption name MultiPV value {alt}")

    def analyse(self, board, depth):
        self.socket.send("ucinewgame")
        self.socket.send(f"position fen {board}")
        self.socket.send(f"go depth {depth}")

        lines = []

        while True:
            response = self.socket.recv()

            if "bestmove" in response:
                break
            lines.append(response)

        self.socket.send("stop")
        result = process_response_lines(lines)
        return result

    def get_config(self):
        with open("uci_server_config.json") as config_file:
            data = json.load(config_file)
        return data
