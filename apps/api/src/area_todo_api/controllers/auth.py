from fastapi import APIRouter, Depends, status

from area_todo_api.dependencies import get_auth_service, get_current_principal
from area_todo_api.schemas.auth import (
    AuthCredentials,
    MeResponse,
    TokenResponse,
)
from area_todo_api.services.auth_service import AuthService, AuthenticatedPrincipal

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(
    payload: AuthCredentials,
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return service.register(payload)


@router.post("/login", response_model=TokenResponse)
def login(
    payload: AuthCredentials,
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return service.login(payload)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    principal: AuthenticatedPrincipal = Depends(get_current_principal),
    service: AuthService = Depends(get_auth_service),
) -> None:
    service.logout(principal)


@router.get("/me", response_model=MeResponse)
def me(
    principal: AuthenticatedPrincipal = Depends(get_current_principal),
    service: AuthService = Depends(get_auth_service),
) -> MeResponse:
    return service.me(principal)
