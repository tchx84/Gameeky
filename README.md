<img style="vertical-align: middle;" src="data/icons/hicolor/scalable/apps/dev.tchx84.Gameeky.svg" width="128" height="128" align="left">

# Gameeky ![CI](https://github.com/tchx84/Gameeky/workflows/CI/badge.svg)

Play, create and learn.

![](data/screenshots/en/01.png)

Gameeky is a learning tool designed for young learners and educators to create and explore rich interactive games and experiences.

* Play and explore games with your friends
* Create new games without writing any code
* Nurture the artist in you by designing game objects for your games
* Grasp the basics of programming using Python in a LOGO-like experience
* Mature your programming skills by extending your game with Python plugins

## Usage

A thorough tutorial will be available soon.

## Build it yourself

```
git clone https://github.com/tchx84/Gameeky.git
cd Gameeky
flatpak --user install org.gnome.{Platform,Sdk}//45
flatpak-builder --user --force-clean --install build dev.tchx84.Gameeky.json
flatpak --user run --branch=master dev.tchx84.Gameeky
```

Or just use [Builder](https://flathub.org/apps/details/org.gnome.Builder)

## Code of conduct

Gameeky follows the [GNOME Code of Conduct](https://conduct.gnome.org/).

- **Be friendly.** Use welcoming and inclusive language.
- **Be empathetic.** Be respectful of differing viewpoints and experiences.
- **Be respectful.** When we disagree, we do so in a polite and constructive manner.
- **Be considerate.** Remember that decisions are often a difficult choice between competing priorities.
- **Be patient and generous.** If someone asks for help it is because they need it.
- **Try to be concise.** Read the discussion before commenting.

## Disclaimer

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU General Public License](COPYING) for more details.
