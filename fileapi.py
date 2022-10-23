from pathlib import Path

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()


class PathDto(BaseModel):
    path: str


@app.post("/ls/")
async def ls(path_dto: PathDto, response: Response):
    print(path_dto)
    dir_path = Path(path_dto.path)

    if not dir_path.is_absolute():
        dir_path = Path.home() / dir_path
    if not dir_path.is_dir():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'{dir_path} is not a directory'}

    return [{'path': p, 'is_dir': p.is_dir()} for p in dir_path.iterdir()]
