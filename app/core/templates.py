from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.core.config import settings

templates = Jinja2Templates(directory=str(settings.templates_dir))
static_files = StaticFiles(directory=str(settings.static_dir))
