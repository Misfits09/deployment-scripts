import os
import re

backendServicesFolder = os.path.join("..", "backend-services")

if not os.path.exists(backendServicesFolder):
    print("run script from root folder, `../backend-services` was not found")
    exit(1)


def checkIsMaster():
    dir = os.getcwd()
    try:
        os.chdir(backendServicesFolder)
        branch = os.popen("git branch --show-current").readline().strip()
        if branch != "master":
            print("Backend Services is not at master, quitting...")
            print(branch)
            return False

        status = os.popen("git status -b -s").readline().strip()
        if status != "## master...origin/master":
            print("Backend Services is not in sync with origin, quitting...")
            print(status)
            return False

        return True
    finally:
        os.chdir(dir)


def serviceVersion(name):
    servicePath = os.path.join(backendServicesFolder, name)
    if not os.path.exists(servicePath):
        print("Warning: Service", name, "not found in repository, ignoring...")
        return None

    changelogPath = os.path.join(servicePath, "CHANGELOG.md")
    if not os.path.exists(servicePath):
        print("Warning: Service", name,
              "found, but with no changelog, ignoring...")
        return None

    with open(changelogPath) as f:
        lastVersionString = f.readline()
        match = re.match(
            "##?\s*(\d{1,2}\.\d{1,2}\.\d{1,2}).*", lastVersionString)
        if match == None:
            print("Warning: Service", name,
                  "found, but invalid last changelog line, ignoring...")
            return None
        return match.group(1)
