from fastapi.testclient import TestClient


class TestCreateArtist:
    def test_有効なアーティスト情報でPOSTすると201が返る(self, client: TestClient):
        response = client.post(
            "/artists",
            json={"artist_name": "Leo/need", "unit_name": "Leo/need"},
        )

        assert response.status_code == 201
        body = response.json()
        assert body["artist_name"] == "Leo/need"
        assert body["unit_name"] == "Leo/need"
        assert isinstance(body["id"], int)
        assert "meta_info" in body

    def test_ユニット名を省略してPOSTすると201が返る(self, client: TestClient):
        response = client.post("/artists", json={"artist_name": "MEIKO"})

        assert response.status_code == 201
        assert response.json()["unit_name"] is None

    def test_アーティスト名が空文字のとき400が返る(self, client: TestClient):
        response = client.post("/artists", json={"artist_name": ""})

        assert response.status_code == 400
        body = response.json()
        assert body["code"] == "NAME_REQUIRED"

    def test_アーティスト名が未指定のとき422が返る(self, client: TestClient):
        response = client.post("/artists", json={"unit_name": "Leo/need"})

        assert response.status_code == 422

    def test_アーティスト名が50文字超のとき422が返る(self, client: TestClient):
        response = client.post("/artists", json={"artist_name": "a" * 51})

        assert response.status_code == 422

    def test_アーティスト名が重複のとき409が返る(self, client: TestClient):
        client.post("/artists", json={"artist_name": "Leo/need"})

        response = client.post("/artists", json={"artist_name": "Leo/need"})

        assert response.status_code == 409
        body = response.json()
        assert body["code"] == "DUPLICATE_NAME"
