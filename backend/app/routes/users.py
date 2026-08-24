from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database.mongodb import database
from app.core.security import require_admin


router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


# Get All Users - Admin Only
@router.get("/")
async def get_all_users(
    current_user: dict = Depends(require_admin)
):

    users = []

    async for user in database.users.find():

        users.append({
            "user_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        })

    return users


# Get Single User - Admin Only
@router.get("/{user_id}")
async def get_user(
    user_id: str,
    current_user: dict = Depends(require_admin)
):

    try:
        user = await database.users.find_one(
            {"_id": ObjectId(user_id)}
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "user_id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"]
    }


# Delete User - Admin Only
@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(require_admin)
):

    try:
        object_id = ObjectId(user_id)

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    # Prevent admin from deleting themselves
    if user_id == current_user["user_id"]:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete your own account"
        )

    result = await database.users.delete_one(
        {"_id": object_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully",
        "user_id": user_id
    }