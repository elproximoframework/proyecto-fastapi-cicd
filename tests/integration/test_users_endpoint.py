import pytest
from httpx import AsyncClient


class TestUsersEndpoint:
    @pytest.mark.asyncio
    async def test_create_user_success(self, client: AsyncClient, user_payload):
        # 1. Registrar usuario
        response = await client.post("/api/v1/users/", json=user_payload)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_payload["email"]
        assert "password" not in data  # La contraseña nunca debe ser expuesta
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, client: AsyncClient, user_payload):
        # 1. Primer registro exitoso
        await client.post("/api/v1/users/", json=user_payload)
        
        # 2. Intentar registrar el mismo email de nuevo
        response = await client.post("/api/v1/users/", json=user_payload)
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_get_users_requires_auth(self, client: AsyncClient):
        # Intentar acceder a listado sin token JWT de portador
        response = await client.get("/api/v1/users/")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_full_auth_flow(self, client: AsyncClient, user_payload):
        # 1. Registrar usuario
        reg_response = await client.post("/api/v1/users/", json=user_payload)
        assert reg_response.status_code == 201

        # 2. Iniciar sesión para obtener el JWT token
        login_response = await client.post("/api/v1/auth/token", data={
            "username": user_payload["email"],
            "password": user_payload["password"],
        })
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        token = token_data["access_token"]

        # 3. Acceder al recurso protegido /me usando el token JWT
        me_response = await client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        assert me_response.json()["email"] == user_payload["email"]
