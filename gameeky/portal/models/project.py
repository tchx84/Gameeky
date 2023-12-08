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
