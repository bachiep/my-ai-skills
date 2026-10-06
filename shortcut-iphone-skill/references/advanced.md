# Kỹ thuật nâng cao: vượt giới hạn Shortcuts thuần

## Scriptable — chạy JavaScript thật trên iOS

App chạy JS (ES6) với quyền native: file, lịch, widget, thông báo. Không cần
tài khoản developer.

- **Shortcuts → Scriptable**: action "Run Script" (chọn script, truyền input, nhận
  output) hoặc URL `scriptable:///run?name=TênScript`.
- **Scriptable → Shortcuts**: trong JS mở
  `shortcuts://run-shortcut?name=X&input=text&text=...`, hoặc dùng `CallbackURL`
  để gọi x-callback-url và đợi kết quả.
- **Pattern "executor" dùng chung**: 1 shortcut nhận JSON `{code}` qua input text
  rồi chạy JS động — gọi từ bất kỳ đâu bằng
  `shortcuts://run-shortcut?name=Scriptable%20Executor&input=text&text=<JSON encode>`.
- Dùng cho: logic phức tạp, JSON lồng nhau, đọc/ghi file làm "database" cá nhân,
  vẽ widget màn hình chính/khóa.

## x-callback-url — gọi app qua lại có trả kết quả

Chuẩn: `<scheme>://x-callback-url/<action>?<tham số>&x-success=<url>&x-error=<url>&x-cancel=<url>`.
Mọi giá trị phải URL-encode.

- Trong Shortcuts, action **"Open X-Callback URL"** là cách duy nhất để *đợi* app
  ngoài trả kết quả rồi chạy tiếp (phimtat.vn dùng chiêu này cho web app cắt nhạc).
- App hỗ trợ tốt: **Drafts** (`drafts://x-callback-url/create?text=...`),
  **Fantastical** (`fantastical://x-callback-url/parse?sentence=...`),
  **Bear** (`bear://x-callback-url/create?...`), **Things** (`things:///add?...`).
- Notion không có x-callback-url đầy đủ → dùng API chính thức qua Get Contents of URL.
- Mẹo: luôn có nhánh xử lý khi app đích chưa được cài.

## Automation — trigger và giới hạn thực tế

**Điểm cốt lõi**: trigger KHÔNG nằm trong file `.shortcut` — người dùng phải tự tạo
automation theo hướng dẫn; automation là device-local (không sync sang máy khác).

| Trigger | Chạy ngầm? | Lưu ý |
|---|---|---|
| Giờ giấc | Có (iOS 15.4+ tắt "Hỏi trước khi chạy"; iOS 17+ mặc định chạy ngay) | iOS có thể trì hoãn khi Low Power/khóa lâu |
| Vị trí đến/đi | Có | Cần quyền Vị trí "Luôn luôn" |
| NFC | Có, nhưng **máy phải mở khóa** | Chỉ đọc UID thẻ |
| Focus (bật/tắt) | Có | Rẽ nhánh theo từng Focus bằng If |
| Mở/đóng app | Có | Không kích khi mở lại từ nền |
| Wi-Fi join/leave | Có | Ổn định hơn vị trí, hợp làm "về nhà/tới công ty" |
| Cắm sạc, % pin, báo thức, ngủ/dậy | Có | |

Giới hạn không vượt được: 1 automation = 1 trigger; action tương tác (Ask, gửi tin
nhắn...) vẫn bắt bấm; máy khóa thì action mở app lỗi; automation lỗi chỉ hiện chấm
đỏ → nên thêm "Show Notification" cuối để xác nhận đã chạy; Home automation chạy
trên hub, không được hiện UI.
**Pushcut** cho trigger Apple không có: webhook từ ngoài gọi vào, lịch chạy đáng tin.

## Gọi API ngoài từ Shortcuts

Action "Get Contents of URL": GET/POST/PUT/PATCH/DELETE + headers + body JSON/Form/File.

- GET: nhúng tham số vào URL (Shortcuts tự encode biến). Vd gửi Telegram:
  `https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<ID>&text=<nội dung>`.
- POST JSON: header `Content-Type: application/json`, body JSON; đọc kết quả bằng
  "Get Dictionary Value" (`ok`, `result...`).
- Auth: header `Authorization: Bearer <token>`. **Không nhúng token vào shortcut
  phát hành công khai** — ai decompile cũng đọc được.
- Nhà thông minh ngoài HomeKit: gọi HTTP API trực tiếp (vd ESP8266
  `http://192.168.1.50/relay?on=1`), kết hợp trigger NFC/Siri.

## Chạy JavaScript trên trang web Safari

Action "Run JavaScript on Web Page": chạy JS trên trang Safari đang mở, trả kết quả
về cho action sau.

- Chỉ chạy từ **Share Sheet trong Safari** (input là "Safari web page"); phải bật
  Cài đặt → Shortcuts → Nâng cao → Allow Running Scripts.
- Bắt buộc gọi `completion(kết_quả)` cuối code; cấm `alert()`/`prompt()`.
- Dùng để: trích link/ảnh/giá từ trang, xóa phần tử gây phiền, tự điền form.
- Mẹo tốc độ (iOS 18.4+): URL-encode code rồi chạy qua `new Function(decodeURIComponent("..."))`.

## Khi nào cần app bổ trợ

| Nhu cầu | App | Ghi chú |
|---|---|---|
| Biến lưu giữa các lần chạy (persistent storage) | **Data Jar** (miễn phí) | Key-value sync iCloud; Shortcuts gốc thiếu nhất |
| Biến toàn cục, OCR, NFC đọc/ghi, FaceID, UI kiểu app | **Toolbox Pro** (~$6) | 130+ actions |
| Dialog nhiều nút + timeout, fuzzy search, gộp audio/video, scan tài liệu | **Actions** (miễn phí) | 180+ actions |
| Logic JS phức tạp, widget | **Scriptable** (miễn phí) | Xem trên |
| Chạy nền thật, webhook trigger | **Pushcut** | Cần 1 máy làm server |
