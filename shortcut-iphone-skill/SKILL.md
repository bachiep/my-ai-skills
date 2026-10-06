---
name: "tao_phim_tat_iphone"
description: "Thiết kế, dựng và phát hành phím tắt iPhone (.shortcut): phân tích shortcut có sẵn từ link iCloud, dựng file mới từ đặc tả, ký và đóng gói kèm hướng dẫn tiếng Việt theo phong cách phimtat.vn. Dùng khi người dùng muốn tạo mới, sửa, phân tích hoặc phát hành phím tắt iPhone. / Design, build and publish iPhone Shortcuts: analyze existing shortcuts from iCloud links, compile new .shortcut files from spec, sign and package with Vietnamese guides."
metadata: {"version": "1.1.0"}
---

# Tạo phím tắt iPhone

## Purpose

Biến ý tưởng thành file `.shortcut` thật, import được vào iPhone, kèm hướng dẫn
tiếng Việt. Đồng thời đọc được shortcut của người khác (vd. phimtat.vn) từ link
iCloud để học kỹ thuật và tái sử dụng.

## Workflow

1. **Hiểu yêu cầu**: shortcut làm gì, input từ đâu (Share sheet / nhập tay / file),
   chạy hoàn toàn trên máy hay cần server, iOS tối thiểu bao nhiêu.
2. **Tìm donor**: nếu có shortcut tương tự (link iCloud bất kỳ), fetch về và
   decompile để tái dùng cấu trúc tham số thật. Không bịa identifier hay tham số.
   Cách đọc shortcut người khác: xem `references/signing-distribution.md`.
3. **Thiết kế dictionary-driven** (phong cách phimtat.vn): tách menu, bảng tra cứu,
   config version ra dictionary đặt đầu file; luồng action chỉ chứa logic chung.
   Các pattern tái dùng: xem `references/patterns-phimtat.md`.
4. **Viết spec JSON** rồi compile:
   ```bash
   bin/shortcut-cli compile --no-sign spec.json -o "Ten Phim Tat.shortcut"
   bin/shortcut-cli info "Ten Phim Tat.shortcut"   # kiểm tra số action, cấu trúc
   ```
   Định dạng spec: `{"WFWorkflowName": "...", "WFWorkflowActions": [{"WFWorkflowActionIdentifier": "is.workflow.actions.gettext", "WFWorkflowActionParameters": {"UUID": "...", ...}}]}`.
   Xem mẫu đã validate trong `templates/` (minimal, menu-driven, http-api).
   **Lưu ý quan trọng**:
   - Tự sinh `UUID` **viết hoa** cho MỌI action và tự nối `OutputUUID` trong Magic
     Variable cho đúng — tool compile KHÔNG tự sinh UUID, nó chỉ chuẩn hóa cấu
     trúc (canonical normalization) để file import không bị mất action.
   - `compile` mặc định ký file sau khi dựng; trên Linux ký thất bại (thoát mã lỗi)
     nhưng file unsigned vẫn được ghi — luôn dùng `--no-sign` trên Linux rồi ký
     riêng ở bước 5.
   - `info`/`verify` chỉ kiểm tra cấu trúc, không đảm bảo logic chạy đúng.

## Đọc gì trước (progressive disclosure)

| Việc cần làm | Đọc file này trước |
|---|---|
| Dựng shortcut mới từ đầu | `templates/` + `references/control-flow.md` |
| Phân tích shortcut có sẵn | `references/signing-distribution.md` (§ đọc shortcut người khác) |
| Cần action/identifier nào | `references/actions.md` |
| Menu, update, mẹo hệ thống | `references/patterns-phimtat.md` |
| Vượt giới hạn Shortcuts (JS, API, automation) | `references/advanced.md` |
| Ký file, phát hành, update | `references/signing-distribution.md` |
| Shortcut lỗi, debug | `references/debugging.md` |
| Mở app/Cài đặt bằng URL | `references/url-schemes.md` |
5. **Ký file** (bắt buộc từ iOS 17, không ký thì không import được):
   - Có Mac: `shortcuts sign --mode anyone --input In.shortcut --output Out.shortcut`
   - Không có Mac: POST plist chưa ký tới `https://hubsign.routinehub.services/sign`
   - Mode `anyone` cho phát hành công khai.
6. **Test trên iPhone thật**: import, chạy từng nhánh If/Menu, duyệt các hộp "Cho phép".
7. **Phát hành kiểu phimtat.vn**: trong app Shortcuts bấm Chia sẻ → Copy iCloud Link,
   rồi viết trang hướng dẫn gồm: Tên, Yêu cầu iOS, Tính năng, Cách dùng, Mẹo.
   Chọn mô hình update (API riêng / updater chung / RoutineHub API):
   `references/signing-distribution.md`.

