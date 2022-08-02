# -*- coding: utf-8 -*-
"""Return a deduplicated list.."""

import traceback

from tcex import TcEx


def parse_arguments():
    """Parse arguments coming into the app."""
    # retrieve the string as an argument
    tcex.parser.add_argument('--incoming_list', help='Incoming list', required=True)
    return tcex.args


def main():
    """."""
    # handle the incoming arguments
    args = parse_arguments()
    # read the string from the playbook to get the actual value of the argument
    incoming_list = tcex.playbook.read(args.incoming_list)
    # log the string
    tcex.log.info(f'Incoming list (before deduplication): {incoming_list}')

    deduplicated_list = list(set(incoming_list))
    tcex.log.info(f'Deduplicated list: {deduplicated_list}')
    # output the reversed string to downstream playbook apps
    tcex.playbook.create_output('deduplicatedList', deduplicated_list)

    # exit
    tcex.exit(0)


if __name__ == "__main__":
    # initialize a TcEx instance
    tcex = TcEx()
    try:
        # start the app
        main()
    except SystemExit:
        pass
    except:  # if there are any strange errors, log it to the logging in the UI
        err = 'Generic Error. See logs for more details.'
        tcex.log.error(traceback.format_exc())
        tcex.message_tc(err)
        tcex.playbook.exit(1)
