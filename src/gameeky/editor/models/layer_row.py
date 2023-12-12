from gettext import gettext as _

from .base_row import BaseRow


class LayerRow(BaseRow):
    __gtype_name__ = "LayerRowModel"

    __items__ = {
        "layer 0": _("Layer 0"),
        "layer 1": _("Layer 1"),
        "layer 2": _("Layer 2"),
        "layer 3": _("Layer 3"),
        "layer 4": _("Layer 4"),
        "layer 5": _("Layer 5"),
        "layer 6": _("Layer 6"),
        "layer 7": _("Layer 7"),
        "all layers": _("All Layers"),
    }
