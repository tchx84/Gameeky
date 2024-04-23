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

__command_template__ = (
    "pandoc --standalone --css=none --include-in-header=%s --output=%s %s"
)


def build_html(
    sources_path: str,
    header_path: str,
    destination_path: str,
    language: str,
):
    source_path = os.path.join(sources_path, language, "index.md")
    target_path = os.path.join(destination_path, language, "index.html")

    command = __command_template__ % (header_path, target_path, source_path)

    if (code := subprocess.call(command, shell=True)) != 0:
        sys.exit(code)


def list_languages(translations: str) -> list:
    languages = ["en"]

    for translation in os.listdir(translations):
        if translation.endswith(".po"):
            languages.append(translation.removesuffix(".po"))

    return languages


def main():
    parser = ArgumentParser()
    parser.add_argument("sources", help="path to the markdown files directory")
    parser.add_argument("header", help="path to the header file")
    parser.add_argument("translations", help="path to the PO directory")
    parser.add_argument("destination", help="path to the HTML files directory")
    parser.add_argument("--language", help="a target language code (e.g. 'es')")
    args = parser.parse_args()

    languages = [args.language] if args.language else list_languages(args.translations)

    for language in languages:
        build_html(args.sources, args.header, args.destination, language)


if __name__ == "__main__":
    main()
