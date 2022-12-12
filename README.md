# Scripts for `backend-deployments`

## Installation

While at the root of the `backend-deployments` repository (which must be in the same parent folder as `backend-services`), clone this repository.

**All commands must be run from backend-deployments' root directory**

## Usage examples

### Put an environment iso master

Retrives versions from the repository and puts the values in the target versions.json
Default environment is : preprod

```bash
deployment-scripts/sync repo --env=preprod -p
```

**Options:**

- --env=envname1      : Change the targetted environment
- -n, --no-check      : Bypass the default check that backend-services is at master and up to - date with origin
- -p, --ignore-pr     : Do not update versions beginning with "pr-"
- --ignore=service1,service2 : Do not update specified services

### Sync an environmen with another

Retrives versions from another environment and puts the values in the target versions.json

- Default source environment is : preprod
- Default destination environment is : staging

```bash
deployment-scripts/sync env --source=preprod --dest=staging -p
```

**Options:**

- `--source=envname1`   : Change the source environment
- `--dest=envname1`     : Change the destination environment
- `--no-add`            : Does not add new services from source env into destination env
- `-p, --ignore-pr`     : Do not update versions beginning with "pr-"
- `--ignore=service1,service2` : Do not update specified services
