#!/usr/bin/env python
'''Control a Mars Rover

Usage:
    ./rover_control.py
'''
import argparse
import logging
import logging.config
import logging.handlers
import pathlib
import sys

import rover.control as controller


def get_next_line(filename):
    '''Opens a file in read mode and yield all lines, one at a time.

    :param filename: The name of the file
    :type filename: str

    :yields: each line of the file
    '''
    with open(filename, "r") as cmd_file:
        yield from cmd_file


def process_from_file(filename):
    '''Process commands from a file'''
    file = pathlib.Path(filename)
    if not file.is_file():
        logger = logging.getLogger("process_from_file")
        logger.warning("File %s not found, please check the path", filename)
        return

    rover_control = controller.Control()
    for line in get_next_line(filename):
        rover_control.process(line.strip())


def main():
    '''Parse arguments and control rover'''
    argv = sys.argv[1:]
    parser = argparse.ArgumentParser(prog=__file__)
    logging_name_map = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warn': logging.WARN,
        'info': logging.INFO,
        'debug': logging.DEBUG,
    }
    logging_names = logging_name_map.keys()

    parser.set_defaults(
        log_level="warn",
        log_file="/tmp/rover.log",
        cmd_file="cmds_exemple.txt"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=sorted(logging_names),
        help=("Level to log at. "
              "One of: %(choices)s."
              "Default: %(default)s")
    )

    parser.add_argument(
        "--log-file",
        dest="log_file",
        metavar="FILE",
        help=("File to log to."
              "Default: %(default)s")
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="cmd_file",
        metavar="FILE",
        help=("File with commands to process"
              "Default: %(default)s")
    )
    options = parser.parse_args(argv)

    log_file = options.log_file

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_logs": False,
        "formatters": {
            "standard": {
                "format":
                "%(asctime)s [%(levelname)7.7s] - %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "terminal": {
                "format":
                "[%(levelname)7.7s] %(name)s: %(message)s",
            },
        },
        "handlers": {
            "stream": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "terminal"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": log_file,
                "level": "INFO",
                "formatter": "standard",
                "maxBytes": 10000000,
                "backupCount": 10,
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "": {
                "handlers": ["file", "stream"],
                "level": logging_name_map[options.log_level]
            }
        }

    })

    mainlog = logging.getLogger("rover_control")
    mainlog.info("start rover!")
    process_from_file(options.cmd_file)


if __name__ == "__main__":
    main()
