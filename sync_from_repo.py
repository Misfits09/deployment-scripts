#!/usr/bin/python3

import json
import os
import sys
import getopt
import serviceversion
import formatjson
import config


def SyncFromRepo(argsList):
    try:
        args = getopt.getopt(argsList, "n:p", [
            "ignore-pr", "no-check", "ignore=", "env="])
    except Exception as e:
        print(e)
        exit(1)

    ignore = []
    check_branch_at_master = True
    ignore_pr_versions = False
    dest_env = "preprod"

    for opt, arg in args[0]:
        if opt in ("-n", "--no-check"):
            check_branch_at_master = False
        elif opt == "--ignore" and arg != '':
            ignore = arg.strip().lower().split(",")
        elif opt in ("-p", "--ignore-pr"):
            ignore_pr_versions = True
        elif opt == "--env":
            requested_env = arg.lower().strip()
            if requested_env in config.ENVS:
                dest_env = arg.lower().strip()
            else:
                print("Provided env \"%s\ does not exist" % requested_env)
                exit(1)

    dest_path = os.path.join(
        os.path.join(config.ENVS[dest_env]['folder'], config.ENVS[dest_env]['file']))

    if not os.path.exists(dest_path):
        print("run script from root folder, `%s` was not found" % dest_path)
        exit(1)

    if check_branch_at_master and not serviceversion.checkIsMaster():
        exit(1)

    dest_file = open(dest_path, 'r')
    dest_data = json.loads(dest_file.read())

    dest_has_tags = bool(config.ENVS[dest_env]['withTags'])

    for service in dest_data:
        dest_version = (str(dest_data[service]['version']
                            if dest_has_tags else dest_data[service])) if service in dest_data else None

        if ignore_pr_versions and dest_version != None and dest_version.startswith('pr-'):
            continue

        repo_version = serviceversion.serviceVersion(service)
        if repo_version == None:
            continue

        if dest_has_tags:
            app = dest_data[service]["app"] if "app" in dest_data[service] else None
            dest_data[service] = {
                "version": repo_version,
                "tag": repo_version if repo_version.startswith('pr-') else "staging",
            }
            if app != None:
                dest_data[service]["app"] = app
        else:
            dest_data[service] = repo_version

    open(dest_path, 'w').write(
        formatjson.VersionsJSONEncoder().encode(dest_data))
