# -*- coding: utf-8 -*-
"""Strip a string."""

import traceback

from tcex import TcEx


def parse_arguments():
    """Parse arguments coming into the app."""
    tcex.parser.add_argument('--string', help='String', required=False)
    return tcex.args


def main():
    """Strip a string."""
    args = parse_arguments()

    # read the string from the playbook to get the actual value of the argument
    string = tcex.playbook.read(args.string)
    tcex.log.info(f'String value: {string}')
    tcex.playbook.create_output('strippedString', string.strip())
    tcex.message_tc(f'Stripped string: {string.strip()}')

    tcex.exit(0)


if __name__ == "__main__":
    tcex = TcEx()
    try:
        # start the app
        main()
    except SystemExit:
        pass
    except Exception as e:  # if there are any strange errors, log it to the logging in the UI
        err = f'Generic Error.  See logs for more details ({e}).'
        tcex.log.error(traceback.format_exc())
        tcex.message_tc(err)
        tcex.playbook.exit(1)
