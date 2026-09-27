from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException, UnauthorizedException, NotFoundException
from app.core.security import get_password_hash, verify_password, create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.models.user import User


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register_user(self, user_in: UserCreate) -> UserResponse:
        existing = self.repo.get_by_email(user_in.email)
        if existing:
            raise BadRequestException("User with this email already exists")

        hashed_pw = get_password_hash(user_in.password)
        user = self.repo.create(user_in, hashed_pw)
        return UserResponse.model_validate(user)

    def authenticate_user(self, credentials: UserLogin) -> Token:
        user = self.repo.get_by_email(credentials.email)
        if not user:
            raise UnauthorizedException("Invalid email or password")

        if not verify_password(credentials.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")

        token_str = create_access_token(subject=user.id)
        return Token(
            access_token=token_str,
            token_type="bearer",
            user_id=user.id,
            role=user.role
        )

    def get_user_by_id(self, user_id: str) -> UserResponse:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserResponse.model_validate(user)
