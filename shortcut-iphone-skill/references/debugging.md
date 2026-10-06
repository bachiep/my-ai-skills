# Debug & lỗi thường gặp

## Quy trình debug

1. **Xác định tầng lỗi trước khi sửa**: chạy thủ công trong editor.
   - Chạy tay mà lỗi → vấn đề nằm trong actions.
   - Chạy tay OK mà automation không chạy → vấn đề ở trigger (chưa bật, đang chờ
     xác nhận, máy khóa, thiếu quyền).
2. **Gắn thiết bị đo**: chèn tạm action Show Result/Notification ngay trước bước
   nghi ngờ để hiện giá trị biến đã resolve. **Biến rỗng là nguyên nhân của phần
   lớn ca lỗi.** Xóa sau khi sửa xong.
3. **Test logic nặng ở ngoài trước**: vd nghi Run Shell Script thì chạy script với
   dữ liệu mẫu trong Terminal trước khi ký lại.
4. **Sửa → validate → ký lại → verify lại.** Mọi chỉnh sửa sau khi validate đều
   cần một vòng validate + ký mới.
5. Checklist trước khi đổ lỗi cho trigger: chạy shortcut một lần trong editor để
   duyệt hết hộp "Cho phép" (Photos, Contacts, Location, app bên thứ ba); kiểm tra
   "Ask Before Running" có đang bật; thay action của app bên thứ ba bằng action hệ
   thống để loại trừ.

## Sai lầm phổ biến

| Sai lầm | Cách tránh |
|---|---|
| Biến rỗng mà không kiểm tra → action sau chạy sai lặng lẽ | If "has any value" (mã 100) sau mỗi bước lấy dữ liệu ngoài |
| Action nhận nhầm input của action trước (input chaining) | Set Variable đặt tên rõ; dùng `nothing` để chặn input khi cần |
| Đường dẫn file cứng theo máy tạo | Dùng "Ask Where To Save" / biến thư mục, không hardcode |
| Không test nhánh offline | Mọi nhánh gọi mạng phải có fallback; test ở chế độ máy bay |
| Quên duyệt quyền lần đầu rồi đổ lỗi automation hỏng | Chạy tay trong editor một lần để duyệt hết permission |
| Đặt tên trùng → tạo bản "Tên 2" gây nhầm | Xóa bản cũ trước khi import lại khi test lặp |
| Dùng `prefs:root=` làm xương sống | Luôn có đường lui thủ công; coi scheme không chính thức là "có thể gãy" |
| Nhồi 50+ action vào một shortcut | Tách thành shortcut con + Run Shortcut; mỗi shortcut một nhiệm vụ |
| Không ghi chú logic phức tạp | Comment action đầu mỗi khối |
| Không kiểm tra biến rỗng sau download | If has-any-value trước khi parse JSON |
