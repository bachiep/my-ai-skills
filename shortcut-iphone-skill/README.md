# Tạo phím tắt iPhone

[![test](https://github.com/bachiep/shortcut-iphone-skill/actions/workflows/test.yml/badge.svg)](https://github.com/bachiep/shortcut-iphone-skill/actions/workflows/test.yml)

Skill dành cho AI agent: thiết kế, dựng và phát hành phím tắt iPhone (`.shortcut`)
— từ phân tích shortcut có sẵn qua link iCloud, dựng file mới từ đặc tả, ký file,
đến đóng gói kèm hướng dẫn tiếng Việt theo phong cách [phimtat.vn](https://phimtat.vn).

## Cài đặt

**Cho agent (khuyên dùng):**

```bash
git clone https://github.com/bachiep/shortcut-iphone-skill.git
cd shortcut-iphone-skill
./install.sh   # tự phát hiện thư mục skill của agent trên máy rồi cài vào
```

Mỗi agent để skill một chỗ khác nhau (Claude Code: `~/.claude/skills/`,
Muse: `~/workspace/skills/`, ...) nên script sẽ tự tìm thay vì cài cứng một
đường dẫn. Muốn chỉ định tay: `./install.sh --target /đường/dẫn/tới/skill`.
Bản chất skill không phụ thuộc vị trí — chỉ cần copy nguyên thư mục
(`SKILL.md` + `bin/` + `references/`) vào nơi agent đọc skill rồi cho agent
đọc `SKILL.md`.

**Thủ công:** clone repo này vào thư mục skill của agent rồi cho agent đọc
`SKILL.md`:

```bash
git clone https://github.com/bachiep/shortcut-iphone-skill.git ~/workspace/skills/tao-phim-tat-iphone
```

Skill tuân theo chuẩn agent skill: `SKILL.md` ở root với frontmatter
(`name`, `description` song ngữ Việt/Anh để agent dễ nhận diện),
`tài liệu chi tiết trong `references/`, tool thực thi trong `bin/`.

## Cách dùng

Khi cần tạo / sửa / phân tích phím tắt iPhone, đọc `SKILL.md` và làm theo quy trình
7 bước: hiểu yêu cầu → tìm donor (phân tích shortcut mẫu từ iCloud) → thiết kế
dictionary-driven → viết spec JSON → compile → ký → test → phát hành.

Tool đi kèm (`bin/shortcut-cli`):

```bash
python3 bin/shortcut-cli fetch "<link iCloud>" -o ten.shortcut
python3 bin/shortcut-cli decompile ten.shortcut --pretty
python3 bin/shortcut-cli compile spec.json -o "Ten.shortcut"
python3 bin/shortcut-cli info "Ten.shortcut"
```

## Cấu trúc

- `SKILL.md` — quy trình, tooling, output contract, operating rules
- `references/patterns-phimtat.md` — 33 pattern tái dùng (phimtat.vn, RoutineHub, Viticci, Cassinelli)
- `references/actions.md` — bảng action identifier + tham số, action mới iOS 26
- `references/control-flow.md` — mã WFCondition, Magic Variable, quy tắc build cứng
- `references/url-schemes.md` — `shortcuts://`, `prefs:root=`, scheme app phổ biến
- `references/signing-distribution.md` — ký file, link iCloud, 3 mô hình update
- `references/advanced.md` — Scriptable, x-callback-url, automation, gọi API ngoài
- `references/debugging.md` — quy trình debug, lỗi thường gặp
- `templates/` — 3 mẫu spec JSON đã validate (minimal, menu-driven, http-api), dùng làm điểm khởi đầu
- `bin/shortcut-cli` — tool fetch/decompile/compile (vendored từ
  [hightech-ninja/shortcut-cli](https://github.com/hightech-ninja/shortcut-cli), MIT)

## Kiến thức được tổng hợp từ

- Phân tích dịch ngược 6 phím tắt của phimtat.vn
- Cộng đồng RoutineHub (quy ước updater, version manifest, app bổ trợ)
- r/shortcuts, MacStories (Federico Viticci), Matthew Cassinelli
- Tài liệu Apple (Shortcuts, App Intents, iOS 26 Intelligent Actions)

## Giấy phép

MIT — xem `LICENSE`.
