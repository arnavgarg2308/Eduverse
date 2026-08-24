from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database.mongodb import database
from app.core.security import (
    get_current_user,
    verify_password,
    hash_password
)

from app.schemas.auth import (
    UserProfileUpdate,
    ChangePassword
)


router = APIRouter(
    prefix="/api/profile",
    tags=["Profile"]
)


# Get current user profile
@router.get("/")
async def get_profile(
    current_user: dict = Depends(get_current_user)
):

    try:
        user = await database.users.find_one(
            {
                "_id": ObjectId(
                    current_user["user_id"]
                )
            }
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
        "name": user.get("name"),
        "email": user.get("email"),
        "role": user.get("role")
    }


# Update current user profile
@router.put("/")
async def update_profile(
    updated_data: UserProfileUpdate,
    current_user: dict = Depends(get_current_user)
):

    update_data = updated_data.model_dump(
        exclude_none=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No data provided for update"
        )

    try:
        result = await database.users.update_one(
            {
                "_id": ObjectId(
                    current_user["user_id"]
                )
            },
            {
                "$set": update_data
            }
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "Profile updated successfully"
    }


# Change Password
@router.put("/change-password")
async def change_password(
    password_data: ChangePassword,
    current_user: dict = Depends(get_current_user)
):

    try:
        user = await database.users.find_one(
            {
                "_id": ObjectId(
                    current_user["user_id"]
                )
            }
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

    password_correct = verify_password(
        password_data.current_password,
        user["password_hash"]
    )

    if not password_correct:
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    hashed_new_password = hash_password(
        password_data.new_password
    )

    await database.users.update_one(
        {
            "_id": ObjectId(
                current_user["user_id"]
            )
        },
        {
            "$set": {
                "password_hash": hashed_new_password
            }
        }
    )

    return {
        "message": "Password changed successfully"
    }