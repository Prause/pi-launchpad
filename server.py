from bottle import route, run, abort, template
from subprocess import Popen
import argparse
import json


known_signals = {}
signals = []
args = {}

@route("/")
def main():
    return template( "remote.html", signals=signals )


@route("/signals/<signal_key>/signal", method="POST")
def handle_signal(signal_key):
    if signal_key in known_signals:
        command = known_signals[signal_key]["command"]
        if isinstance(command, str):
            Popen( ["bash", "-c", command] )
        else:
            Popen( command )
    else:
        abort(404, "Not a known signal")


@route("/config/reload", method="POST")
def reload_config():
    with open(args.config) as conf_file:
        config = json.loads( conf_file.read() )

        signals = config["signals"]
        known_signals = { s["key"]: s for s in signals }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-p", "--port", type=int, default=8080, help="port the service will listen on for signals. default is 8080")
    parser.add_argument("-c", "--config", default="./conf.json", help="config json-file for the launchpad. default is ./conf.json")

    args = parser.parse_args()
    with open(args.config) as conf_file:
        config = json.loads( conf_file.read() )

        signals = config["signals"]
        known_signals = { s["key"]: s for s in signals }

    run(host="0.0.0.0", port=args.port)
