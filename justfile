default:
    @just --list

# アプリ起動
start:
    uv run uvicorn app.main:app --reload

# 依存パッケージのインストール
sync:
    uv sync

# .env ファイルの初期セットアップ
setup-env:
    cp .env.example .env

# pre-commit フックのインストール
setup-hooks:
    uv run pre-commit install

# 初回セットアップ（sync + hooks）
setup: sync setup-hooks

# --- Lint ---

# lint チェック
lint:
    uv run ruff check .

# lint 自動修正
lint-fix:
    uv run ruff check . --fix

# --- Format ---

# フォーマットチェック（変更なし）
format-check:
    uv run ruff format . --check

# フォーマット適用
format:
    uv run ruff format .

# lint + format をまとめて修正
fix: lint-fix format

# lint + format チェックをまとめて実行
check: lint format-check

# --- Docker ---

# DB（PostgreSQL）起動
db-start:
    docker compose up -d

# DB 停止
db-stop:
    docker compose down

# DB ログ確認
db-logs:
    docker compose logs -f db
