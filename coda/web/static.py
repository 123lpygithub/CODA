"""Serve only the built workbench, alongside the local API."""
from pathlib import PurePosixPath

from starlette.exceptions import HTTPException
from starlette.staticfiles import StaticFiles


class WorkbenchFiles(StaticFiles):
    async def get_response(self, path, scope):
        parts = PurePosixPath(path).parts
        if (parts and parts[0] == "api") or any(part.startswith(".") for part in parts):
            raise HTTPException(status_code=404)
        response = await super().get_response(path, scope)
        if parts and parts[0] == "assets" and response.status_code == 200:
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        else:
            response.headers["Cache-Control"] = "no-cache"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response
