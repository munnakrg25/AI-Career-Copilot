import os
import re
import uuid

from fastapi import HTTPException, UploadFile

# 10 MB limit for resume uploads
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

# PDF magic bytes: every valid PDF starts with %PDF-
PDF_MAGIC = b"%PDF-"


def _safe_filename(original: str) -> str:
    """
    Return a safe, server-generated filename that:
    - Strips any directory components (prevents path traversal)
    - Keeps only alphanumeric characters, hyphens, underscores, and dots
    - Preserves the .pdf extension
    - Prepends a UUID so concurrent uploads never collide
    """
    # Strip all directory separators (handles both / and \ and ../)
    basename = os.path.basename(original.replace("\\", "/"))

    # Keep only safe characters in the stem
    stem, _, ext = basename.rpartition(".")
    safe_stem = re.sub(r"[^\w\-]", "_", stem)[:64] or "resume"
    safe_ext = ext.lower()[:8]

    return f"{uuid.uuid4().hex}_{safe_stem}.{safe_ext}"


async def validate_and_save_resume(file: UploadFile, upload_dir: str) -> str:
    """
    Validate an uploaded resume file and save it safely.

    Checks (in order):
    1. File extension must be .pdf
    2. File size must not exceed MAX_FILE_SIZE_BYTES
    3. File content must start with the PDF magic bytes (%PDF-)

    Returns the absolute path of the saved file.
    Raises HTTPException 400 for all validation failures.
    """

    # --- 1. Extension check ---
    original_name = file.filename or ""
    if not original_name.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF resumes are accepted."
        )

    # --- 2. Read file into memory with size guard ---
    # Read one byte beyond the limit so we can detect oversized files
    # without loading the whole file.
    chunks = []
    total_bytes = 0

    while True:
        chunk = await file.read(65536)  # 64 KB chunks
        if not chunk:
            break
        total_bytes += len(chunk)
        if total_bytes > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=(
                    f"File too large. Maximum allowed size is "
                    f"{MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB."
                )
            )
        chunks.append(chunk)

    content = b"".join(chunks)

    # --- 3. PDF magic bytes check ---
    if not content.startswith(PDF_MAGIC):
        raise HTTPException(
            status_code=400,
            detail="Invalid file content. The uploaded file is not a valid PDF."
        )

    # --- 4. Save with a safe server-generated filename ---
    os.makedirs(upload_dir, exist_ok=True)
    safe_name = _safe_filename(original_name)
    file_path = os.path.join(upload_dir, safe_name)

    with open(file_path, "wb") as f:
        f.write(content)

    return file_path
