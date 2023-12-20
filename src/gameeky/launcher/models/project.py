# Copyright (c) 2023 Martín Abente Lahaye.
#
# This file is part of Gameeky
# (see gameeky.tchx84.dev).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import shutil

from ...common.scanner import Description
from ...common.utils import get_projects_path


class Project:
    @classmethod
    def write(cls, path: str, description: Description) -> None:
        with open(os.path.join(path, "gameeky.project"), "w") as file:
            file.write(description.to_json())

    @classmethod
    def create(cls, description: Description) -> None:
        project_path = os.path.join(get_projects_path(), description.name)

        os.makedirs(os.path.join(project_path, "actuators"))
        os.makedirs(os.path.join(project_path, "assets"))
        os.makedirs(os.path.join(project_path, "entities"))
        os.makedirs(os.path.join(project_path, "scenes"))

        cls.write(project_path, description)

    @classmethod
    def rename(cls, old: Description, new: Description) -> None:
        projects_path = get_projects_path()

        old_project_path = os.path.join(projects_path, old.name)
        new_project_path = os.path.join(projects_path, new.name)

        os.rename(old_project_path, new_project_path)
        cls.write(new_project_path, new)

    @classmethod
    def remove(cls, description: Description) -> None:
        project_path = os.path.join(get_projects_path(), description.name)
        shutil.rmtree(project_path)
