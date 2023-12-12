from gettext import gettext as _

from .base_row import BaseRow


class DirectionRow(BaseRow):
    __gtype_name__ = "DirectionRowModel"

    __items__ = {
        "east": _("East"),
        "north": _("North"),
        "south": _("South"),
        "west": _("West"),
    }
