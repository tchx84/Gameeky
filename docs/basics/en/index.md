# Documentation

> ⚠️ **Warning:** Gameeky is still in early stages of development and therefore things are subject to change.

> 📝 **Note:** This document is not an exhaustive tutorial on everything Gameeky can do, but should provide enough directions to get started.

## Topics

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Thematic packs](#thematic-packs)
4. [Overview](#overview)
5. [The launcher](#the-launcher)
6. [The player](#the-player)
7. [Cooperative game play](#cooperative-game-play)
8. [The scene editor](#the-scene-editor)
9. [The entity editor](#the-entity-editor)
10. [LOGO-like code](#logo-like-code)
11. [Plugins](#plugins)

## Introduction

[Gameeky](https://github.com/tchx84/gameeky) lets young learners and educators create and explore cooperative games and learning experiences. More specifically:

* Play and explore games with friends.
* Create new games without writing any code.
* Tell stories through these games.
* Nurture artistic skills by designing game objects and creatures.
* Grasp the basics of programming using Python in a LOGO-like experience.
* Mature programming skills by extending games with Python plugins.

> 📝 **Note:** This is a learning tool in the shape of a game engine. It's not a professional game engine. If you're looking for a tool to create professional video games, please consider the [Godot](https://godotengine.org) game engine.

## Installation

The recommended installation method is through the software center of the system, e.g., *GNOME Software*. Search for *Gameeky* and install it. Alternatively, it can also be installed from [Flathub](https://flathub.org). Similarly, search for *Gameeky* and follow the website instructions.

Lastly, it can also be installed from the terminal:

```bash
flatpak --user install flathub dev.tchx84.Gameeky
```

## Thematic packs

Gameeky provides predefined packs of building blocks for different interests, e.g., a farming role playing [game](https://github.com/tchx84/FreedomValley) set in a medieval fantasy world. A thematic pack contains:

* Assets like tilesets, sprites and sounds.
* Entities created from these assets, with predefined properties and behaviors.
* Scenes created with those entities.
* Actuators that extend the predefined behaviors.

These building blocks can be reused to create custom scenes, new games and many learning materials.

The recommended installation method is through the software center of the system, e.g., *GNOME Software*. Thematic packs are offered as addons from the software center page. Alternatively, it can also be installed from [Flathub](https://flathub.org). Similarly, thematic packs are offered as addons from the website. Select the addon and follow the website instructions.

Lastly, packs can also be installed from the terminal:

```bash
flatpak --user remote-ls flathub | grep dev.tchx84.Gameeky.ThematicPack
flatpak --user install flathub dev.tchx84.Gameeky.ThematicPack.FreedomValley
```

## Overview

The Gameeky package provides four main components:

1. The launcher is the main component where all thematic packs and projects can be found and launched from.
2. The player is where games can be played and joined.
3. The scene editor is where scenes can be created and edited.
4. The entity editor is where entities can be created and edited.

## The launcher

The launcher serves as the Gameeky starting point. It provides an easy way to manage thematic packs installed as addons and projects located under the `~/gameeky` directory. The manager supports all the basic management operations:

* Create new thematic packs and project from scratch.
* Edit existing projects.
* Remove existing projects.

![](https://raw.githubusercontent.com/tchx84/Gameeky/main/data/screenshots/en/04.png)

## The player

The player provides a visual representation of the game world and the means to interact with that world.

To start a game, click on the *Play* button of the project from the launcher. This will start the default scene for that project. Every thematic pack and project comes with a default scene. To play other scenes from the same project, follow these steps:

1. From the launcher, click on the *Play* button of the project.
2. From the player, go to the menu and select the *New* option.
3. From the creation dialog, select the scene file and click on the *Create* button.

![](https://raw.githubusercontent.com/tchx84/Gameeky/main/data/screenshots/en/02.png)

### In-game screen elements

Once in the game, the scene takes most of the screen but there are other elements as well.

The [HUD](https://en.wikipedia.org/wiki/HUD_(video_games)) is an interface placed at the bottom center of the screen. This element is used to visualize the user's character stats. It's composed of the following parts:

* A green bar that represents the user's character durability, e.g., to monitor the health of the character.
* A blue bar that represents the user's character stamina, e.g., to estimate how many actions can be performed by the character.
* An icon slot to display the entity that is currently being held by the user's character, e.g., to determine what tool the character is equipped with.

Another element is the dialogue viewer. This viewer is placed at the bottom of the screen and it's used to display in-game dialogues, e.g., a message from a game character or the narrator. It's composed of the following parts:

* A light blue section that contains the dialogue text.
* A button to close the dialogue.

### Controls

Once in the game, the user's character can be controlled with two methods:

* Keyboard controls. To see the full list of key bindings, go the menu and select the *Keyboard Shortcuts* option.
* Mouse controls. To see the available actions, right-click on the game view and select an action from the menu. To move the user's character, click on the scene view and the user's character will move towards that direction.

### Actions

The user's character can perform multiple actions to interact with the game world:

* *Move* to advance the user's character to one of four directions, e.g., to move the character to the *North*.
* *Take* to hold an entity from the scene. The entity must be directly in front of the user's character to be taken, e.g., to grab the entity and move that it later.
* *Use* to apply any effects that the held entity might have. These effects affect the entities that are located right in font of the user's character, e.g., to chop some logs with an axe.
* *Drop* to stop holding an entity, e.g., to stop moving it.
* *Interact* to activate any behavior from an entity. To interact with another entity, the entity must be located right in front of the user's character, e.g., to activate a teleport or read dialogues from letters.
* *Stop* to stop any action being performed and simply idle.

### Save files

The state of the game can be saved at any moment and restored later. Save files are full copies of the scene and therefore regular scene files.

1. To save the state of the game, go to the menu and select the *Save As…* option.
2. To restore the state of the game, follow the same steps described above to open an scene.

## Cooperative game play

Gameeky was designed from the ground up to create and share cooperative experiences. All the games created with it can be played cooperatively. There are no special requirements. Although there's no theoretical limit as for how many users can join a cooperative game, there are technical limitations. E.g., limited computing resources.

To start a cooperative game, follow these steps:

1. From the launcher, click on the *Play* button from the project's card.
2. From the player, go to the menu and select the *New* option.
3. From the creation dialog, increase the number of participants and then click on the *Create* button.

To join a cooperative game:

1. From the launcher, click on the *Play* button from the same project's card.
2. From the player, go to the menu and select the *Join* option.
3. From the join dialog, specify the [IP address](https://flathub.org/apps/org.gabmus.whatip) of the user who started the cooperative game and click on the *Join* button.

> 📝 **Note:** All the users joining a cooperative game must have a copy of the same thematic pack or project.

> 📝 **Note:** Custom scenes created from thematic packs don't need to be shared. The scene is automatically shared during game play, as long as all users share the same thematic pack.

## The scene editor

The scene editor lets users create and modify scenes. It serves as the initial and simplest form of no-code creation experience in Gameeky.

To edit an existing Scene, click on the *Edit* button of the project from the launcher. To create a new scene it's recommended to start off an existing project such as a thematic pack. Follow these steps to add a new Scene:

1. From the launcher, click on the *Copy* button of the project. This step is **only** needed for thematic packs. Thematic packs can't be modified, so this creates an editable copy.
2. From the launcher, click on the *Edit* button of the project.
3. From the scene editor, go to the menu and select the *New* option.

![](https://raw.githubusercontent.com/tchx84/Gameeky/main/data/screenshots/en/01.png)

### Concepts

A scene is a collection of entities arranged in a tiles matrix. The basic properties of a scene are:

* A *Name* that must be unique among the scenes of the same project.
* The *Time* of the day in which the scene occurs. It can be *Day*, *Night* or *Dynamic*.
* If *Dynamic*, the *Duration* specifies the number of seconds that it takes to complete a full day and night cycle. Otherwise this property is ignored.
* The *Width* of the scene specifies the total number of tiles on the horizontal axis.
* The *Height* of the scene specifies the total number of tiles on the vertical axis.

### Workflow

The scene editing workflow resembles one of a painting tool. Entities are painted and removed to and from the scene. The basic steps to edit a scene are the following:

1. To add entities to the scene, select an entity from the left panel and place it on the scene by clicking on a tile in the matrix.
2. To remove entities from the scene, select the *Remove* tool from the left and then click on the entity tile in the matrix.
3. Although entities come with predefined properties and behaviors, particular entities in the scene can be customized. Select the *Edit* tool from the left panel and then click on the entity tile in the matrix.

Additionally, the scene editor provides helpers to make things easier such as:

* Drawing area selector to add or remove multiple entities at once, e.g., to quickly create the scene terrain.
* Layer selector to modify entities at a specific layer, e.g., to quickly modify the scene terrain.
* Time selector to visualize the scene during *Day* or *Night*, e.g., to inspect the light sources in the scene.

### Tips and tricks

For an improved experience, try the following tips and tricks:

* When creating the basic terrain of the scene, use the layer selector and set it at *Layer 0*. This will reduce the unnecessary overlapping of terrain tiles and it will ease the editing workflow overall.
* When editing a scene, leave the player open on that scene. When changes to the scene are saved, the player will detect these changes and present an option to reload the scene with the new changes. This reduces the time switching between the scene editor and the player.
* When editing a scene, use the initial location setter tool from the left panel to place the user's character in a convenient location to inspect the changes.

## The entity editor

The entity editor lets users create and modify game objects and creatures. It provides a deeper no-code creation experience, as it requires understanding the underlying systems of Gameeky.

Before creating a new entity from scratch, it's recommended to inspect existing entities from thematic packs. So, to inspect an existing entity follow these steps:

1. From the scene editor, right-click on an entity in the left panel.
2. Select the *Edit* option from the menu.

To create a new entity:

1. From the scene editor, right-click anywhere in the left panel.
2. Select the *Add* option from the menu.

![](https://raw.githubusercontent.com/tchx84/Gameeky/main/data/screenshots/en/03.png)

### Concepts

Entities represent everything that can exist in the game, e.g., the grass, the user's character, a light source, the background music and even the game logic. An entity is composed of three parts:

1. Game logic properties.
2. Graphics.
3. Sounds.

#### Game logic properties

These properties determine how entities behave and interact with other entities, e.g., different combinations of these properties will determine whether an entity is acting as a static stone or a living foe.

Although there are two dozen properties, a few of these require special attention here:

* The *Identifier* must be unique among all the entities of the same project.
* An entity is always in one and a single *State*, e.g., *Idling*, *Moving*, *Destroyed*, etc. The state can change by performing different actions, by intrinsic or extrinsic means.
* An entity is always pointing to one and a single *Direction*. It can be *North*, *East*, *South* or *West*.
* An entity state can be changed intrinsically by *Actuators* that provide predefined logic, e.g., a *Roams* actuator will move the entity to random directions, and a *Destroys* actuator will flag the entity for removal from the scene when its durability reaches zero.
* All entity properties coexist in a single system and therefore behaviors can emerge from different combinations of these properties, e.g., the speed in which an entity can move is determined by its *Weight* and its *Strength*, while the total weight of an entity depends on the weight of the entity its holding, and so on.

#### Graphics

Entities are represented on the screen through 2D graphics, which can be static or animated.

These graphics are assigned to specific combinations of state and direction, e.g., a specific animation will be rendered when an entity is *Moving* to the *West*, while another animation will be rendered when the same entity is *Idling* to the *South*.

All entities must provide a *Default* graphic, e.g., to visualize it on the scene editor or debug plugins.

#### Sounds

Similarly to graphics, entities can emit sounds when in specific states, e.g., footsteps sound is played when the entity is *Moving*. Directions don't matter here.

There aren't *Default* sounds, as sounds are optional.

### Workflow

The entity creation workflow is similar to filling a form or a template. The most basic entity is created with the following steps:

1. Under the *Game* tab, start setting the values from top to bottom. Note that all properties provide their own defaults. Only the identifier is mandatory. Setting a name is recommended so that it's easier to find the entity on the scene editor.
2. Under the *Graphics* tab, click on the *Add* button to create the first and default animation. Leave both *State* and *Direction* to *Default*. Expand the *Details* section of the default animation to select an image. Click on the *View* button to inspect the selected image.
3. Save the entity and use it from the scene editor.

### Tips and tricks

For an improved experience, try the following tips and tricks:

* When creating a new thematic pack assume that the entity with identifier number *1* will be assigned to the user's character in the game.
* When creating a new entity, always begin with setting the identifier number and then *Save* the Entity to disk. Keep the name suggested by the entity editor. This will make it easier to assign unique identifiers along the road.
* When creating a new animation, always leave both, the entity editor and the tileset viewer, open side by side. This will make it easier to set up the animation frames.
* After creating an animation, click on the *Copy* button to add the next animation. This will make it easier to set up the next animation.

## LOGO-like code

Having support for cooperative game play opens the door for cooperators that can be controlled with code. To achieve this, Gameeky provides a small library that enables learners to control a single Entity using Python, in a LOGO-like experience.

### Workflow

Follow these steps to start a cooperative game:

1. From the launcher, click on the *Play* button of the project.
2. From the player, go to the menu and select the *New* option.
3. From the creation dialog, increased the number of participants and then click on the *Create* button.

To join the game from code, these steps must be followed:

1. Write Python code that uses the Gameeky library, see examples below.
2. Run that code from the terminal with the following command:

```bash
cd ~/path/to/my/file/
flatpak --user run --filesystem=$PWD --command=dev.tchx84.Gameeky.Exec dev.tchx84.Gameeky sample.py
```

### Examples

Join and leave a [game](../../../src/gameeky/library/game.py):

```python
from gameeky.library import Game

game = Game(project="~/gameeky/project", address="127.0.0.1")
game.join()
game.quit()
```

Perform [actions](../../../src/gameeky/common/definitions.py):

```python
from gameeky.library import Game
from gameeky.common.definitions import Direction

game = Game(project="~/gameeky/project", address="127.0.0.1")
game.join()
game.update()

game.idle(time=1000)
game.move(Direction.EAST, time=1000)
game.move(Direction.WEST, time=1000)
game.take(time=1000)
game.use(time=1000)
game.drop(time=1000)
game.interact(time=1000)

game.quit()
```

Inspect the position and basic properties of the user's character [entity](../../../src/gameeky/common/entity.py):

```python
from gameeky.library import Game

game = Game(project="~/gameeky/project", address="127.0.0.1")
game.join()
game.update()

print(game.entity.position.x, game.entity.position.y)

game.quit()
```

Inspect the state of the [scene](../../../src/gameeky/common/scene.py):

```python
from gameeky.library import Game

game = Game(project="~/gameeky/project", address="127.0.0.1")
game.join()
game.update()

for entity in game.scene.entities:
    print(entity.position.x, entity.position.y)

game.quit()
```

> 📝 **Note:** Cooperators can only see their immediate surroundings from the scene, not the full scene.

Inspect the advance [stats](../../../src/gameeky/common/stats.py) of the user's character entity:

```python
from gameeky.library import Game

game = Game(project="~/gameeky/project", address="127.0.0.1")
game.join()
game.update()

print(game.stats.durability, game.stats.stamina, game.stats.held)

game.quit()
```

### Tips and tricks

For an improved experience, try the following tips and tricks:

* When testing code locally, leave both the player and the terminal open side by side. That way it will easier to see the code in action, literally.

## Plugins

Actuators can modify the behavior of an entity. A single entity can use multiple actuators to model more complex behaviors. Although there's a wide range of predefined actuators, the end result is limited when compared to actual code. Therefore, Gameeky provides support for user-created actuators to go beyond what the predefined actuators can do.

### Concepts

There are three types of actuators:

1. Regular actuators enact on each tick of the scene, e.g., to [move](../../../src/gameeky/server/game/actuators/roams.py) the entity to a random location on each tick.
2. Activatable actuators enact only in fixed time intervals or when explicitly activated by another entity, e.g., to [spawn](../../../src/gameeky/server/game/actuators/spawns.py) a new foe to the scene every five seconds.
3. Interactable actuators enact when other entities interact with its entity, e.g., to [teleport](../../../src/gameeky/server/game/actuators/teleports.py) an entity to a different location when that entity interacts with a portal.

All actuators use their own entity game properties to modify their behavior:

* The *Target Name* and *Target Type* properties can be used to filter the entities affected by the actuator, e.g., to [target](../../../src/gameeky/server/game/actuators/aggroes.py) only certain entities types for aggression.
* The *Rate* property can be used in activatables to reduce the activation frequency, e.g., to [hatch](../../../src/gameeky/server/game/actuators/transmutes.py) an egg into a chicken after ten seconds.
* The *Radius* property can be used to determine the area of effect of an actuator, e.g., to [burn](../../../src/gameeky/server/game/actuators/affects.py) entities when stepping into a fire.

### Workflow

To create a new actuator, follow the steps:

1. Open a new document in a text editor.
2. Write an actuator class, see examples below.
3. Save the new document to `~/gameeky/PROJECT_NAME/actuators/ACTUATOR_NAME.py`
4. From the entity editor, go under the *Game* tab to the actuators section.
5. A new option called *ACTUATOR_NAME* will be displayed along with the predefined actuators.
6. Select it and save the entity to disk.

> 📝 **Note:** User-created actuators can also be accessed from the scene editor when customizing specific entities.

### Examples

A minimal [actuator](../../../src/gameeky/server/game/actuators/base.py) class:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        pass
```

Inspect the [entity](../../../src/gameeky/server/game/entity.py):

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        print(self.entity.name)
```

Perform an action on the entity:

```python
from gameeky.plugins import Actuator as Plugin
from gameeky.common.definitions import Action, Direction

class Actuator(Plugin):
    def tick(self) -> None:
        self.entity.perform(Action.MOVE, Direction.SOUTH)
```

Send a dialogue to the entity:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        self.entity.tell("Hello...")
```

Inspect all the other entities sitting right in front of the entity:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        for entity in self.entity.obstacles:
            print(entity.name)
```

Inspect all the other entities that share the same position as the entity:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        for entity in self.entity.surfaces:
            print(entity.name)
```

Inspect all the other entities that surround the entity:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        for entity in self.entity.surroundings:
            print(entity.name)
```

> 📝 **Note:** The *surroundings* method takes into account the *Radius* property of the entity.

Inspect all entities in the [scene](../../../src/gameeky/server/game/scene.py), that are not static:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        for entity in self.entity.scene.mutables:
            print(entity.name)
```

Inspect all entities that are controlled by users:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        for entity in self.entity.scene.playables:
            print(entity.name)
```

Create an actuator that enacts every five seconds:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    activatable = True

    def tick(self) -> None:
        if not self.ready:
            return

        print("Activated...")

        super().tick()
```

> 📝 **Note:** The *ready* property takes into account the *Rate* property of the entity.

Create an actuator that enacts only when interacted by users:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    interactable = True

    def prepare(self, interactee: "Entity") -> bool:
        if interactee.playable is False:
            return False

        return super().prepare(interactee)

    def tick(self) -> None:
        if self.interactee is None:
            return

        print(f"Interacted with {self._interactee.name}")

        super().tick()
```

Fore more complex examples check Gameeky's predefined [actuators](../../../src/gameeky/server/game/actuators/) directory.

### Tips and tricks

For an improved experience, try the following tips and tricks:

* A single actuator should not modify the whole scene. Iterating over all the entities in the scene is extremely costly and the performance will be severed, e.g., stick to *mutables* and *playables* only.
* It's preferred to write different actuators for different behaviors, e.g., avoid writing a single actuator that implements all of the custom behaviors. This will make it easier to understand and reuse in the long run.
* Use only public methods and attributes, e.g., stick to methods like *obstacles* or *interactee*. These will make it less likely for the actuators to break in the future.
