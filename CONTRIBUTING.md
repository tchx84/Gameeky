# Contributing

Thanks for taking the time to contribute! Before getting started:

1. Please make sure to read this document carefully.
2. Discuss the changes you wish to make by creating a [new issue](https://github.com/tchx84/Gameeky/issues/new).

## Understanding the goal

Gameeky is a learning tool in the form of a game engine. It's not a game engine that's also useful as a learning tool. Therefore, its primary goal is to provide a better learning experience for programming, arts and other STEAM skills. It's not a goal to provide an efficient nor professional game development process. You can read more about this project rationale [here](https://blogs.gnome.org/tchx84/2023/12/15/gameeky-a-new-learning-tool-to-develop-steam-skills/).

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

## Adding new translations

To add a new translation simply run these commands on the terminal:

```sh
# Fedora requirements
$ sudo dnf install meson desktop-file-utils appstream python3-black python3-pyflakes python3-mypy python3-pytest python3-pytest-timeout python3-gobject gtk4-devel

$ cd Gameeky
$ echo "es" >> po/LINGUAS # e.g adding Spanish translation

$ meson setup _translate
$ cd _translate
$ ninja gameeky-pot
$ ninja gameeky-update-po

# Edit the newly created po/es.po
# Commit the changes and create a new Pull Request
```

## Testing your changes

This project comes with automated tests that you can run, even before you submit your changes. Simply run these commands on the terminal:

```sh
# Fedora requirements
$ sudo dnf install meson desktop-file-utils appstream python3-black python3-pyflakes python3-mypy python3-pytest python3-pytest-timeout python3-gobject gtk4-devel

$ cd Gameeky
$ meson setup _test --prefix $PWD/usr

$ cd _test
$ ninja install
$ meson test
```

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU General Public License](COPYING) for more details.
