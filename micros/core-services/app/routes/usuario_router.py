from fastapi import APIRouter, Response, Request, Query
from ..controllers.usuario_controller import UserController
from ..models.usuario_model import CreateUserModel, UpdateUserModel
from ..models.paginator_model import PaginatorSearch


router = APIRouter()


@router.post("/createUser", summary="Create a user")
async def create_user(request: Request, user: CreateUserModel, response: Response):
    client_ip = request.client.host
    res = await UserController().create_user(client_ip,user)
    if res:
        response.status_code = 200
    else:
        response.status_code = 404
    return res

@router.get("/getUserById", summary="Get user by id")
async def get_user_by_id(response: Response, id_usuario: str):
    res = await UserController().get_user_by_id(id_usuario)
    if res:
        response.status_code = 200
    else:
        response.status_code = 400
    return res



@router.delete("/deleteUser", summary="Delete user")
async def delete_user(response: Response, id_usuario: str = Query(..., description="ID del usuario a eliminar")):
    res = await UserController().delete_user(id_usuario)
    if res:
        response.status_code = 200
    else:
        response.status_code = 400
    return res


@router.put("/updateUser", summary="Update user")
async def update_user(id_usuario: str, user: UpdateUserModel, response: Response):
    res = await UserController().update_user(id_usuario, user)
    if res:
        response.status_code = 200
    else:
        response.status_code = 400
    return res
