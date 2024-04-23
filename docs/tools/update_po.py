#!/usr/bin/env python3

# Copyright (c) 2024 Rafael Fontenelle.
# Copyright (c) 2024 Martin Abente Lahaye.
#
# This file is part of Gameeky
# (see gameeky.tchx84.dev).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import subprocess

from argparse import ArgumentParser

__command_template__ = "msgmerge --previous --update --backup=none %s %s"


def msgmerge(translations: str, language: str):
    source = os.path.join(translations, "gameeky.pot")
    file = os.path.join(translations, f"{language}.po")

    command = __command_template__ % (file, source)

    if (code := subprocess.call(command, shell=True)) != 0:
        sys.exit(code)


def list_languages(translations: str) -> list:
    languages = []

    for translation in os.listdir(translations):
        if translation.endswith(".po"):
            languages.append(translation.removesuffix(".po"))

    return languages


def main():
    parser = ArgumentParser()
    parser.add_argument("translations", help="path to the PO directory")
    parser.add_argument("--language", help="a language code (e.g. 'es')")
    args = parser.parse_args()

    languages = [args.language] if args.language else list_languages(args.translations)

    for language in languages:
        msgmerge(args.translations, language)


if __name__ == "__main__":
    main()
