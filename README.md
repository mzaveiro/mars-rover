# Mars Rover Navigation

## Quick start

You can control a rover by doing:

```
$ ./rover_control.py
```

By default the script will look for [cmds_exemple.txt](cmds_exemple.txt) file
which contains the input from the challenge.

You can decrease the logging level to check what the script is doing under the 
hood by using:

```
$ ./rover_control.py --log-level debug
```

Check `--help` for all possible arguments.


## Testing

You will need to install the test requirements on you virtualenv first.

```
$ pip install -r requirements-test.txt
```

Then run all tests normally

```
python -m pytest -v -s
```

## Design considerations

The app is made of 3 parts:

1. `rover_control`: script that interacts with the user.
2. `rover.control`: parses the cmds from string to something meaningful and
takes care of the command sequence.
3. `rover.rover`: encapsulates the rover's functionalities together with a few
other modules.

The idea is that you can have more than one rover at the same time if you want,
or swap `rover.control` to a web server and modify `rover_control` to send REST
requests.

The rover itself comprises `Rover` class that acts as an interface from the
controller to the `Navigation`. That in turn takes care of the rover's allowed
movements and stores its runtime information in `LocationStorage`.

You can check the modules docstrings for more information.
