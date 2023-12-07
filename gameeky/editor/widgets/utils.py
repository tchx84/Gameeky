from typing import Optional

from gi.repository import Gtk


def get_position_in_model(model: Gtk.StringList, value: str) -> Optional[int]:
    for index, row in enumerate(list(model)):
        if row.props.string == value:
            return index

    return None
