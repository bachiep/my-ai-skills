# Ký, phân phối & đọc shortcut người khác

## Vì sao phải ký

- iOS 15+: file `.shortcut` là envelope AEA1 đã ký. iOS 17+ **bỏ hẳn** công tắc
  "Cho phép phím tắt không đáng tin" → file không ký hợp lệ thì **không import được**.
- Khi ký, Apple nhận 1 bản copy để kiểm tra chống giả mạo.

## Cách ký

| Cách | Lệnh | Ghi chú |
|---|---|---|
| Apple CLI (macOS) | `shortcuts sign --mode anyone --input In.shortcut --output Out.shortcut` | Chính thức, cần đăng nhập iCloud trên máy Mac |
| HubSign (mọi OS) | POST JSON tới `https://hubsign.routinehub.services/sign` | Dịch vụ cộng đồng của RoutineHub, trả về file AEA1 đã ký |
| Shortcut "Sign Shortcut File" (trên iPhone) | Cài từ RoutineHub #26044, chạy trên máy | Ký ngay trên iPhone khi không có Mac và HubSign bị chặn |

Gọi HubSign bằng JSON: `{"shortcutName": "<tên>", "shortcut": "<plist XML dạng chuỗi>"}`,
header `Content-Type: application/json`. Plist gửi đi nên ở định dạng XML
(`plistlib.dumps(wf, fmt=FMT_XML)`). Kiểm tra kết quả: 4 byte đầu phải là `AEA1`.

Mode: `anyone` (ai cũng import được — dùng khi phát hành công khai),
`people-who-know-me` (chỉ người có trong Danh bạ của người ký).

## Link chia sẻ iCloud (cách phimtat.vn phát hành)

1. Trong app Shortcuts: Chia sẻ phím tắt → **Copy iCloud Link**.
2. Apple ký và upload, trả về `https://www.icloud.com/shortcuts/<uuid>`.
3. Người nhận mở link → "Get Shortcut" → xem trước actions → "Add Shortcut".
4. iOS 15+: người nhận **không cần** bật gì thêm — đây là luồng phát hành chuẩn.

Lưu ý vận hành:
- Link gắn với **Apple ID đã tạo link** → dùng Apple ID riêng cho phát hành.
- Ra bản mới = share lại = **link mới** (link cũ vẫn trỏ bản cũ). Vì vậy các trang
  lớn nhúng cơ chế "kiểm tra update" trong shortcut: gọi API riêng, so version,
  báo người dùng tải đè (xem mẫu meta `{ver,id}` + pattern kiểm tra update trong
  `references/patterns-phimtat.md`).

## Cơ chế update: 3 mô hình

1. **Tự kiểm tra qua API riêng** (kiểu phimtat.vn): meta `{ver,id}` đầu shortcut →
   GET `check-update?id=` → so sánh → alert + mở trang tải + exit.
2. **Dùng updater chung của cộng đồng** (khuyến nghị khi phát hành rộng):
   `getmyworkflows` → kiểm tra đã cài UpdateKit/Swing Updater chưa →
   `dictionary {Shortcut Name, Current Version}` → `runworkflow` gọi updater.
   Chỉ 3 action để "đăng ký".
3. **RoutineHub API** (không cần server riêng):
   `GET routinehub.co/api/v1/shortcuts/<id>/versions/latest` → JSON
   `{Version, URL, Notes, Release}` (giới hạn 20 call/phút, 300 call/ngày/IP).

Quy ước version manifest (mở, shortcut nào cũng đọc/ghi được):
file `iCloud Drive/Shortcuts/RoutineHub/versions.json` dạng `{"<id>": "<version>"}` —
chỉ sửa key của mình, không xóa entry của shortcut khác. Version dạng `X.Y`,
mỗi bản có release notes + ngày UTC.

## Đọc shortcut của người khác (đã kiểm chứng)

1. Lấy `<id>` từ HTML trang chia sẻ:
   `curl -sL "<url-trang>" -A "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15" | grep -o 'icloud.com\\/shortcuts\\/[a-f0-9]*'`
2. Gọi `https://www.icloud.com/shortcuts/api/records/<id>` → JSON chứa
   `fields.signedShortcut.value.downloadURL` (mẫu có `${f}` → thay bằng tên file
   URL-encode) → tải file.
3. `bin/shortcut-cli fetch "<link-icloud>" -o <file>` (tool tự làm bước 2),
   rồi `bin/shortcut-cli decompile <file> --pretty` để đọc từng action.
   iCloud trả về bản **unsigned** nên đọc thoải mái trên Linux.

## Cấu trúc trang phát hành kiểu phimtat.vn

Mỗi phím tắt một trang gồm: nút **Nhận phím tắt** (link iCloud) → **Yêu cầu**
(iOS tối thiểu) → **Chức năng chính** → **Hướng dẫn** (từng bước) → **Mẹo**.
Khi giao shortcut cho người dùng, dùng đúng cấu trúc này.
