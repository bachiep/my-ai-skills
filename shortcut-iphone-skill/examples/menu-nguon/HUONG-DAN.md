# Phím tắt Menu Nguồn

## Yêu cầu
iOS 15 trở lên

## Tính năng
- 🔒 Khóa màn hình ngay lập tức
- ⏻ Tắt máy / 🔁 Khởi động lại không cần nút nguồn vật lý
- Rung phản hồi khi chọn, menu tiếng Việt

## Cách dùng
1. Cài file `Menu Nguon.shortcut` vào iPhone (cần ký trước — xem `references/signing-distribution.md`)
2. Chạy phím tắt → chọn thao tác trong menu
3. Muốn dùng nhanh: thêm ra Màn hình chính hoặc gán vào nút Action / chạm mặt lưng

## Mẹo
- Hỏng nút nguồn? Dùng phím tắt này để khóa/tắt máy, mở lại bằng "Chạm để bật màn hình" (Cài đặt → Trợ năng → Cảm ứng)
- File `spec.json` là bản đặc tả đầy đủ — agent đọc để học cách dựng menu dictionary-driven

## Ghi chú kỹ thuật (cho agent)
- 16 actions, đã validate bằng `bin/validate-shortcut`
- Mẫu này minh họa: comment tài liệu đầu file, meta dictionary `{ten, ver, by}`,
  menu `choosefrommenu` 2 cấp, `vibrate` phản hồi xúc giác
