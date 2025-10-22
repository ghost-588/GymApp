from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.exceptions.exceptions import (
    AlreadyExistsError,
    BusinessRuleError,
    InvalidCredentials,
    InvalidToken,
    NotAuthorizedError,
    NotFoundError,
)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"detail": exc.message})

    @app.exception_handler(AlreadyExistsError)
    async def already_exists_handler(request: Request, exc: AlreadyExistsError):
        return JSONResponse(status_code=400, content={"detail": exc.message})

    @app.exception_handler(ValidationError)
    async def validation_error(request: Request, exc: ValidationError):
        return JSONResponse(status_code=422, content={"detail": exc.message})

    @app.exception_handler(BusinessRuleError)
    async def business_rule_error(request: Request, exc: BusinessRuleError):
        return JSONResponse(status_code=422, content={"detail": exc.message})

    @app.exception_handler(NotAuthorizedError)
    async def not_authorized_error(requset: Request, exc: NotAuthorizedError):
        return JSONResponse(status_code=403, content={"detail": exc.message})

    @app.exception_handler(InvalidToken)
    async def invalid_token_error(request: Request, exc: InvalidToken):
        return JSONResponse(status_code=401, content={"detail": exc.message})

    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials_error(request: Request, exc: InvalidCredentials):
        return JSONResponse(status_code=400, content={"detail": exc.message})
