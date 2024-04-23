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

from argparse import ArgumentParser
from mdpo.po2md import pofile_to_markdown


def build_markdown(sources_path: str, translations_path: str, language: str):
    source_path = os.path.join(sources_path, "en", "index.md")
    target_directory_path = os.path.join(sources_path, language)
    target_path = os.path.join(target_directory_path, "index.md")
    translation_path = os.path.join(translations_path, f"{language}.po")

    # Ensure language directory exists
    os.makedirs(target_directory_path, exist_ok=True)

    pofile_to_markdown(
        source_path,
        translation_path,
        save=target_path,
        md_encoding="utf-8",
        po_encoding="utf-8",
        wrapwidth=0,
    )


def list_languages(translations: str) -> list:
    languages = []

    for translation in os.listdir(translations):
        if translation.endswith(".po"):
            languages.append(translation.removesuffix(".po"))

    return languages


def main():
    parser = ArgumentParser()
    parser.add_argument("sources", help="path to the markdown files directory")
    parser.add_argument("translations", help="path to the PO directory")
    parser.add_argument("--language", help="a target language code (e.g. 'es')")
    args = parser.parse_args()

    languages = [args.language] if args.language else list_languages(args.translations)

    for language in languages:
        build_markdown(args.sources, args.translations, language)


if __name__ == "__main__":
    main()
