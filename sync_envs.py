#!/usr/bin/python3

import json
import os
import formatjson
import getopt
import sys
import config


def SyncFromEnvironment(argsList):
    if not os.path.exists("zoov-staging/versions.json") or not os.path.exists("zoov-preprod/versions.json"):
        print("run script from root folder, one of `zoov-staging/versions.json` or `zoov-preprod/versions.json` was not found")
        exit(1)
    try:
        args = getopt.getopt(argsList, "p", [
            "ignore-pr", "no-add", "ignore=", "source=", "dest="])
    except Exception as e:
        print(e)
        exit(1)

    ignore_pr = False
    add_new_service = True
    ignore = []
    source_env = "preprod"
    dest_env = "staging"
    for opt, arg in args[0]:
        if opt in ("-p", "--ignore-pr"):
            ignore_pr = True
        elif opt == "--ignore":
            ignore = arg.strip().lower().split(",")
        elif opt == "--source":
            source_env = arg.strip().lower()
            if source_env not in config.ENVS:
                print(f"Unknown environment: {source_env}")
                exit(1)
        elif opt == "--dest":
            dest_env = arg.strip().lower()
            if dest_env not in config.ENVS:
                print(f"Unknown environment: {dest_env}")
                exit(1)
        elif opt == "--no-add":
            add_new_service = False

    source_path = os.path.join(
        config.ENVS[source_env]['folder'], config.ENVS[source_env]['file'])
    source_file = open(source_path, "r")
    dest_path = os.path.join(
        config.ENVS[dest_env]['folder'], config.ENVS[dest_env]['file'])
    dest_file = open(dest_path, "r")

    source_data = json.loads(source_file.read())
    dest_data = json.loads(dest_file.read())

    for service in source_data:

        source_has_tags = isinstance(source_data[service], dict)
        dest_has_tags = isinstance(
            dest_data[service], dict) if service in dest_data else bool(config.ENVS[dest_env]['withTags'])

        source_version = str(source_data[service]['version']
                             if source_has_tags else source_data[service])
        dest_version = (str(dest_data[service]['version']
                            if dest_has_tags else dest_data[service])) if service in dest_data else None

        if ignore_pr and dest_version != None and dest_version.startswith("pr-"):
            continue
        if service in ignore:
            continue
        if dest_version == None and not add_new_service:
            continue

        if dest_has_tags:
            tag = source_version if source_version.startswith(
                'pr-') else 'staging'
            dest_data[service] = {"version": source_version, "tag": tag}

            if source_has_tags and "app" in source_data[service]:
                dest_data[service]["app"] = source_data[service]["app"]
        else:
            dest_data[service] = source_version

    open(dest_path, 'w').write(
        formatjson.VersionsJSONEncoder().encode(dest_data))
