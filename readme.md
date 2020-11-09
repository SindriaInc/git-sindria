# Git Sindria

Git extension client for gitlab.

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
