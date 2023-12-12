from gettext import gettext as _

from .base_row import BaseRow


class AreaRow(BaseRow):
    __gtype_name__ = "AreaRowModel"

    __items__ = {
        "1x1": _("1x1"),
        "3x3": _("3x3"),
        "5x5": _("5x5"),
        "7x7": _("7x7"),
        "9x9": _("9x9"),
    }
