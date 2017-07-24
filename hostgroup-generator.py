#!/usr/bin/env python3
"""
Generate hostgroups for Wikimedia Cloud VPS projects.

Generates lists of hosts suitable for use with either dsh/pssh or clush for
Cloud VPS projects using data collected from the openstack-browser API.
"""
from urllib.request import urlopen
import argparse
import contextlib
import os
import sys
import yaml

OSB = 'https://tools.wmflabs.org/openstack-browser'


def eprint(*args, **kwargs):
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def get_list(url):
    body = urlopen(url).read().decode('utf-8').strip()
    if not body:
        return []
    return body.split('\n')


@contextlib.contextmanager
def _open(fname=None):
    """Based on https://stackoverflow.com/a/17603000/8171"""
    if fname and fname != '-':
        fh = open(fname, 'w')
    else:
        fh = sys.stdout
    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()


def _outfile(base, fname):
    if base == '-':
        return base
    if os.path.isfile(base):
        return base
    return os.path.join(base, fname)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=sys.modules[__name__].__doc__)
    parser.add_argument(
        '--all', action='store_true',
        help='generate hostgroups for all projects')
    parser.add_argument(
        '--classifiers', metavar='YAML',
        default=os.path.join(
            os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')),
            'clustershell',
            'classifiers.yaml'),
        help='YAML file of patterns to partition hostgroups for a project')
    parser.add_argument(
        '--output', metavar='FILE',
        default=os.getcwd(),
        help='directory or file to output results to')
    parser.add_argument(
        '--clush', action='store_true',
        help='generate clush hostgroup mapping file instead of dsh files')
    parser.add_argument(
        'project', metavar='PROJECT', nargs='*',
        help='Cloud VPS project name')
    args = parser.parse_args()

    if args.all:
        projects_url = '{}/api/projects.txt'.format(OSB)
        projects = get_list(projects_url)
    elif not args.project:
        parser.error('No project names provided and `--all` not used.')
    else:
        projects = args.project

    # Validate output file/directory
    if args.output == '-':
        outpath = '-'
    else:
        outpath = os.path.abspath(args.output)
        if len(projects) > 1 and not os.path.isdir(outpath):
            parser.error(
                'Output location is not a directory and multiple'
                'projects are selected')

    try:
        with open(args.classifiers, 'r') as f:
            classifiers = yaml.safe_load(f.read())
    except IOError as e:
        classifiers = {}

    hostgroups = {}

    for project in projects:
        eprint('Fetching hosts for project {}'.format(project))
        api_url = '{}/api/dsh/project/{}'.format(OSB, project)
        hosts = get_list(api_url)

        if not hosts:
            eprint(' - No hosts in project {}'.format(project))
            continue

        if project in classifiers:
            for prefix, group in classifiers[project].items():
                key = '{}-{}'.format(project, group)
                hostgroups[key] = [
                    host
                    for host in hosts
                    if host.startswith(prefix)
                ]
        else:
            hostgroups[project] = hosts

    if args.clush:
        with _open(_outfile(args.output, 'hostgroups.yaml')) as f:
            f.write(yaml.safe_dump(hostgroups, default_flow_style=False))
    else:
        for name, data in hostgroups.items():
            with _open(_outfile(args.output, name)) as f:
                f.write("\n".join(data))


main()