Tài liệu tham khảo trong `references/`: `patterns-phimtat.md` (33 pattern),
`actions.md` (bảng action + iOS 26), `control-flow.md` (điều kiện, biến, quy tắc
build), `url-schemes.md`, `signing-distribution.md` (ký, phát hành, update),
`advanced.md` (Scriptable, x-callback-url, automation, API ngoài),
`debugging.md` (quy trình debug, lỗi thường gặp).

## Tooling

- `bin/shortcut-cli` (vendored từ `hightech-ninja/shortcut-cli`, MIT — xem
  `bin/LICENSE.shortcut-cli`): `fetch` (tải từ link iCloud), `decompile --pretty`
  (đọc logic), `compile --no-sign` (dựng từ JSON), `info`/`verify` (kiểm tra).
- `bin/validate-shortcut`: kiểm tra hard rules của skill (UUID viết hoa/duy nhất,
  Magic Variable trỏ đúng, grouping cân bằng, mã WFCondition chuẩn). Chạy sau mỗi
  lần compile: `python3 bin/validate-shortcut "Ten.shortcut"`.
- `templates/`: 3 mẫu spec đã validate. `examples/menu-nguon/`: ví dụ hoàn chỉnh
  end-to-end (spec + file + hướng dẫn kiểu phimtat.vn).
- Chạy: `python3 bin/<tool> ...` từ thư mục skill. Test suite: `python3 -m unittest
  discover -s tests` (10 tests).

## Output Contract

Mỗi lần giao cho người dùng:
- File `.shortcut` (đã ký nếu ký được; nếu chưa ký thì nói rõ và hướng dẫn cách ký).
- Hướng dẫn tiếng Việt theo cấu trúc: **Tính năng** (gạch đầu dòng) → **Cách dùng**
  (từng bước) → **Mẹo** → **Yêu cầu** (iOS tối thiểu).
- Ghi chú những nhánh cần test trên máy thật và quyền app sẽ hỏi.

## Operating Rules

1. **Donor-based + no invention**: tái dùng tham số từ file thật đã decompile; không bịa
   identifier hay tên tham số. Tra cứu trong `references/actions.md`. Identifier nào
   chưa từng thấy trong file thật thì đánh dấu "chưa verify" và đối chiếu bằng file
   export thật trước khi phát hành.
2. **Control flow**: If/Repeat/Menu dùng chung một `GroupingIdentifier` (UUID) và
   `WFControlFlowMode` (0=mở, 1=nhánh giữa, 2=đóng). Lệch là file hỏng.
   Quy tắc build cứng: `references/control-flow.md`.
3. **WFCondition là mã số nguyên** (bảng chuẩn trong `references/control-flow.md`).
   Bẫy: `4` = bằng chuỗi, `99` = chứa, không có mã "bằng" cho số.
4. **Dictionary-driven**: menu, config, bảng tra cứu tách khỏi luồng action.
   Pattern chi tiết: `references/patterns-phimtat.md`.
5. **Input**: ưu tiên Share-sheet input trước, fallback `ask`/chọn file sau; khai báo
   `WFWorkflowInputContentItemClasses` hẹp để hiện đúng chỗ trong Share sheet.
6. **On-device first**: chỉ đẩy lên server việc Shortcuts không làm được (cắt audio
   chính xác, dịch ảnh...); mọi nhánh gọi mạng phải có fallback khi offline.
   Asset nhỏ (âm thanh, ảnh, config) thì nhúng base64 vào `gettext` thay vì tải về.
7. Không nhúng API key/secret/token vào file phát hành công khai.
8. Ghi rõ yêu cầu iOS tối thiểu theo action đã dùng (xóa nền ảnh: iOS 17+,
   Intelligent Actions/AI: iOS 26+...).
9. Khi phân tích shortcut của người khác: chỉ học kỹ thuật, không copy nguyên
   thương hiệu/nội dung của họ vào sản phẩm mới.
10. **Automation trigger không nằm trong file `.shortcut`** — chỉ ship được
    shortcut, automation người dùng tự tạo theo hướng dẫn. Chi tiết trigger và
    giới hạn: `references/advanced.md`.
11. **Debug theo quy trình**: chạy tay trong editor → chèn Show Result trước bước
    nghi ngờ (biến rỗng là nguyên nhân phổ biến nhất) → sửa → validate → ký lại.
    Xem `references/debugging.md`.
12. Khi Shortcuts thuần không đủ: cân nhắc app bổ trợ (Data Jar cho lưu trữ lâu
    dài, Scriptable cho logic JS, Toolbox Pro/Actions cho UI nâng cao) hoặc tách
    thành shortcut con gọi qua Run Shortcut. Xem `references/advanced.md`.
