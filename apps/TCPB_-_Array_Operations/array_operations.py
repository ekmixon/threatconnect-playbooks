# -*- coding: utf-8 -*-
""" Array Operations Playbook App """
import traceback
import sys

from tcex import TcEx

# Python 2 unicode
if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

tcex = TcEx()

# App args
tcex.parser.add_argument('--array', required=True)
tcex.parser.add_argument('--operation', required=True)
args = tcex.args


def main():
    """Main App Logic"""
    array = tcex.playbook.read(args.array)
    operation = tcex.playbook.read(args.operation)

    # check for valid inputs
    if array is None:
        err = 'Array must not be null.'
        tcex.log.error(err)
        tcex.message_tc(err)
        tcex.exit(1)

    # log values
    tcex.log.debug(f'String Array: {array}')
    tcex.log.info(f'Operation: {operation}')

    results = None
    if operation == 'Sort':
        results = sorted(array)
    elif operation == 'Reverse Sort':
        results = sorted(array, reverse=True)
    elif operation == 'Sort Lowercase':
        results = sorted(array, key=str.lower)
    elif operation == 'Lowercase':
        results = [x.lower() for x in array]
    elif operation == 'Titlecase':
        results = [x.title() for x in array]
    elif operation == 'Uppercase':
        results = [x.upper() for x in array]
    elif operation == 'Duplicates':
        results = list({x for x in array if array.count(x) > 1})
    elif operation == 'Unique':
        results = list(set(array))
    # use array splice
    # elif operation == 'Pop':
    #     array.pop()
    #     results = array

    # create output
    tcex.log.debug(f'Results: {results}')
    if results is not None:
        tcex.playbook.create_output('array.count', len(results))
        tcex.playbook.create_output('array.results', results)

    tcex.message_tc(f'{operation} operation successfully applied on array.')
    tcex.exit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        main_err = f'Generic Error.  See logs for more details ({e}).'
        tcex.log.error(traceback.format_exc())
        tcex.message_tc(main_err)
        tcex.playbook.exit(1)
