# Documentación

> ⚠️ **Advertencia:** Gameeky aún se encuentra en las primeras etapas de desarrollo y, por lo tanto, las cosas están sujetas a cambios.

> 📝 **Notese:** Este documento no es un tutorial exhaustivo sobre todo lo que Gameeky puede hacer, pero debería proporcionar suficientes instrucciones para comenzar.

## Temas

1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Paquetes temáticos](#paquetes-temáticos)
4. [Descripción general](#descripción-general)
5. [El lanzador](#el-lanzador)
6. [El reproductor](#el-reproductor)
7. [Juego cooperativo](#juego-cooperativo)
8. [El editor de escenas](#el-editor-de-escenas)
9. [El editor de entidades](#el-editor-de-entidades)
10. [Código similar a LOGO](#código-similar-a-logo)
11. [Complementos](#complementos)

## Introducción

[Gameeky](https://github.com/tchx84/gameeky) permite a jóvenes estudiantes y educadores crear y explorar juegos cooperativos y experiencias de aprendizaje. Más específicamente:

* Juega y explora juegos con amigos.
* Crea nuevos juegos sin escribir ningún código.
* Cuenta historias a través de estos juegos.
* Fomenta habilidades artísticas diseñando objetos y criaturas del juego.
* Aprende conceptos básicos de programación usando Python en una experiencia similar a [LOGO](https://es.wikipedia.org/wiki/Logo_(lenguaje_de_programaci%C3%B3n)).
* Madura habilidades de programación ampliando juegos con complementos en Python.

> 📝 **Notese:** Esta es una herramienta de aprendizaje en forma de motor de juego. No es un motor de juego profesional. Si está buscando una herramienta para crear videojuegos profesionales, considere el motor de juegos [Godot](https://godotengine.org).

## Instalación

El método de instalación recomendado es a través del centro de software del sistema, por ejemplo, *GNOME Software*. Busque *Gameeky* e instálelo. Alternativamente, también se puede instalar desde [Flathub](https://flathub.org). De manera similar, busque *Gameeky* y siga las instrucciones del sitio web.

Por último, también se puede instalar desde la terminal:

```bash
flatpak --user install flathub dev.tchx84.Gameeky
```

## Paquetes temáticos

Gameeky proporciona paquetes con bloques de construcción predefinidos para diferentes intereses, por ejemplo, un [juego] de rol agrícola (https://github.com/tchx84/FreedomValley) ambientado en un mundo de fantasía medieval. Un paquete temático contiene:

* Recursos como conjuntos de mosaicos, sprites y sonidos.
* Entidades creadas a partir de estos recursos, con propiedades y comportamientos predefinidos.
* Escenas creadas con esas entidades.
* Actuadores que amplían los comportamientos predefinidos.

Estos bloques de construcción se pueden reutilizar para crear escenas personalizadas, juegos nuevos y muchos materiales de aprendizaje.

El método de instalación recomendado es a través del centro de software del sistema, por ejemplo, *Software GNOME*. Los paquetes temáticos se ofrecen como complementos desde la página del centro de software. Alternativamente, también se puede instalar desde [Flathub](https://flathub.org). Del mismo modo, los paquetes temáticos se ofrecen como complementos del sitio web. Seleccione el complemento y siga las instrucciones del sitio web.

Por último, los packs también se pueden instalar desde la terminal:

```bash
flatpak --user remote-ls flathub | grep dev.tchx84.Gameeky.ThematicPack
flatpak --user install flathub dev.tchx84.Gameeky.ThematicPack.FreedomValley
```

## Descripción general

Gameeky proporciona cuatro componentes principales:

1. El lanzador es el componente principal desde donde se pueden encontrar y ejecutar todos los paquetes temáticos y proyectos.
2. El reproductor es el lugar donde se puede jugar y unirse a juegos.
3. El editor de escenas es donde se pueden crear y editar escenas.
4. El editor de entidades es donde se pueden crear y editar entidades.

## El lanzador

El lanzador sirve como punto de partida de Gameeky. Proporciona una manera fácil de administrar paquetes temáticos instalados como complementos y proyectos ubicados en el directorio `~/gameeky`. El administrador soporta todas las operaciones básicas de gestión:

* Crear nuevos paquetes temáticos y proyectos desde cero.
* Editar proyectos existentes.
* Eliminar proyectos existentes.

![](https://raw.githubusercontent.com/tchx84/Gameeky/main/data/screenshots/en/04.png)

## El reproductor

El reproductor proporciona una representación visual del mundo del juego y los medios para interactuar con ese mundo.

Para iniciar un juego, haga clic en el botón *Jugar* del proyecto desde el lanzador. Esto iniciará la escena predeterminada para ese proyecto. Cada paquete temático y proyecto viene con una escena predeterminada. Para jugar otras escenas del mismo proyecto, siga estos pasos:

1. Desde el lanzador, haga clic en el botón *Jugar* del proyecto.
2. Desde el reproductor, vaya al menú y seleccione la opción *Nuevo*.
3. Desde el cuadro de diálogo de creación, seleccione el archivo de escena y haga clic en el botón *Crear*.

![](https://raw.githubusercontent.com/tchx84/Gameeky/main/data/screenshots/en/02.png)

### Elementos de la pantalla del juego

Una vez en el juego, la escena ocupa la mayor parte de la pantalla, pero también hay otros elementos.

El [HUD](https://es.wikipedia.org/wiki/HUD_(videojuegos)) es una interfaz ubicada en la parte inferior central de la pantalla. Este elemento se utiliza para visualizar las estadísticas del personaje del usuario. Está compuesto por las siguientes partes:

* Una barra verde que representa la durabilidad del personaje del usuario, por ejemplo, para monitorear la salud del personaje.
* Una barra azul que representa la resistencia del personaje del usuario, por ejemplo, para estimar cuántas acciones puede realizar el personaje.
* Un icono para mostrar la entidad que actualmente sostiene el personaje del usuario, por ejemplo, para determinar con qué herramienta está equipado el personaje.

Otro elemento es el visor de diálogos. Este visor se coloca en la parte inferior de la pantalla y se utiliza para mostrar diálogos del juego, por ejemplo, un mensaje de un personaje del juego o del narrador. Está compuesto por las siguientes partes:

* Una sección de color azul claro que contiene el texto del diálogo.
* Un botón para cerrar el diálogo.

### Controles

Una vez en el juego, el personaje del usuario se puede controlar con dos métodos:

* Controles de teclado. Para ver la lista completa de combinaciones de teclas, vaya al menú y seleccione la opción *Atajos de Teclado*.
* Controles del ratón. Para ver las acciones disponibles, haga clic derecho en la escena del juego y seleccione una acción del menú. Para mover el personaje del usuario, haga clic en la escena y el personaje del usuario se moverá en esa dirección.

### Acciones

El personaje del usuario puede realizar múltiples acciones para interactuar con el mundo del juego:

* *Mover* para hacer avanzar el personaje del usuario en una de cuatro direcciones, por ejemplo, para mover el personaje hacia el *Norte*.
* *Tomar* para sostener una entidad de la escena. La entidad debe estar directamente frente al personaje del usuario para ser tomada, por ejemplo, para sostener la entidad y moverla.
* *Usar* para aplicar cualquier efecto que la entidad sostenida pueda tener. Estos efectos afectan a las entidades que se encuentran justo en la fuente del personaje del usuario, por ejemplo, para cortar algunos troncos con un hacha.
* *Soltar* para dejar de sostener una entidad, por ejemplo, para dejar de moverla.
* *Interactuar* para activar cualquier comportamiento de una entidad. Para interactuar con otra entidad, la entidad debe estar ubicada justo en frente del personaje del usuario, por ejemplo, para activar un portal o leer letreros.
* *Detener* para detener cualquier acción que se esté realizando y simplemente hacer nada.

### Guardar archivos

El estado del juego se puede guardar en cualquier momento y restaurar más tarde. Los archivos guardados son copias completas de la escena y, por lo tanto, archivos de escena normales.

1. Para guardar el estado del juego, vaya al menú y seleccione la opción *Guardar Como…*.
2. Para restaurar el estado del juego, sigue los mismos pasos descritos anteriormente para abrir una escena.

## Juego cooperativo

Gameeky fue diseñado desde cero para crear y compartir experiencias cooperativas. Todos los juegos creados con él se pueden jugar de forma cooperativa. No hay requisitos especiales. Aunque no existe un límite teórico en cuanto a cuántos usuarios pueden unirse a un juego cooperativo, existen limitaciones técnicas. Por ejemplo, recursos informáticos limitados.

Para iniciar un juego cooperativo, sigue estos pasos:

1. Desde el lanzador, haga clic en el botón *Jugar* de la tarjeta del proyecto.
2. Desde el reproductor, vaya al menú y seleccione la opción *Nuevo*.
3. Desde el cuadro de diálogo de creación, aumente el número de participantes y luego haga clic en el botón *Crear*.

Para unirse a un juego cooperativo:

1. Desde el lanzador, haga clic en el botón *Jugar* de la tarjeta del mismo proyecto.
2. Desde el reproductor, vaya al menú y seleccione la opción *Unirse*.
3. En el cuadro de diálogo para unirse, especifique la [dirección IP](https://flathub.org/apps/org.gabmus.whatip) del usuario que inició el juego cooperativo y haga clic en el botón *Unirse*.

> 📝 **Notese:** Todos los usuarios que se unan a un juego cooperativo deben tener una copia del mismo paquete temático o proyecto.

> 📝 **Notese:** No es necesario compartir las escenas personalizadas creadas a partir de paquetes temáticos. La escena se comparte automáticamente durante el juego, siempre que todos los usuarios compartan el mismo paquete temático.

## El editor de escenas

El editor de escenas permite a los usuarios crear y modificar mundos del juego. Sirve como la experiecia inicial y más sencilla de creación sin código en Gameeky.

Para editar una escena existente, haga clic en el botón *Editar* del proyecto desde el lanzador. Para crear una nueva escena, se recomienda comenzar con un proyecto existente, como un paquete temático. Siga estos pasos para agregar una nueva escena:

1. Desde el lanzador, haga clic en el botón *Copiar* del proyecto. Este paso **sólo** es necesario para los paquetes temáticos. Los paquetes temáticos no se pueden modificar, por lo que se crea una copia editable.
2. Desde el lanzador, haga clic en el botón *Editar* del proyecto.
3. Desde el editor de escenas, vaya al menú y seleccione la opción *Nuevo*.

![](https://raw.githubusercontent.com/tchx84/Gameeky/main/data/screenshots/en/01.png)

### Conceptos

Una escena es una colección de entidades dispuestas en una cuadrícula de mosaicos. Las propiedades básicas de una escena son:

* Un *Nombre* que debe ser único entre las escenas del mismo proyecto.
* La *Tiempo* del día en que ocurre la escena. Puede ser *Día*, *Noche* o *Dinámico*.
* Si es *Dinámico*, la *Duración* especifica la cantidad de segundos que se necesitan para completar un ciclo completo de día y noche. De lo contrario, esta propiedad se ignora.
* El *Ancho* de la escena especifica el número total de mosaicos en el eje horizontal.
* La *Alto* de la escena especifica el número total de mosaicos en el eje vertical.

### Flujo de trabajo

El flujo de trabajo de edición de escenas se parece al de una herramienta de diseño gráfico. Las entidades se pintan y se retiran de la escena. Los pasos básicos para editar una escena son los siguientes:

1. Para agregar entidades a la escena, seleccione una entidad en el panel izquierdo y colóquela en la escena haciendo clic en un mosaico de la cuadrícula.
2. Para eliminar entidades de la escena, seleccione la herramienta *Eliminar* de la izquierda y luego haga clic en el mosaico de la entidad en la cuadrícula.
3. Aunque las entidades vienen con propiedades y comportamientos predefinidos, se pueden personalizar entidades particulares de la escena. Seleccione la herramienta *Editar* en el panel izquierdo y luego haga clic en el mosaico de entidad en la cuadrícula.

Además, el editor de escenas proporciona ayudas para facilitar las cosas, como por ejemplo:

* Selector de área de dibujo para agregar o eliminar múltiples entidades a la vez, por ejemplo, para crear rápidamente el terreno de la escena.
* Selector de capas para modificar entidades en una capa específica, por ejemplo, para modificar rápidamente el terreno de la escena.
* Selector de tiempo para visualizar la escena durante el *Día* o la *Noche*, por ejemplo, para inspeccionar las fuentes de luz en la escena.

### Consejos y trucos

Para un mejor experiencia, siga estos consejos y trucos:

* Al crear el terreno básico de la escena, use el selector de capas y configúrelo en *Capa 0*. Esto reducirá la superposición innecesaria de mosaicos de terreno y facilitará el flujo de trabajo de edición en general.
* Al editar una escena, deje el reproductor abierto en esa escena. Cuando se guarden los cambios en la escena, el reproductor detectará estos cambios y presentará una opción para recargar la escena con los nuevos cambios. Esto reduce el tiempo de cambio entre el editor de escenas y el reproductor.
* Al editar una escena, use la herramienta de configuración de ubicación inicial del panel izquierdo para colocar el personaje del usuario en una ubicación conveniente para inspeccionar los cambios.

## El editor de entidades

El editor de entidades permite a los usuarios crear y modificar criaturas y objetos del juego. Proporciona una experiencia de creación sin código más profunda, ya que requiere comprender los sistemas subyacentes de Gameeky.

Antes de crear una nueva entidad desde cero, se recomienda inspeccionar las entidades existentes de los paquetes temáticos. Entonces, para inspeccionar una entidad existente, siga estos pasos:

1. Desde el editor de escenas, haga clic derecho en una entidad en el panel izquierdo.
2. Seleccione la opción *Editar* del menú.

Para crear una nueva entidad:

1. Desde el editor de escenas, haga clic derecho en cualquier parte del panel izquierdo.
2. Seleccione la opción *Agregar* del menú.

![](https://raw.githubusercontent.com/tchx84/Gameeky/main/data/screenshots/en/03.png)

### Conceptos

Las entidades representan todo lo que puede existir en el juego, por ejemplo, la hierba, el personaje del usuario, una fuente de luz, la música de fondo e incluso la lógica del juego. Una entidad se compone de tres partes:

1. Propiedades de la lógica del juego.
2. Gráficos.
3. Sonidos.

#### Propiedades de la lógica del juego

Estas propiedades determinan cómo las entidades se comportan e interactúan con otras entidades; por ejemplo, diferentes combinaciones de estas propiedades determinarán si una entidad actúa como una piedra estática o como un enemigo vivo.

Aunque hay dos docenas de propiedades, algunas de ellas requieren atención especial aquí:

* El *Identificador* debe ser único entre todas las entidades de un mismo proyecto.
* Una entidad siempre está en un solo *Estado*, por ejemplo, *Inactivo*, *Moviendo*, *Destruido*, etc. El estado puede cambiar realizando diferentes acciones, por medios intrínsecos o extrínsecos.
* Una entidad siempre apunta a una única *Dirección*. Puede ser *Norte*, *Este*, *Sur* u *Oeste*.
* El estado de una entidad se puede cambiar intrínsecamente mediante *Actuadores* que proporcionan una lógica predefinida, por ejemplo, un actuador *Deambula* moverá la entidad en direcciones aleatorias, y un actuador *Se destruye* señalará la entidad para su eliminación de la escena cuando su durabilidad llegue a cero.
* Todas las propiedades de una entidad coexisten en un solo sistema y por lo tanto pueden surgir comportamientos de diferentes combinaciones de estas propiedades, por ejemplo, la velocidad a la que una entidad puede moverse está determinada por su *Peso* y su *Fuerza*, mientras que el peso total de una entidad depende del peso de la entidad que sostiene, y así sucesivamente.

#### Gráficos

Las entidades se representan en pantalla a través de gráficos 2D, que pueden ser estáticos o animados.

Estos gráficos se asignan a combinaciones específicas de estado y dirección, por ejemplo, se representará una animación específica cuando una entidad se *Mueva* hacia el *Oeste*, mientras que se representará otra animación cuando la misma entidad esté *Quieta* hacia el *Sur*.

Todas las entidades deben proporcionar un gráfico *Predeterminado*, por ejemplo, para visualizarlo en el editor de escenas o al depurar complementos.

#### Sonidos

De manera similar a los gráficos, las entidades pueden emitir sonidos cuando se encuentran en estados específicos, por ejemplo, el sonido de pasos se reproduce cuando la entidad se está *Moviendo*. Las direcciones no importan aquí.

No hay sonidos *Predeterminados*, ya que los sonidos son opcionales.

### Flujo de trabajo

El flujo de trabajo de creación de entidades es similar a completar un formulario o una plantilla. La entidad más básica se crea con los siguientes pasos:

1. En la pestaña *Juego*, comience a configurar los valores de arriba a abajo. Tenga en cuenta que todas las propiedades proporcionan sus propios valores predeterminados. Sólo el identificador es obligatorio. Se recomienda establecer un nombre para que sea más fácil encontrar la entidad en el editor de escenas.
2. En la pestaña *Gráficos*, haga clic en el botón *Agregar* para crear la primera animación predeterminada. Deje *Estado* y *Dirección* en *Predeterminado*. Expanda la sección *Detalles* de la animación predeterminada para seleccionar una imagen. Haga clic en el botón *Ver* para inspeccionar la imagen seleccionada.
3. Guarde la entidad y úsela desde el editor de escenas.

### Consejos y trucos

Para una mejor experiencia, siga estos consejos y trucos:

* Al crear un nuevo paquete temático, asuma que la entidad con el número de identificador *1* se asignará al personaje del usuario en el juego.
* Al crear una nueva entidad, comience siempre configurando el número de identificador y luego *Guarde* la entidad en el disco. Mantenga el nombre sugerido por el editor de entidades. Esto facilitará la asignación de identificadores únicos a la larga.
* Al crear una nueva animación, deje siempre abiertos el editor de entidades y el visor de mosaicos, uno al lado del otro. Esto facilitará la configuración de los cuadros de animación.
* Después de crear una animación, haga clic en el botón *Copiar* para agregar la siguiente animación. Esto facilitará la configuración de la siguiente animación.

## Código similar a LOGO

Tener soporte para juegos cooperativos abre la puerta a cooperadores que pueden controlarse con código. Para lograr esto, Gameeky proporciona una pequeña biblioteca que permite a los usuarios controlar una única Entidad usando Python, en una experiencia similar a LOGO.

### Flujo de trabajo

Sigue estos pasos para iniciar un juego cooperativo:

1. Desde el lanzador, haga clic en el botón *Jugar* del proyecto.
2. Desde el reproductor, vaya al menú y seleccione la opción *Nuevo*.
3. Desde el cuadro de diálogo de creación, aumente el número de participantes y luego haga clic en el botón *Crear*.

Para unirse al juego desde el código se deben seguir estos pasos:

1. Escriba código Python que utilice la biblioteca Gameeky; consulte los ejemplos a continuación.
2. Ejecute ese código desde la terminal con el siguiente comando:

```bash
cd ~/path/to/my/file/
flatpak --user run --filesystem=$PWD --command=dev.tchx84.Gameeky.Exec dev.tchx84.Gameeky sample.py
```

### Ejemplos

Unirse y abandonar un [juego](../../../src/gameeky/library/game.py):

```python
from gameeky.library import Game

game = Game(project="~/gameeky/project", address="127.0.0.1")
game.join()
game.quit()
```

Realizar [acciones](../../../src/gameeky/common/definitions.py):

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

Inspeccionar la posición y las propiedades básicas del personaje del usuario [entidad](../../../src/gameeky/common/entity.py):

```python
from gameeky.library import Game

game = Game(project="~/gameeky/project", address="127.0.0.1")
game.join()
game.update()

print(game.entity.position.x, game.entity.position.y)

game.quit()
```

Inspeccione el estado de la [escena](../../../src/gameeky/common/scene.py):

```python
from gameeky.library import Game

game = Game(project="~/gameeky/project", address="127.0.0.1")
game.join()
game.update()

for entity in game.scene.entities:
    print(entity.position.x, entity.position.y)

game.quit()
```

> 📝 **Notese:** Los cooperadores solo pueden ver su entorno inmediato en la escena, no la escena completa.

Inspeccionar las [estadísticas](../../../src/gameeky/common/stats.py) avanzadas de la entidad de personaje del usuario:

```python
from gameeky.library import Game

game = Game(project="~/gameeky/project", address="127.0.0.1")
game.join()
game.update()

print(game.stats.durability, game.stats.stamina, game.stats.held)

game.quit()
```

### Consejos y trucos

Para una mejor experiencia, siga estos consejos y trucos:

* Cuando pruebe el código localmente, deje el reproductor y la terminal abiertos uno al lado del otro. De esa forma será más fácil ver el código en acción, literalmente.

## Complementos

Los actuadores pueden modificar el comportamiento de una entidad. Una sola entidad puede utilizar múltiples actuadores para modelar comportamientos más complejos. Aunque existe una amplia gama de actuadores predefinidos, el resultado final es limitado en comparación con el código real. Por lo tanto, Gameeky proporciona soporte para actuadores creados por el usuario, e ir más allá de lo que pueden hacer los actuadores predefinidos.

### Conceptos

Hay tres tipos de actuadores:

1. Los actuadores regulares actúan en cada tic de la escena, por ejemplo, para [mover](../../../src/gameeky/server/game/actuators/roams.py) la entidad a una ubicación aleatoria en cada tic.
2. Los actuadores activables actúan solo en intervalos de tiempo fijos o cuando son activados explícitamente por otra entidad, por ejemplo, para [agregar](../../../src/gameeky/server/game/actuators/spawns.py) un nuevo enemigo a la escena cada cinco segundos.
3. Los actuadores interactuables actúan cuando otras entidades interactúan con su entidad, por ejemplo, para [teletransportar](../../../src/gameeky/server/game/actuators/teleports.py) una entidad a una ubicación diferente cuando esa entidad interactúa con un portal.

Todos los actuadores utilizan las propiedades de juego de su entidad para modificar su comportamiento:

* Las propiedades *Nombre de Destino* y *Tipo de Destino* se pueden utilizar para filtrar las entidades afectadas por el actuador, por ejemplo, [apuntar](../../../src/gameeky/server/game/actuators/ aggroes.py) solo ciertos tipos de entidades para agresión.
* La propiedad *Tasa* se puede usar en activables para reducir la frecuencia de activación, por ejemplo, para [incubar](../../../src/gameeky/server/game/actuators/transmutes.py) un huevo en un pollo después de diez segundos.
* La propiedad *Radio* se puede utilizar para determinar el área de efecto de un actuador, por ejemplo, para [quemar](../../../src/gameeky/server/game/actuators/affects.py) entidades al entrar en un incendio.

### Flujo de trabajo

Para crear un nuevo actuador, siga los pasos:

1. Abra un nuevo documento en un editor de texto.
2. Escriba una clase de actuador; consulte los ejemplos a continuación.
3. Guarde el nuevo documento en `~/gameeky/NOMBRE_DEL_PROYECTO/actuators/NOMBRE_DEL_ACTUADOR.py`
4. Desde el editor de entidades, vaya a la pestaña *Juego* y a la sección de actuadores.
5. Se mostrará una nueva opción llamada *NOMBRE_DEL_ACTUADOR* junto con los actuadores predefinidos.
6. Selecciónelo y guarde la entidad en el disco.

> 📝 **Notese:** También se puede acceder a los actuadores creados por el usuario desde el editor de escenas al personalizar entidades específicas.

### Ejemplos

Una clase [actuador](../../../src/gameeky/server/game/actuators/base.py) mínima:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        pass
```

Inspeccionar la [entidad](../../../src/gameeky/server/game/entity.py):

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        print(self.entity.name)
```

Realizar una acción sobre la entidad:

```python
from gameeky.plugins import Actuator as Plugin
from gameeky.common.definitions import Action, Direction

class Actuator(Plugin):
    def tick(self) -> None:
        self.entity.perform(Action.MOVE, Direction.SOUTH)
```

Enviar un diálogo a la entidad:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        self.entity.tell("Hello...")
```

Inspeccionar todas las demás entidades que se encuentran en frente a la entidad:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        for entity in self.entity.obstacles:
            print(entity.name)
```

Inspeccionar todas las demás entidades que comparten la misma posición que la entidad:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        for entity in self.entity.surfaces:
            print(entity.name)
```

Inspeccionar todas las demás entidades que rodean la entidad:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        for entity in self.entity.surroundings:
            print(entity.name)
```

> 📝 **Notese:** El método *surroundings* tiene en cuenta la propiedad *Radio* de la entidad.

Inspeccionar todas las entidades en la [escena](../../../src/gameeky/server/game/scene.py), que no sean estáticas:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        for entity in self.entity.scene.mutables:
            print(entity.name)
```

Inspeccionar todas las entidades controladas por usuarios:

```python
from gameeky.plugins import Actuator as Plugin

class Actuator(Plugin):
    def tick(self) -> None:
        for entity in self.entity.scene.playables:
            print(entity.name)
```

Crear un actuador que actúa cada cinco segundos:

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

> 📝 **Notese:** La propiedad *ready* tiene en cuenta la propiedad *Tasa* de la entidad.

Crear un actuador que actúa solo cuando los usuarios interactúen con él:

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

Para ver ejemplos más complejos, consulte el directorio [actuadores](../../../src/gameeky/server/game/actuators/) predefinidos de Gameeky.

### Consejos y trucos

Para una mejor experiencia, siga estos consejos y trucos:

* Un solo actuador no debe modificar toda la escena. Iterar sobre todas las entidades en la escena es extremadamente costoso y el rendimiento se verá afectado, por ejemplo, limitarse a *mutables* y *playables* únicamente.
* Es preferible escribir diferentes actuadores para diferentes comportamientos; por ejemplo, evitar escribir un solo actuador que implemente todos los comportamientos personalizados. Esto hará que sea más fácil de entender y reutilizar a largo plazo.
* Utilice sólo métodos y atributos públicos, por ejemplo, apéguese a métodos como *obstacles* o *interactee*. Esto hará que sea menos probable que los actuadores se rompan en el futuro.
