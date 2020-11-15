# Git Sindria

Git extension client for gitlab, bitbucket and github.

[![asciicast](https://asciinema.org/a/x3jXmG0PJffXqvR3TUDgxC6N5.svg)](https://asciinema.org/a/x3jXmG0PJffXqvR3TUDgxC6N5)

## Requirements

- Python >= 3.8

## Install RedHat/Fedora/CentOS

- Download rpm package: [git-sindria-1.0.0-1.noarch.rpm](https://raw.githubusercontent.com/SindriaInc/git-sindria/master/rpms/git-sindria-1.0.0-1.noarch.rpm)
- Install with package manager: `sudo dnf install git-sindria-1.0.0-1.noarch.rpm`

## Uninstall RedHat/Fedora/CentOS

- Uninstall with package manager: `sudo dnf remove git-sindria`

## Install from source

Make sure you have `make` package installed.

- Clone this repo: `git clone https://github.com/SindriaInc/git-sindria.git`
- Move into it: `cd git-sindria`
- Build package: `make`
- Install package: `sudo make install`
- Clean build cache: `make clean`

## Uninstall from source

- Uninstall package: `sudo make uninstall`

## Configuration

If you don't have a token goto under your gitlab profile and generate personal access token.

- Setup token: `git config --global sindria.token <token>`
- Setup projects path: `git config --global sindria.path <path>`

### Optional

- Setup provider: `git config --global sindria.provider <provider>`
- Setup url: `git config --global sindria.url <url>`

## Usage

- Multi clone by top level group or username: `git sindria clone <group-or-username>`
- Clear local cached repos by top level group or username: `git sindria clear <group-or-username>`
- Git log advanced: `git sindria log`

## Coming soon

- Get info about repos, groups and subgroups with stats
- Get git url ssh/https for clone specific repo
- Create empty repo
- Create repo bootstrap framework
- Create repo bootstrap sindria template with CI/CD
- Gitlab admin
- Export issues
- Setup mirror
- Setup webhook integration
- Other git provider support (Bitbucket, GitHub)

## License

This software is release open source under [GPLV2](LICENSE) license.
