import os
from pathlib import Path
from distutils.util import strtobool

import supervisely as sly
from dotenv import load_dotenv


if sly.is_development():
    load_dotenv("local.env")
    load_dotenv("debug.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api: sly.Api = sly.Api.from_env()

TASK_ID = sly.env.task_id()
TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()

PROJECT_ID = sly.env.project_id(raise_not_found=False)
DATASET_ID = sly.env.dataset_id(raise_not_found=False)

INPUT_PATH = os.environ.get("modal.state.files", None)
if INPUT_PATH is None or INPUT_PATH == "":
    INPUT_PATH = os.environ.get("modal.state.slyFolder")
IS_ON_AGENT = api.file.is_on_agent(INPUT_PATH)

REMOVE_SOURCE = bool(strtobool(os.getenv("modal.state.remove_source", "False")))
OUTPUT_PROJECT_NAME = os.environ.get("modal.state.project_name", "")
DPI = int(os.environ.get("model.state.dpi", 300))

DEFAULT_DATASET_NAME = "ds0"

STORAGE_DIR = sly.app.get_data_dir()
CONVERTED_LOCAL_DIR = Path(STORAGE_DIR) / "results"