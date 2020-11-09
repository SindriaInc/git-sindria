# Git Sindria

Git extension client for gitlab.

## Requirements

- Python >= 3.8

## Install from source

Make sure you have `make` package installed.

- Clone this repo: `git clone https://github.com/SindriaInc/git-sindria.git`
- Build package: `make`
- Install package: `sudo make install`
- Clean build cache: `make clean`

## Uninstall from source

- Uninstall package: `sudo make uninstall`

## Configuration

If you don't have a token goto under your gitlab profile and generate personal access token.

- Setup token: `git config --global sindria.token <token>`
- Setup gitlab url: `git config --global sindria.url <url>`
- Setup projects path: `git config --global sindria.path <path>`

## Usage

- Multi clone by top level group: `git sindria clone <group>`

## Coming soon

- Destroy local repo cached by group
- Get info about repos, groups and subgroups with stats
- Get git url ssh/https for clone specific repo
- Create empty repo
- Create repo bootstrap framework
- Create repo bootstrap sindria template with CI/CD