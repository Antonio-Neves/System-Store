# **Python Installation Manager**

https://www.python.org/downloads/

```jsx
Usage:
    py <regular Python options>
                         Launch the default runtime with specified options. This
                         is the equivalent of the python command.
    py -V:<TAG>          Launch runtime identified by <TAG>, which should
                         include the company name if not PythonCore. Regular
                         Python options may follow this option.
    py -3<VERSION>       Equivalent to -V:PythonCore\3<VERSION>. The version
                         must begin with the digit 3, platform overrides are
                         permitted, and regular Python options may follow. py -3
                         is the equivalent of the python3 command.
    py exec <any of the above>
                         Equivalent to any of the above launch options, and the
                         requested runtime will be installed if needed.
    py help [<CMD>]      Show help for Python installation manager commands
    py install <TAG>     Download new Python runtimes, or pass --update to
                         update existing installs.
    py list [<FILTER>]   Show installed Python runtimes, optionally filtering by
                         <FILTER>.
    py uninstall <TAG>   Remove one or more runtimes from your machine. Pass
                         --purge to clean up all runtimes and cached files.

Find additional information at https://docs.python.org/dev/using/windows.

Global options: (options must follow the command)
    -v, --verbose    Increased output (log_level=20)
    -vv              Further increased output (log_level=10)
    -q, --quiet      Less output (log_level=30)
    -qq              Even less output (log_level=40)
    -y, --yes        Always accept confirmation prompts (confirm=false)
    -h, -?, --help   Show help for a specific command
    --config=<PATH>  Override configuration with JSON file
```

Alterar versão principal do Python

```jsx
$Env:PYTHON_MANAGER_DEFAULT="3.12"
```