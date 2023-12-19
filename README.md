# Gameeky ![CI](https://github.com/tchx84/Gameeky/workflows/CI/badge.svg)

<img height="100" src="https://github.com/tchx84/Gameeky/blob/main/data/icons/hicolor/scalable/apps/dev.tchx84.Gameeky.svg"/>

Gameeky is a learning tool designed for young learners and educators to create and explore rich interactive worlds and experiences.

## Usage

A thorough documentation and tutorial page will be available soon.

## Build it yourself

```
git clone https://github.com/tchx84/Gameeky.git
cd Gameeky
flatpak --user install org.gnome.{Platform,Sdk}//45
flatpak-builder --user --force-clean --install build dev.tchx84.Gameeky.json
flatpak --user run --branch=master dev.tchx84.Gameeky
```

Or just use [Builder](https://flathub.org/apps/details/org.gnome.Builder)
