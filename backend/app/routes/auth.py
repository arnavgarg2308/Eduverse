from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bson import ObjectId

from app.schemas.auth import (
    UserRegister,
    UserLogin,
    UserProfileUpdate,
    ChangePassword
)
from app.database.mongodb import database

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

security = HTTPBearer()


# Register API
@router.post("/register")
async def register_user(user: UserRegister):

    existing_user = await database.users.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    new_user = {
        "name": user.name,
        "email": user.email,
        "password_hash": hashed_password,
        "role": user.role
    }

    result = await database.users.insert_one(new_user)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
        "name": user.name,
        "email": user.email,
        "role": user.role
    }


# Login API
@router.post("/login")
async def login_user(user: UserLogin):

    existing_user = await database.users.find_one(
        {"email": user.email}
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_correct = verify_password(
        user.password,
        existing_user["password_hash"]
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "user_id": str(existing_user["_id"]),
            "email": existing_user["email"],
            "role": existing_user["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": existing_user["role"]
    }


# Get Current User API
@router.get("/me")
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = await database.users.find_one(
        {"email": payload["email"]}
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

# Update Current User Profile
@router.put("/me")
async def update_current_user(
    updated_data: UserProfileUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    update_data = updated_data.model_dump(
        exclude_none=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No data provided for update"
        )

    # If email is being changed, check duplicate email
    if "email" in update_data:

        existing_user = await database.users.find_one(
            {
                "email": update_data["email"],
                "_id": {"$ne": ObjectId(payload["user_id"])}
            }
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

    try:
        result = await database.users.update_one(
            {
                "_id": ObjectId(payload["user_id"])
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

    updated_user = await database.users.find_one(
        {
            "_id": ObjectId(payload["user_id"])
        }
    )

    return {
        "message": "Profile updated successfully",
        "user_id": str(updated_user["_id"]),
        "name": updated_user["name"],
        "email": updated_user["email"],
        "role": updated_user["role"]
    }

# Change Password API
@router.put("/change-password")
async def change_password(
    password_data: ChangePassword,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    try:
        user = await database.users.find_one(
            {
                "_id": ObjectId(payload["user_id"])
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

    # Check current password
    password_correct = verify_password(
        password_data.current_password,
        user["password_hash"]
    )

    if not password_correct:
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    # Hash new password
    new_password_hash = hash_password(
        password_data.new_password
    )

    await database.users.update_one(
        {
            "_id": user["_id"]
        },
        {
            "$set": {
                "password_hash": new_password_hash
            }
        }
    )

    return {
        "message": "Password changed successfully"
    }