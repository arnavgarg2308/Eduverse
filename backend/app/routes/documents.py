from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database.mongodb import database
from app.core.security import get_current_user
from app.schemas.document import DocumentCreate, DocumentUpdate


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


# Create Document
@router.post("/")
async def create_document(
    document: DocumentCreate,
    current_user: dict = Depends(get_current_user)
):

    new_document = document.model_dump()

    new_document["user_id"] = current_user["user_id"]

    result = await database.documents.insert_one(
        new_document
    )

    return {
        "message": "Document created successfully",
        "document_id": str(result.inserted_id),
        "user_id": current_user["user_id"]
    }


# Get Current User Documents
@router.get("/")
async def get_all_documents(
    current_user: dict = Depends(get_current_user)
):

    documents = []

    async for document in database.documents.find(
        {
            "user_id": current_user["user_id"]
        }
    ):

        document["document_id"] = str(document["_id"])
        del document["_id"]

        documents.append(document)

    return documents


# Get Single Document
@router.get("/{document_id}")
async def get_document(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):

    try:
        document = await database.documents.find_one(
            {
                "_id": ObjectId(document_id),
                "user_id": current_user["user_id"]
            }
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid document ID"
        )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    document["document_id"] = str(document["_id"])
    del document["_id"]

    return document


# Update Document
@router.put("/{document_id}")
async def update_document(
    document_id: str,
    updated_data: DocumentUpdate,
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
        result = await database.documents.update_one(
            {
                "_id": ObjectId(document_id),
                "user_id": current_user["user_id"]
            },
            {
                "$set": update_data
            }
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid document ID"
        )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "message": "Document updated successfully"
    }


# Delete Document
@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):

    try:
        result = await database.documents.delete_one(
            {
                "_id": ObjectId(document_id),
                "user_id": current_user["user_id"]
            }
        )

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid document ID"
        )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "message": "Document deleted successfully"
    }