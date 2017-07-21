#!/usr/bin/env python3
"""
Simple script that generates hosts files usable with dsh/pssh
for running administrative actions on all hosts in a particular
labs project.

Hits the openstack-browser API.

You can execute commands via pssh like:

    pssh -t0 -p4 -h <hostgroup> '<command>'

This sets parallelism to 4, tweak as necessary.
"""
from urllib.request import urlopen
import argparse
import sys

OSB = 'https://tools.wmflabs.org/openstack-browser'

# Maps prefixes to hostgroup names
classifier = {
    'tools': {
        '': 'all',
        'tools-bastion-': 'bastion',
        'tools-checker-': 'checker',
        'tools-cron-': 'cron',
        'tools-docker-': 'docker',
        'tools-elastic-': 'elastic',
        'tools-exec-': 'exec-all',
        'tools-flannel-': 'flannel',
        'tools-k8s-': 'k8s',
        'tools-mail': 'mail',
        'tools-master': 'master',
        'tools-proxy-': 'proxy',
        'tools-redis-': 'redis',
        'tools-services-': 'services',
        'tools-static-': 'static',
        'tools-webgrid-': 'webgrid-all',
        'tools-webgrid-generic': 'webgrid-generic',
        'tools-webgrid-lighttpd-': 'webgrid-lighttpd-all',
        'tools-webgrid-lighttpd-14': 'webgrid-lighttpd-trusty',
        'tools-worker-': 'worker',
    },
}


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_list(url):
    body = urlopen(url).read().decode('utf-8').strip()
    if not body:
        return []
    return body.split('\n')


def main():
    parser = argparse.ArgumentParser(description='DSH hostfile generator')
    parser.add_argument(
        'project', metavar='PROJECT', nargs='*',
        help='Cloud VPS project')
    parser.add_argument(
        '--all', action='store_true',
        help='Generate files for all projects')
    args = parser.parse_args()

    if args.all:
        projects_url = '{}/api/projects.txt'.format(OSB)
        projects = get_list(projects_url)
    elif not args.project:
        parser.error('No project names provided and `--all` not used.')
    else:
        projects = args.project

    for project in projects:
        eprint('Fetching hosts for project {}'.format(project))
        api_url = '{}/api/dsh/project/{}'.format(OSB, project)
        hosts = get_list(api_url)

        if not hosts:
            eprint(' - No hosts in project {}'.format(project))
            continue

        if project in classifier:
            for prefix, group in classifier[project].items():
                with open('{}-{}'.format(project, group), 'w') as f:
                    f.write("\n".join([
                        host
                        for host in hosts
                        if host.startswith(prefix)
                    ]))
        else:
            with open(project, 'w') as f:
                f.write("\n".join(hosts))


main()
