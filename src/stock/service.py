from src.database.models import UserTable
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status


async def user_registration(payload=None, db=None):
    data = UserTable(username=payload.password, password=payload.password)
    existed_data = (
        db.query(UserTable)
        .filter(
            UserTable.username == payload.username
            and UserTable.password == payload.password
        )
        .first()
    )
    if existed_data:
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="User existed")
    try:
        db.add(data)
        db.commit()
        db.refresh(data)
        return data, "Registration successfully"
    except:
        return {}, "Registration failed"


async def user_login(payload=None, db=None):
    try:
        data = (
            db.query(UserTable)
            .filter(
                UserTable.username == payload.username
                and UserTable.password == payload.password
            )
            .first()
        )
        return data, "Authencation successfully"
    except:
        return {}, "Authentication failed"
