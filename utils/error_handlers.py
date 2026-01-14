from fastapi import Request
from starlette import status
from fastapi.responses import JSONResponse
from utils.domain_error import (PermissionDenied, 
                                NotFoundError, 
                                DatabaseError,
                                NotAuthenticatedUser, 
                                BadRequest)
from utils.logger import logger


async def permission_denied_handler(request:Request, exc:PermissionDenied):
    logger.warning(f"Permission denied: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"error":"permission denied", "detail":exc.detail},
    )


async def not_found_handler(request:Request, exc:NotFoundError):
    logger.info(f"Not found: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error":"not found", "detail":exc.detail},
    )


async def database_error_handler(request:Request, exc:DatabaseError):
    logger.error(f"Database error: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error":"database error", "detail":exc.detail},
    )

async def bad_request(request:Request, exc:BadRequest):
    logger.warning(f"Bad request: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "bad request", "detail":exc.detail},
    )

async def not_authenticated_user(request:Request, exc:NotAuthenticatedUser):
    logger.warning(f"Bad request: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "bad request", "detail":exc.detail},
    )