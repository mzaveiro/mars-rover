#!/usr/bin/env python
'''Control a Mars Rover

Usage:
    ./rover_control.py
'''
import argparse
import logging
import logging.config
import logging.handlers
import sys

import rover.rover as mars_rover


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
        log_level="info",
        log_file="/tmp/rover.log",
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
        choices=sorted(logging_names),
        help=("File to log to."
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
                "%(asctime)s [%(levelname)5.5s] - %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
        },
        "handlers": {
            "stream": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "standard"
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

    mainlog = logging.getLogger("")
    mainlog.info("start rover!")

    rover = mars_rover.Rover()
    rover.set_boundaries(5, 5)

    rover.set_inital_position(1, 2, 'N')
    rover.navigate('LMLMLMLMM')

    rover.set_inital_position(3, 3, 'E')
    rover.navigate('MMRMMRMRRM')


if __name__ == "__main__":
    main()
