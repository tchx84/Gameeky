from gettext import gettext as _

from .base_row import BaseRow


class DayTimeRow(BaseRow):
    __gtype_name__ = "DayTimeRowModel"

    __items__ = {
        "dynamic": _("Dynamic"),
        "day": _("Day"),
        "night": _("Night"),
    }
