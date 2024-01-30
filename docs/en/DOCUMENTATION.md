# Welcome to Gameeky documentation

## Topics

1. Understanding its goal
2. Installing it
3. Thematic packs
4. Interface basics
5. Cooperative game play
6. Editing scenes
7. Editing entities
8. LOGO-like coding
9. Extending entities and game play with plugins

## Understanding its goal

[Gameeky](https://github.com/tchx84/gameeky) lets young learners and educators create and explore cooperative games and learning experiences.

More specifically:

* Play and explore games with friends
* Create new games without writing any code
* Tell stories through these games
* Nurture artistic skills by designing game objects and creatures
* Grasp the basics of programming using Python in a LOGO-like experience
* Mature programming skills by extending games with Python plugins

Note that this is a learning tool in the form of a game engine. It's not a game engine that's also useful as a learning tool. If you're looking for a tool to create professional video games, please consider the [Godot](https://godotengine.org) game engine.

## Installing it

The recommended installation method is through your system's software center, e.g. *GNOME Software*. Simply search for *Gameeky* and install it.

Alternatively, it can also be installed through [Flathub](https://flathub.org). Similarly, just search for *Gameeky* and follow the website's intructions.

Lastly, it can also be installed via terminal:

```bash
flatpak --user install flathub dev.tchx84.Gameeky
```


## Thematic packs

Gameeky provides prefabricated packs of games and building blocks for different thematic interests, e.g. a farming role [game](https://github.com/tchx84/FreedomValley) in a medieval fantasy setting.

The recommended installation method is through your system's software center, e.g. *GNOME Software*. Thematic packs are offered as addons at the Gameeky page. Simply select and install the thematic packs.

Alternatively, it can also be installed through [Flathub](https://flathub.org). Similarly, thematic packs are offered as addons at the Gameeky page. Simply select and install the thematic packs.

Lastly, it can also be installed via terminal:

```bash
flatpak --user remote-ls flathub | grep dev.tchx84.Gameeky.ThematicPack
flatpak --user install flathub dev.tchx84.Gameeky.ThematicPack.FreedomValley
```

## Interface basics

Gameeky is comprised of four components: The Launcher, the Player, the Scene Editor and the Entity Editor.

![The **Launcher** is the main interface where all Thematic Packs and projects can be found and launched. It's also the gateway to the other three components.](../../data/screenshots/en/04.png)

![The **Player** interface is where game sessions can be created, played and joined by others.](../../data/screenshots/en/02.png)

![The **Scene Editor** interface is where scenes can be created and modified.](../../data/screenshots/en/01.png)

![The **Entity Editor** interface is where entities can be created and modified.](../../data/screenshots/en/03.png)

##  Cooperative game play

Creating a new game session is easy as clicking on the *Play* button on the project's card at the Launcher but, to create a cooperative session these steps must be followed:

1. At the Launcher, click *Play* button on the project's card.
2. At the Player interface, go to the menu and click on *New* option.
3. At the creation dialog, increased the number of players and click on the *Create* button.

To join the cooperative session:

1. At the Launcher, click *Play* button on the same project's card.
2. At the Player interface, go to the menu and click on *Join* option.
3. At the joining dialog, increased specific the [IP address](https://flathub.org/apps/org.gabmus.whatip) of the host and click on the *Join* button.

## Editing scenes

Editing an existing Scene is easy as clicking the *Edit* button on the project's card but, to create a new Scene it's recommended to start off an existing project such as a Thematic Pack. So, to add a new Scene these steps must be followed:

1. At the Launcher, click the *Edit* button on the project's card.
2. At the Scene Editor, go to the menu and click on the *New* option.

### Basic concepts

A Scene is simply a collection of Entities arranged in tiles matrix. The basic properties of a Scene are:

* A **name** that must be unique among the project's Scenes.
* The day **time** in which the scene occurs. It can be *Day*, *Night* or *Dynamic*.
* if *Dynamic*, the *duration* specifies the seconds of a full day and night cycle.
* The **width** of the scene specifies the number of tiles on the horizontal axis.
* The **height** of the scene specifies the number of tiles on the vertical axis.

### Basic workflow

The basic Scene editing workflow resembles a *painting tool* in the sense that Entities are painted to the Scene. The basic steps are the following:

1. To **add** Entities to the Scene, select an Entity from the left panel and place it on the Scene by clicking a tile in the matrix.
2. To **remove** Entities from the scene, select the *Remove* tool from the left panel and remove it from the Scene by clicking the tile in the matrix.

Although Entities come with predefined properties and behaviors, particular Entities in the Scene can be **customized** by selecting the *Edit* tool from the left panel and then clicking the tile in the matrix.

Additionally, the Scene Editor provides helpers to make things easier such as:

* Drawing area selector, to add multiple Entities at once.
* Layer selector, to modify Entities at a specific layer.
* Time selector, to visualize the Scene at *Day* or *Night*.

### Tips and tricks

For an improved experience, try the following tips and tricks:

* When the creating the Scene's terrain, use the Layer selector and set it at *Layer 0*. This will avoid unnecessary stacking of overlapping terrain tiles and ease the editing workflow overall.
