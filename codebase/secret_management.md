# Secret Management

## Không push API keys

API keys phải để trong file `.env` local và không commit lên git.

File `.gitignore` đã chặn:

```text
.env
.env.*
*.pem
*.key
*.secret
secrets/
```

File `.env.example` được phép commit vì chỉ chứa placeholder.

## Cách setup local

Copy file mẫu:

```bash
cp .env.example .env
```

Sau đó điền key thật vào `.env`:

```text
OPENROUTER_API_KEY=key_that_should_not_be_committed
OPENROUTER_MODEL=model_name
```

## Nếu `.env` đã bị git track

Chạy lệnh này một lần:

```bash
git rm --cached .env
```

Sau đó commit lại:

```bash
git add .gitignore .env.example secret_management.md
git commit -m "Hide local secrets from git"
```

## Nếu GitHub báo secret scanning

Nếu key thật đã từng bị commit, hãy:

1. Revoke key cũ trên provider.
2. Tạo key mới.
3. Cập nhật key mới trong `.env`.
4. Không dùng lại key đã lộ.

Nếu secret nằm trong commit history, cần xoá khỏi history bằng công cụ như `git filter-repo` hoặc tạo repo/branch sạch tuỳ tình huống.
