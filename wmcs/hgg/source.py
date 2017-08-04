# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Wikimedia Foundation and contributors
# License: Apache-2.0
"""
Helper program intended to be used as a clustershell external node group
source for processing a hostgroup.yaml file.
"""
from __future__ import print_function

import argparse
import itertools
import sys
import yaml


def cmd_map(groups, args):
    print('\n'.join(sorted(groups[args.group])))


def cmd_all(groups, args):
    print('\n'.join(sorted(set(itertools.chain(*groups.values())))))


def cmd_list(groups, args):
    print('\n'.join(sorted(groups.keys())))


def cmd_reverse(groups, args):
    print('\n'.join(sorted([
        name for name, nodes in groups.items() if args.node in nodes])))


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=sys.modules[__name__].__doc__)
    parser.add_argument(
        '--hostgroups', required=True,
        help='path to a YAML file with hostgroup information.')

    subparser = parser.add_subparsers(
        title='subcommands', metavar='COMMAND', dest='cmd')
    subparser.required = True

    map_parser = subparser.add_parser(
        'map', help='resolve a group name into a node set.')
    map_parser.add_argument('group', metavar='GROUP', help='group name')
    map_parser.set_defaults(func=cmd_map)

    all_parser = subparser.add_parser('all', help='list all nodes')
    all_parser.set_defaults(func=cmd_all)

    list_parser = subparser.add_parser('list', help='list all hostgroups')
    list_parser.set_defaults(func=cmd_list)

    reverse_parser = subparser.add_parser(
        'reverse', help='find groups containing a give node')
    reverse_parser.add_argument('node', metavar='NODE', help='node name')
    reverse_parser.set_defaults(func=cmd_reverse)

    args = parser.parse_args()
    with open(args.hostgroups) as fh:
        args.func(yaml.safe_load(fh), args)


if __name__ == '__main__':
    main()
