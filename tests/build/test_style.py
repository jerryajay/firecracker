"""
Tests ensuring codebase style compliance.

# TODO

- Add checks for non-rust code in the codebase.
"""

from subprocess import run

import pytest


SUCCESS_CODE = 0


def install_rustfmt_if_needed():
    """ Installs rustfmt if it's not available yet. """
    rustfmt_check = run(
        'rustup component list | grep --silent "rustfmt.*(installed)"',
        shell=True
    )

    if not rustfmt_check.returncode == SUCCESS_CODE:
        # rustfmt-preview is used with the current state of things.
        # See github.com/rust-lang-nursery/rustfmt for information.
        run(
            'rustup component add rustfmt-preview'
            '    >/dev/null 2>&1',
            shell=True,
            check=True
        )


@pytest.mark.timeout(120)
def test_style():
    """ Fails if there's misbehaving Rust style in this repo. """
    install_rustfmt_if_needed()

    run('cargo fmt --all -- --write-mode=diff', shell=True, check=True)
    """ Exits with an error if the style is bad. """