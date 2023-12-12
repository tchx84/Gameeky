from gettext import gettext as _

from .base_row import BaseRow


class StateRow(BaseRow):
    __gtype_name__ = "StateRowModel"

    __items__ = {
        "destroyed": _("Destroyed"),
        "destroying": _("Destroying"),
        "dropping": _("Dropping"),
        "exhausted": _("Exhausted"),
        "held": _("Held"),
        "idling": _("Idling"),
        "interacting": _("Interacting"),
        "moving": _("Moving"),
        "taking": _("Taking"),
        "using": _("Using"),
    }
