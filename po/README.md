# How To Translate

## Requirements

```bash
$ sudo dnf install meson desktop-file-utils appstream python3-black python3-pyflakes python3-mypy python3-pytest python3-pytest-timeout python3-gobject gtk4-devel
```

## Steps

```bash
$ cd Gameeky
$ echo "es" >> po/LINGUAS # e.g adding Spanish translation

$ meson setup _translate
$ cd _translate
$ ninja gameeky-pot
$ ninja gameeky-update-po

# Edit the newly created po/es.po
# Commit the changes
```

> 📝 **Note:** Gameeky requires that both the user interface and the beginner's guide are translated. Please check [doc/README.md](../doc/README.md).
