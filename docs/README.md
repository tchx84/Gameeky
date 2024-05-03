# How To Translate

## Requirements

```bash
$ sudo dnf install pandoc
$ pip install --user mdpo
```

## Steps

```bash
$ cd Gameeky
$ python3 docs/tools/update_pot.py docs/basics/src/en/index.md docs/basics/po/gameeky.pot
$ python3 docs/tools/update_po.py docs/basics/po --language es
$ python3 docs/tools/update_md.py docs/basics/src/ docs/basics/po/ --language es
$ python3 docs/tools/update_html.py docs/basics/src/ docs/basics/data/headers.xml docs/basics/po docs/basics/html/ --language es
```

> 📝 **Note:** You can omit the `--language` argument to update all the available languages.
