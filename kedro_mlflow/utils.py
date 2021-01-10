from pathlib import Path
from typing import Union


def _validate_project_path(project_path: Union[str, Path, None] = None) -> Path:
    project_path = Path(project_path or Path.cwd())
    return project_path


def _already_updated(project_path: Union[str, Path, None] = None) -> bool:
    project_path = _validate_project_path(project_path)
    # TODO: add a better check
    flag = (project_path / "conf" / "base" / "mlflow.yml").is_file()
    return flag


def _parse_requirements(path, encoding="utf-8"):
    with open(path, mode="r", encoding=encoding) as file_handler:
        requirements = [
            x.strip() for x in file_handler if x.strip() and not x.startswith("-r")
        ]
    return requirements


class KedroContextError(Exception):
    """Error occurred when loading project and running context pipeline."""
