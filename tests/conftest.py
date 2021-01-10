import os
from pathlib import Path
from typing import Dict

import mlflow
import pytest
import toml
import yaml


@pytest.fixture(autouse=True)
def cleanup_mlflow_after_runs():
    # A test function will be run at this point
    yield
    while mlflow.active_run():
        mlflow.end_run()


def _write_yaml(filepath: Path, config: Dict):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    yaml_str = yaml.dump(config)
    filepath.write_text(yaml_str)


def _write_toml(filepath: Path, config: Dict):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    toml_str = toml.dumps(config)
    filepath.write_text(toml_str)


def _get_local_logging_config():
    return {
        "version": 1,
        "formatters": {
            "simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
        },
        "root": {"level": "ERROR", "handlers": ["console"]},
        "loggers": {
            "kedro": {"level": "ERROR", "handlers": ["console"], "propagate": False}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "ERROR",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            }
        },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "simple",
            "filename": "logs/info.log",
        },
    }


@pytest.fixture
def config_dir(tmp_path):
    """This emulates the root of a kedro project.
    This function must be called before any instantiation of DummyContext

    """
    for env in ["base", "local"]:
        catalog = tmp_path / "conf" / env / "catalog.yml"
        credentials = tmp_path / "conf" / env / "credentials.yml"
        logging = tmp_path / "conf" / env / "logging.yml"
        parameters = tmp_path / "conf" / env / "parameters.yml"
        globals_yaml = tmp_path / "conf" / env / "globals.yml"
        pyproject_toml = tmp_path / "pyproject.toml"
        _write_yaml(catalog, dict())
        _write_yaml(parameters, dict())
        _write_yaml(globals_yaml, dict())
        _write_yaml(credentials, dict())
        _write_yaml(logging, _get_local_logging_config()),

    _write_toml(
        pyproject_toml,
        {
            "tool": {
                "kedro": {
                    "package_name": "dummy_package",
                    "project_name": "dummy_package",
                    "project_version": "0.17.0",
                }
            }
        },
    )

    os.mkdir(tmp_path / "src")
    os.mkdir(tmp_path / "src" / "dummy_package")
    with open(tmp_path / "src" / "dummy_package" / "run.py", "w") as f:
        f.writelines(
            [
                "from pathlib import Path\n",
                "from kedro.framework.session import KedroSession\n",
                "def run_package():\n",
                "    package_name = Path(__file__).resolve().parent.name\n",
                "    with KedroSession.create(package_name) as session:\n",
                "        session.run()\n",
                "if __name__ == '__main__':",
                "    run_package()",
            ]
        )
