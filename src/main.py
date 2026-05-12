from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.routes import movie_router, accounts_router

app = FastAPI(title="Movies homework", description="Description of project")

api_version_prefix = "/api/v1"

app.include_router(
    accounts_router, prefix=f"{api_version_prefix}/accounts", tags=["accounts"]
)
app.include_router(
    movie_router, prefix=f"{api_version_prefix}/theater", tags=["theater"]
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Берем первую ошибку из списка
    err = exc.errors()[0]
    # Убираем префикс "Value error, " если он есть
    msg = err.get("msg").replace("Value error, ", "")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": msg
        },  # Тесты часто ожидают строку в detail или определенный формат
    )
