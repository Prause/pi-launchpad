# pi-launchpad
Very basic browser "remote control" to launch commands on your raspberry (or any other system, really).

## depencencies

The server uses the bottlepy framework, please download the self-contained python file at http://bottlepy.org/ and place it in the `server.py`'s directory or PIP-install it.
(Tested with Bottle 0.12)

## config

The config resides in a `conf.json` file (which can be pointed to on server start with the `--config` flag).
Each entry in the config's `signals` array needs
- a `key` (unique key)
- `name` (displayed on the remote html page)
- and the `command` to be executed

The command can be
- either an array of the command to be executed + it's parameters (see e.g. `power` in `example_conf.json`)
- or a string, which would be passed to `bash -c <command-string>`. (see e.g. `vol_up` in `example_conf.json`)

## running the server

```
python3 server.py --port 8080
```
The server will then listen on port 8080 publicly.

You can reload the config with
```
curl -X POST localhost:8080/config/reload
```

## license
MIT
