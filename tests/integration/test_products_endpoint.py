import pytest
from httpx import AsyncClient


class TestProductsEndpoint:
    @pytest.mark.asyncio
    async def test_apply_discount_percentage_out_of_bounds(self, client: AsyncClient):
        # 1. Intentar aplicar un descuento inválido del 150%
        response = await client.get("/api/v1/products/1/discount?percentage=150")
        assert response.status_code == 400
        assert "between 0 and 100" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_apply_discount_product_not_found(self, client: AsyncClient):
        # 1. Intentar aplicar descuento del 20% a un producto que no existe
        response = await client.get("/api/v1/products/999/discount?percentage=20")
        assert response.status_code == 404
        assert "product not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_apply_discount_success(self, client: AsyncClient, user_payload):
        # 1. Registrar usuario para poder crear el producto
        reg_response = await client.post("/api/v1/users/", json=user_payload)
        assert reg_response.status_code == 201

        # 2. Obtener token JWT de inicio de sesión
        login_response = await client.post(
            "/api/v1/auth/token",
            data={
                "username": user_payload["email"],
                "password": user_payload["password"],
            },
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # 3. Crear un producto de prueba
        product_payload = {
            "name": "Laptop de Test",
            "description": "Una laptop de prueba",
            "price": 1000.0,
            "stock": 5,
        }
        prod_response = await client.post(
            "/api/v1/products/",
            json=product_payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert prod_response.status_code == 201
        product_id = prod_response.json()["id"]

        # 4. Calcular descuento del 15% de forma pública
        discount_response = await client.get(
            f"/api/v1/products/{product_id}/discount?percentage=15"
        )
        assert discount_response.status_code == 200
        data = discount_response.json()
        assert data["product_id"] == product_id
        assert data["original_price"] == 1000.0
        assert data["discount_percentage"] == 15.0
        assert data["discount_amount"] == 150.0
        assert data["final_price"] == 850.0
