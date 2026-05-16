# Than-thong Runtime Checklist

## 1. Cài plugin guard từ local path
```powershell
openclaw plugins install E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\runtime-guard\than-thong-guard
```

## 2. Bật internal hooks broad discovery qua config
Cần thêm `hooks.internal.enabled=true` và `hooks.internal.load.extraDirs` trỏ tới:
- `E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\managed-hooks`

Nếu dùng CLI config one-liner được:
```powershell
openclaw config set hooks.internal.enabled true
openclaw config set hooks.internal.load.extraDirs '["E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\managed-hooks"]' --strict-json
```

## 3. Kiểm tra hooks đã thấy chưa
```powershell
openclaw hooks list
```
Kỳ vọng có:
- `than-thong-bootstrap`
- `than-thong-command-guard`

## 4. Kiểm tra plugin guard
```powershell
openclaw status
```
Sau đó test một đường bị chặn qua runtime nếu có bề mặt phù hợp.

## 5. Nếu config CLI không ăn
Dùng Control UI / config editor để thêm:
```json5
{
  hooks: {
    internal: {
      enabled: true,
      load: {
        extraDirs: [
          "E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\managed-hooks"
        ]
      }
    }
  },
  plugins: {
    entries: {
      "than-thong-guard": {
        enabled: true
      }
    }
  }
}
```
