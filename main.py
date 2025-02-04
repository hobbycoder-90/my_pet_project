from fastapi import FastAPI, status, Request
import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.bookings.router import router as bookings_router
from app.users.router import router as users_router
from app.auth.router import router as auth_router
from app.hotels.router import router as hotels_router
from app.rooms.router import router as rooms_router

from app.pages.router import router as router_pages


app = FastAPI(
    title="FastAPI PetProject Bookings Hotel",
    version="0.1",
    description="This is a very fancy project, with auto docs for the API and everything",
)

# Благодаря этой функции клиент видит ошибки, происходящие на сервере, вместо "Internal server error"
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)

app.include_router(router_pages)



if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
    ) 


"fastapi dev main.py"