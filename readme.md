# Git Sindria

Git extension client for gitlab.

## Requirements

- Python >= 3.8

## Install RedHat/Fedora/CentOS

- Download rpm package: [git-sindria](https://raw.githubusercontent.com/SindriaInc/git-sindria/master/rpms/git-sindria-1.0.0-1.x86_64.rpm)
- Install with package manager: `sudo dnf install git-sindria-1.0.0-1.x86_64.rpm`

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
- Setup gitlab url: `git config --global sindria.url <url>`
- Setup projects path: `git config --global sindria.path <path>`

## Usage

- Multi clone by top level group or username: `git sindria clone <group-or-username>`
- Clear local cached repos by top level group or username: `git sindria clear <group-or-username>`

## Coming soon

- Get info about repos, groups and subgroups with stats
- Get git url ssh/https for clone specific repo
- Create empty repo
- Create repo bootstrap framework
- Create repo bootstrap sindria template with CI/CD
- Gitlab admin

## License

This software is release open source under [GPLV2](LICENSE) license.
