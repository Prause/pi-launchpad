# pi-launchpad
Very basic browser "remote control" to launch commands on your raspberry (or any other system, really).

## depencencies

The server uses the bottlepy framework, please download the self-contained python file at http://bottlepy.org/ and place it in the `server.py`'s directory or PIP-install it.
(Tested with Bottle 0.12)

For the lazy:
wget https://github.com/bottlepy/bottle/raw/master/bottle.py

## config

The config resides in a `conf.json` file (which can be pointed to on server start with the `--config` flag).
Each entry in the config's `signals` array needs
- a `key` (unique key)
- `name` (displayed on the remote html page)
- and the `command` to be executed
- optionally: a `variable` name for substitution

The command can be
- either an array of the command to be executed + it's parameters (see e.g. `power` in `example_conf.json`)
- or a string, which would be passed to `bash -c <command-string>`. (see e.g. `vol_up` in `example_conf.json`)

Input variables:
Disclaimer: Be warned that this allows anyone with access to the remote's UI to execute malicious code on your Pi.
For array commands you can add a `variable` to the config. For those commands, any occurrence in the `command` array is substituted by an input value provided by the user.
E.g. in `{ "command": [ "echo", "FOO", "FOO BAR" ], "variable": "FOO" }` the first "FOO" will be substituted, the second in "FOO BAR" won't.
The command will not be executed, if no input is provided.

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
