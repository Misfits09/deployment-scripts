import sys

DOCS = {
    "repo":
    """
Retrives versions from the repository and puts the values in the target versions.json
Default environment is : preprod

Options:
    --env=envname1      : Change the targetted environment
    -n, --no-check      : Bypass the default check that backend-services is at master and up to date with origin
    -p, --ignore-pr     : Do not update versions beginning with "pr-"

    --ignore=service1,service2 : Do not update specified services
""",
    "env": """
Retrives versions from another environment and puts the values in the target versions.json
Default source environment is      : preprod
Default destination environment is : staging

Options:
    --source=envname1   : Change the source environment
    --dest=envname1     : Change the destination environment
    --no-add            : Does not add new services from source env into destination env
    -p, --ignore-pr     : Do not update versions beginning with "pr-"

    --ignore=service1,service2 : Do not update specified services
"""
}


def HelpCommand(args):
    if len(args) != 1 or args[0] not in DOCS:
        print("Usage: %s help <%s>" % (sys.argv[0], "|".join(DOCS)))
        exit(1)
    else:
        print(DOCS[args[0]])
