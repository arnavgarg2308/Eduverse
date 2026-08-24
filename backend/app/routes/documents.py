from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    UploadFile,
    File
)
from app.services.edumorph_service import send_pdf_to_edumorph
from bson import ObjectId
from datetime import datetime

from app.database.mongodb import (
    database,
    gridfs_bucket
)

from app.core.security import get_current_user

from app.schemas.document import (
    DocumentCreate,
    DocumentUpdate
)

from app.services.pdf_service import extract_text_from_pdf


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


# ==========================================
# Upload PDF and Extract Text
# ==========================================

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):

    # Check file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Read PDF file
    file_data = await file.read()
    try:
      edumorph_analysis = await send_pdf_to_edumorph(
        filename=file.filename,
        file_data=file_data
    )

    except Exception as e:
       raise HTTPException(
        status_code=500,
        detail=f"EduMorph analysis failed: {str(e)}"
         )

    # Check empty file
    if not file_data:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # Extract text from PDF
    try:
        extracted_text = extract_text_from_pdf(
            file_data
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    # Store original PDF in GridFS
    file_id = await gridfs_bucket.upload_from_stream(
        file.filename,
        file_data,
        metadata={
            "user_id": current_user["user_id"],
            "content_type": file.content_type,
            "uploaded_at": datetime.utcnow()
        }
    )

    # Save document metadata and extracted text
    document_data = {
    "user_id": current_user["user_id"],
    "filename": file.filename,
    "content_type": file.content_type,
    "file_id": str(file_id),
    "extracted_text": extracted_text,
    "analysis": edumorph_analysis,
    "uploaded_at": datetime.utcnow(),
    "status": "uploaded"
}

    result = await database.documents.insert_one(
        document_data
    )

    return {
        "message": "PDF uploaded and processed successfully",
        "document_id": str(result.inserted_id),
        "file_id": str(file_id),
        "filename": file.filename,
        "text_length": len(extracted_text),
        "status": "uploaded"
    }


# ==========================================
# Create Document
# ==========================================

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


# ==========================================
# Get Current User Documents
# ==========================================

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

        document["document_id"] = str(
            document["_id"]
        )

        del document["_id"]

        documents.append(document)

    return documents


# ==========================================
# Get Single Document
# ==========================================

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

    document["document_id"] = str(
        document["_id"]
    )

    del document["_id"]

    return document


# ==========================================
# Update Document
# ==========================================

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


# ==========================================
# Delete Document
# ==========================================

@router.delete("/{document_id}")
async def delete_document(
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

    await database.documents.delete_one(
        {
            "_id": ObjectId(document_id),
            "user_id": current_user["user_id"]
        }
    )

    return {
        "message": "Document deleted successfully"
    }