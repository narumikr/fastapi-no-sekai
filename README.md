<img src="https://capsule-render.vercel.app/api?type=waving&height=250&color=0:ddaacc,100:ffc096&text=Hello%20SEKAI&fontAlign=45&fontAlignY=40&fontSize=50&animation=fadeIn&desc=FastAPI%20Template%20Repo&descAlign=65&descAlignY=55&fontColor=f5f5f7&descSize=-1&reversal=true&section=header&textBg=false" />

# **_Fast API no SEKAI_**

![welcome comment](https://readme-typing-svg.herokuapp.com?color=%23ff6699&width=500&lines=Hello+there!!+Thanks+for+stopping+by+🎵;Welcome+to+my+SEKAI+💫;)

FastAPIのプロジェクト開始テンプレートリポジトリ

#### **_Tech Stack_**

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white)](#)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?logo=Pydantic&logoColor=white)](#)
[![Pytest](https://img.shields.io/badge/Pytest-fff?logo=pytest&logoColor=000)](#)
[![Postgres](https://img.shields.io/badge/Postgres-%23316192.svg?logo=postgresql&logoColor=white)](#)
[![Swagger](https://img.shields.io/badge/Swagger-85EA2D?logo=swagger&logoColor=173647)](#)

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

### 1. just のインストール

**Mac**
```bash
brew install just
```

**Windows**
```powershell
winget install Casey.Just
```

---

### 2. 依存パッケージのインストール

```bash
# just コマンドで実行できます
just sync

# または直接 uv で実行
uv sync
```

---

### 3. 環境変数の設定

`.env.example` をコピーして `.env` を作成し、DB 接続情報を設定してください。

```bash
# just コマンドでも実行できます
just setup-env

# または手動で
cp .env.example .env
```

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password

APP_TIMEZONE=UTC
```

---

## App の起動

```bash
just start
```

起動後、以下の URL にアクセスできます。

| URL | 内容 |
|---|---|
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/redoc | ReDoc |

## 開発コマンド

| コマンド | 内容 |
|---|---|
| `just sync` | 依存パッケージのインストール |
| `just setup` | 初回セットアップ（sync + pre-commit hooks） |
| `just start` | アプリ起動 |
| `just lint` | lint チェック |
| `just lint-fix` | lint 自動修正 |
| `just format` | フォーマット適用 |
| `just format-check` | フォーマットチェック（変更なし） |
| `just fix` | lint 修正 + フォーマット適用 |
| `just check` | lint + フォーマットチェック |
| `just db-start` | DB（Docker）起動 |
| `just db-stop` | DB（Docker）停止 |
| `just db-logs` | DB ログ確認 |
