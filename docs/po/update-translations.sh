#!/bin/sh

# Exit on error, fail when using unset variables
set -eu

# Enabled language codes
LANGS="es"

pot_creation_date=$(date +'%F %R%z')
version=$(grep '<release ' ../../data/dev.tchx84.Gameeky.metainfo.xml.in | cut -d\" -f4)

# Enter docs/po directory
cd $(dirname $0)

# Regenerate POT file
md2po ../basics/en/index.md \
  -d "Project-Id-Version: gameeky ${version}" \
  -d "Content-Type: text/plain; charset=UTF-8" \
  -d "POT-Creation-Date: ${pot_creation_date}" \
  --quiet --save --po-encoding UTF8 \
  --po-filepath gameeky.pot

# Update PO files, ignoring those failing in msgfmt
for pofile in *.po; do
  set +e
  msgfmt -vvc "$pofile" -o /dev/null || continue
  set -e
  msgmerge --previous --update --backup=none "$pofile" gameeky.pot
  sed -i "$pofile" \
    -e "s|Project-Id-Version: .*|Project-Id-Version: gameeky $version\\\\n\"|"
done

# Build translated docs
for lang in $LANGS; do
  mkdir -p "../basics/${lang}"
  po2md ../basics/en/index.md \
    --pofiles "${lang}.po" \
    --quiet --wrapwidth 0 \
    --save "../basics/${lang}/index.md"
done
