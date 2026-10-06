# URL schemes

Dùng với action **Mở URL** (`is.workflow.actions.openurl`) hoặc từ web/app ngoài.

## shortcuts:// (Apple công bố chính thức)

Mọi giá trị query phải URL-encode.

| Mục đích | URL |
|---|---|
| Mở app Shortcuts | `shortcuts://` |
| Tạo phím tắt mới | `shortcuts://create-shortcut` |
| Mở phím tắt để sửa | `shortcuts://open-shortcut?name=<tên>` |
| Chạy phím tắt | `shortcuts://run-shortcut?name=<tên>` |
| Chạy + truyền text | `shortcuts://run-shortcut?name=X&input=text&text=<text>` |
| Chạy + lấy từ clipboard | `shortcuts://run-shortcut?name=X&input=clipboard` |
| Mở Gallery / tìm | `shortcuts://gallery`, `shortcuts://gallery/search?query=<từ khóa>` |
| Import từ URL (không chính thức nhưng dùng rộng rãi) | `shortcuts://import-shortcut?url=<link file .shortcut>&name=<tên>` |
| x-callback-url | `shortcuts://x-callback-url/run-shortcut?name=X&x-success=<url>&x-error=<url>&x-cancel=<url>` |

Trong nội bộ shortcut-gọi-shortcut thì dùng action `runworkflow` thay vì scheme.

## Mở trang Cài đặt hệ thống (không chính thức, có thể gãy theo iOS)

| Trang | URL |
|---|---|
| Wi-Fi | `prefs:root=WIFI` |
| Bluetooth | `prefs:root=Bluetooth` |
| Dữ liệu di động | `prefs:root=MOBILE_DATA_SETTINGS_ID` |
| Điểm truy cập cá nhân | `prefs:root=INTERNET_TETHERING` |
| Pin | `prefs:root=BATTERY_USAGE` |
| Tình trạng pin | `prefs:root=BATTERY_USAGE&path=BATTERY_HEALTH` |
| Màn hình & Độ sáng | `prefs:root=DISPLAY` |
| Thông báo | `prefs:root=NOTIFICATIONS_ID` |
| Âm thanh | `prefs:root=Sounds` |
| Tập trung | `prefs:root=DO_NOT_DISTURB` |
| Thời gian sử dụng | `prefs:root=SCREEN_TIME` |
| Cài đặt chung | `prefs:root=General` |
| Giới thiệu | `prefs:root=General&path=About` |
| Cập nhật phần mềm | `prefs:root=General&path=SOFTWARE_UPDATE_LINK` |
| Dung lượng iPhone | `prefs:root=General&path=STORAGE_MGMT` |
| VPN | `prefs:root=General&path=VPN` |
| Trợ năng | `prefs:root=ACCESSIBILITY` |
| Quyền riêng tư → Vị trí | `prefs:root=Privacy&path=LOCATION` |
| Tài khoản Apple | `prefs:root=APPLE_ACCOUNT` |
| Cài đặt của 1 app | `App-prefs:<bundleID>` (vd `App-prefs:com.apple.mobilesafari`) |

Danh sách đầy đủ do cộng đồng duy trì (repo `ios-settings-urls` trên GitHub).
Từ iOS 26, điều hướng Wi-Fi bằng scheme kém ổn định.

## Scheme app phổ biến

- Gọi: `tel://<số>`, `telprompt://<số>` (hỏi trước khi gọi)
- SMS: `sms://<số>&body=<text>`
- FaceTime: `facetime://<số>`, `facetime-audio://<số>`
- WhatsApp: `whatsapp://send?phone=<số>&text=<text>`
- Telegram: `tg://resolve?domain=<username>`
- Mail: `mailto:<địa chỉ>?subject=...&body=...`
