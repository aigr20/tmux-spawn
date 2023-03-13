# tmux-spawn

A utility script for creating tmux windows and panes from a configuration file.

## Install

```console
git clone https://github.com/aigr20/tmux-spawn.git
cd tmux-spawn
pip install --user -r requirements.txt
chmod +x tmux-spawn.py
```

## Running

### Config file

By default the script searches for the configuration file in the following locations:

-   `$XDG_CONFIG_HOME/tmux-spawn/spawn-config.json`
-   `$HOME/.config/tmux-spawn/spawn-config.json`

The location can also be provided by using the -c or --config flags.

#### Configuration file

The configuration file can look as follows:

```json5
{
    // The name that identifies the windows to spawn
    "session_name": [
        {
            "name": "window name", // Optional name to set for the window
            // A list of panes, minimum 1
            "panes": [
                {
                    "path": "/a/directory", // Where to open the pane
                    "split_direction": "vertical", // Split vertically or horizontally
                    "program": // Optional program to run in the pane after opening
                }
            ]
        }
    ]
}
```

### Spawning a session

To open the session from the example config:

```console
tmux-spawn.py session_name
```

To open a session from a configuration file in a non-default location:

```console
tmux-spawn.py --config /path/to/config.json session_name
```
