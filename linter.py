#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Hardy Jones
# Copyright (c) 2013
#
# License: MIT
#

"""This module exports the Hlint plugin class."""

from SublimeLinter.lint import Linter
from os.path import basename


class Hlint(Linter):
    """Provides an interface to hlint."""

    cmd = 'hlint --cpp-include /home/falco.peijnenburg/engineering/lumi/hs-pkgs/lumi-hackage-extended/include/ --cpp-include /home/falco.peijnenburg/engineering/lumi/hs-pkgs/lumi-document-store-api/include/ --ignore "Redundant do" --ignore "Use camelCase" --ignore "Use ."'
    regex = (
        r'^(?P<filename>.+):(?P<line>\d+):'
        '(?P<col>\d+):\s*'
        '(?:(?P<error>Error)|(?P<warning>(Warning|Suggestion))):\s*'
        '(?P<message>.+)$'
    )
    multiline = True
    tempfile_suffix = {
        'haskell': 'hs',
        'haskell-sublimehaskell': 'hs',
        'literate haskell': 'lhs'
    }
    defaults = { "lint_mode": "load_save", 'selector': 'source.haskell' }

    def split_match(self, match):
        """Override to ignore errors reported in imported files."""
        match, line, col, error, warning, message, near = (
            super().split_match(match)
        )

        match_filepath = match.groupdict()['filename']
        match_filename = basename(match_filepath)
        linted_filename = basename(self.filename)

        if match_filename != linted_filename and not match_filepath.startswith("/tmp"):
            return None, None, None, None, None, '', None

        return match, line, col, error, warning, message, near
