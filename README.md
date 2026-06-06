# fastapi-no-sekai

FastAPI + SQLAlchemy + PostgreSQL で構築した Web API です。

## 必要な環境

- Python 3.14+
- PostgreSQL

## インストール

### Python 3.14+

**Mac**
```bash
brew install python@3.14
```

**Windows**
[python.org](https://www.python.org/downloads/) からインストーラーをダウンロードして実行してください。

---

### uv（パッケージマネージャー）

**Mac**
```bash
brew install uv
```

**Windows**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

### PostgreSQL

**Mac**
```bash
brew install postgresql@16
brew services start postgresql@16
```

**Windows**
[postgresql.org](https://www.postgresql.org/download/windows/) からインストーラーをダウンロードして実行してください。

---

## セットアップ

### 1. 依存パッケージのインストール

```bash
uv sync
```

### 2. 環境変数の設定

`.env.example` をコピーして `.env` を作成し、DB 接続情報を設定してください。

```bash
cp .env.example .env
```

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password

APP_TIMEZONE=Asia/Tokyo
```

## App の起動

```bash
uvicorn app.main:app --reload
```

起動後、以下の URL にアクセスできます。

| URL | 内容 |
|---|---|
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/redoc | ReDoc |

## 開発コマンド

### リントとフォーマット

```bash
# チェックのみ
uv run ruff check .

# 自動修正
uv run ruff check . --fix

# フォーマット
uv run ruff format .
```

### pre-commit の設定

```bash
uv run pre-commit install
```
