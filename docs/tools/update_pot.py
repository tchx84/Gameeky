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

import time

from argparse import ArgumentParser
from mdpo.md2po import markdown_to_pofile

__header_template__ = """# SOME DESCRIPTIVE TITLE.
# Copyright (C) %s Gameeky's COPYRIGHT HOLDER
# This file is distributed under the same license as the Gameeky package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
"""


def generate_template(source_path: str, destination_path: str) -> None:
    # Generate the contents
    pot = markdown_to_pofile(
        source_path,
        location=False,
        md_encoding="utf-8",
        po_encoding="utf-8",
        metadata={
            "Project-Id-Version": "gameeky",
            "Report-Msgid-Bugs-To": "https://github.com/tchx84/gameeky/issues",
            "POT-Creation-Date": time.strftime("%F %R%z", time.localtime()),
            "PO-Revision-Date": "YEAR-MO-DA HO:MI+ZONE",
            "Last-Translator": "FULL NAME <EMAIL@ADDRESS>",
            "Language-Team": "LANGUAGE <LL@li.org>",
            "Language": "",
            "MIME-Version": "1.0",
            "Content-Type": "text/plain; charset=UTF-8",
            "Content-Transfer-Encoding": "8bit",
            "Plural-Forms": "nplurals=INTEGER; plural=EXPRESSION;",
        },
    )

    # Prepare the headers
    header = __header_template__ % time.strftime("%Y")

    # Save it to disk
    with open(destination_path, "w") as file:
        file.write(header + str(pot))


def main():
    parser = ArgumentParser()
    parser.add_argument("source", help="path to the markdown source file")
    parser.add_argument("destination", help="path to the POT destination file")
    args = parser.parse_args()

    generate_template(args.source, args.destination)


if __name__ == "__main__":
    main()
