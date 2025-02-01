from fastapi import HTTPException, status

# Bookings exceptions

BookingNotFoundExeption = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Booking not found",
)


# Hotels exceptions
HotelNotFoundExeption = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Hotel not found",
)

HotelAlreadyExistsExeption = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Hotel already exists",
)


# Rooms exceptions
RoomNotFoundExeption = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Room not found",
)

RoomAlreadyExistsExeption = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Room already exists",
)


# Users exceptions

UserNotFoundExeption = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)

UserAlreadyExistsExeption = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists",
)

UserLogoutPlsExeption = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Logout please!",
)

UserInactiveException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Inactive user",
)

UserPasswordIncorrectExeption = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Password incorrect",
)


# Auth exceptions
TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token exp is not in token or token is expired"
)


IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect token format. Please login again"
)

TokenIsNotFound = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is not found"
)

UserUnauthorizedExeption = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password"
)

UserIDIsNotInTokenJWTException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User id is not in token",
)