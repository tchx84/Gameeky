# Contributing

Thanks for taking the time to contribute! Before getting started:

1. Please make sure to read this document carefully.
2. Discuss the changes you wish to make by creating a [new issue](https://github.com/tchx84/Gameeky/issues/new).

## Understanding the goal

Gameeky is a learning tool in the shape of a game engine. It's not a professional game engine. Therefore, its primary goal is to provide a better learning experience for programming, arts and other STEAM skills. It's not a goal to provide an efficient nor professional game development process. You can read more about this project rationale [here](https://blogs.gnome.org/tchx84/2023/12/15/gameeky-a-new-learning-tool-to-develop-steam-skills/).

If you're looking for a tool to create professional video games, I highly recommend the [Godot](https://godotengine.org/) game engine.

## Ways of contributing

There are plenty of ways to contribute to this project. To mention a few:

* **Code** refactors and bug fixes.
* **Design** improved tools for a better experience.
* **Translate** this project to your language.
* **Create** new thematic packs to allow more diverse types of games.
* **Write** tutorials and guides to help educators and learners to take advantage of this project.

If you like the project, but just don't have time to contribute, there are other ways to support it:

* **Share** this project on social media.
* **Refer** this project to educators.
* **Use** this project in your classroom.

## Code of conduct

This project follows the [GNOME Code of Conduct](https://conduct.gnome.org/). Please, follow it in all your interactions. In a nutshell:

- **Be friendly.** Use welcoming and inclusive language.
- **Be empathetic.** Be respectful of differing viewpoints and experiences.
- **Be respectful.** When we disagree, we do so in a polite and constructive manner.
- **Be considerate.** Remember that decisions are often a difficult choice between competing priorities.
- **Be patient and generous.** If someone asks for help it is because they need it.
- **Try to be concise.** Read the discussion before commenting.

## Getting started

The following is the recommended way for getting started:

1. [Fork](https://github.com/tchx84/Gameeky/fork) the project.
2. Install [GNOME Builder from Flathub](https://flathub.org/apps/details/org.gnome.Builder)
3. Open Builder and select "Clone Repository..."
4. Clone `https://github.com/YOUR_USERNAME/Gameeky.git`
5. Press the Run ▶ button

## Making changes

The process is well explained in this [article](https://opensource.com/article/19/7/create-pull-request-github), so you can simply follow these instructions to create pull requests.

The only request is that you [organize](https://github.blog/2022-06-30-write-better-commits-build-better-projects/) your commits in a way that makes sense. Please, do not send a single commit with too many changes.

Additionally, you can add your name to [the list of contributors](./src/gameeky/common/widgets/about_window.ui) in a separate commit.

## Changing the user interface

All the user interfaces were built with [Cambalache](https://flathub.org/apps/ar.xjuan.Cambalache). Therefore, it's the recommended tool for manipulating the *UI* files of this project.

## Adding new translations

Gameeky requires that both the user interface and the beginner's guide are translated. To translate the user interface to a new language, run these commands on the terminal:

```bash
# Fedora requirements
$ sudo dnf install meson desktop-file-utils appstream python3-black python3-pyflakes python3-mypy python3-pytest python3-pytest-timeout python3-gobject gtk4-devel

$ cd Gameeky
$ echo "es" >> po/LINGUAS # e.g adding Spanish translation

$ meson setup _translate
$ cd _translate
$ ninja gameeky-pot
$ ninja gameeky-update-po

# Edit the newly created po/es.po
# Commit the changes
```

To translate the beginner's guide, follow these steps:

```bash
$ cd Gameeky

$ mkdir docs/basics/es
$ touch docs/basics/es/index.md

# Edit the newly created index.md file and write a translated version of docs/basics/en/index.md
# Add the language code to docs/meson.build
# Commit the changes and create a Pull Request
```

## Testing your changes

This project comes with automated tests that you can run, even before you submit your changes. Simply run these commands on the terminal:

```bash
# Fedora requirements
$ sudo dnf install meson desktop-file-utils appstream python3-black python3-pyflakes python3-mypy python3-pytest python3-pytest-timeout python3-gobject gtk4-devel

$ cd Gameeky
$ meson setup _test --prefix $PWD/usr

$ cd _test
$ ninja install
$ meson test
```

## Windows support (experimental)

To run on windows, install [msys2](msys2.org) and follow the instructions to set up a development environment. Once the configuration is done, follow the instructions:

### Install the dependencies

```bash
$ pacman -Suy
$ pacman -S git mingw-w64-ucrt-x86_64-meson mingw-w64-ucrt-x86_64-gtk4 mingw-w64-ucrt-x86_64-python3 mingw-w64-ucrt-x86_64-python3-gobject mingw-w64-ucrt-x86_64-libadwaita mingw-w64-ucrt-x86_64-gstreamer mingw-w64-ucrt-x86_64-gst-plugins-good mingw-w64-ucrt-x86_64-gtksourceview5 mingw-w64-ucrt-x86_64-librsvg mingw-w64-ucrt-x86_64-desktop-file-utils unzip meson cmake
```

### Install pandoc

Now we download pandoc and copy it to `/usr/bin` by entering the msys2 terminal and typing the following commands
```bash
$ cd /tmp # Go to temporary directory
$ wget https://github.com/jgm/pandoc/releases/download/3.1.13/pandoc-3.1.13-windows-x86_64.zip # Download pandoc zip
$ unzip pandoc-3.1.13-windows-x86_64.zip # Unzip it
$ cp pandoc-3.1.13/pandoc.exe /usr/bin # Copy it
```

### Copy gettext files

Lastly, make sure to copy gettext ITS files from `/ucrt64/share/gettext/its` to `/usr/share/gettext/its`.
```bash
$ mkdir -p /usr/share/gettext/its # Create the directory if it does not exist
$ cp /ucrt64/share/gettext/its/* /usr/share/gettext/its -rf # and copy the files
```
#### Note: in windows you have to disable the webkit by using `meson setup build -Dwebkit=disabled`


## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU General Public License](COPYING) for more details.
