from bottle import route, run, abort, template, request
from subprocess import Popen
import argparse
import json


known_signals = {}
signals = []
args = {}

@route("/")
def main():
    global signals
    return template( "remote.html", signals=signals )


@route("/health")
def health():
    return "ok"

@route("/signals/<signal_key>/signal", method="POST")
def handle_signal(signal_key):
    global known_signals
    if signal_key in known_signals:
        command = known_signals[signal_key]["command"]
        if isinstance(command, str):
            Popen( ["bash", "-c", command] )
        else:
            if "variable" in known_signals[signal_key]:
                key = known_signals[signal_key]["variable"]
                val = request.body.read().decode('utf8')
                cmd = [ val if s == key else s for s in command ]
                if( val ):
                    Popen( cmd )
            else:
                Popen( command )
    else:
        abort(404, "Not a known signal")


@route("/config/reload", method="POST")
def reload_config():
    global signals
    global known_signals
    with open(args.config) as conf_file:
        config = json.loads( conf_file.read() )

        signals = config["signals"]
        known_signals = { s["key"]: s for s in signals if "key" in s }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-p", "--port", type=int, default=8080, help="port the service will listen on for signals. default is 8080")
    parser.add_argument("-c", "--config", default="./conf.json", help="config json-file for the launchpad. default is ./conf.json")
    parser.add_argument("-d", "--debug", action="store_true")

    args = parser.parse_args()
    reload_config()

    run(host="0.0.0.0", port=args.port, debug=args.debug)
