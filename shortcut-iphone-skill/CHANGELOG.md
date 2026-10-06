# Changelog

## 1.1.0 — 2026-10-06
- Thêm `bin/validate-shortcut`: kiểm tra hard rules (UUID viết hoa/duy nhất,
  Magic Variable trỏ đúng, grouping cân bằng, mã WFCondition chuẩn).
- Thêm test suite 10 tests + CI workflow (GitHub Actions).
- Thêm `templates/` (minimal, menu-driven, http-api) đã validate.
- Thêm cách ký thứ 3: shortcut "Sign Shortcut File" trên iPhone.
- Sửa claim sai: tool compile KHÔNG tự sinh UUID — agent phải tự sinh.
- Ghi chú `--no-sign` trên Linux (compile mặc định ký và thoát lỗi dù file vẫn ghi).

## 1.0.0 — 2026-10-06
- Bản đầu: quy trình 7 bước, 7 file references (35 pattern, bảng action,
  control flow, URL schemes, ký & phát hành, kỹ thuật nâng cao, debug),
  tool shortcut-cli vendored, install.sh đa agent.
- Kiến thức từ: 6 shortcut phimtat.vn dịch ngược, RoutineHub, r/shortcuts,
  MacStories, tài liệu Apple iOS 26.
