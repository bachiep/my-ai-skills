# Pattern từ phimtat.vn (rút ra từ 6 phím tắt đã dịch ngược)

Nguồn: Đọc số tiền thành chữ (77 actions), Chế độ đọc sách (2), Kiểm tra iPhone (60),
Action Button (84), Tạo nhạc chuông (74), Tạo Sticker (78).

## Nhóm INPUT

1. **Share-sheet-first, hỏi sau**: `conditional` kiểm tra Shortcut Input có giá trị
   không → có thì dùng, không thì `ask` / `selectphoto` / `file.select`.
2. **Khai báo InputTypes hẹp**: đặt `WFWorkflowInputContentItemClasses` đúng loại
   (vd chỉ `WFStringContentItem`) để shortcut hiện đúng chỗ trong Share sheet.
3. **Nhận diện loại file bằng regex trên File Extension**: `mp4|mov|...` vs
   `mp3|m4a|...` để rẽ nhánh video/audio.

## Nhóm XỬ LÝ DỮ LIỆU

4. **Dictionary làm bảng tra cứu**: thay hàng loạt `conditional` bằng 1 dictionary +
   `getvalueforkey` (vd bảng số→chữ 115 mục).
5. **Dictionary làm config menu + dispatch generic**: mỗi mục menu là dict con có khóa
   `alert` và/hoặc `url`; 2 `conditional` generic xử lý trước, mục đặc biệt mới rẽ
   nhánh riêng. Thêm tính năng = thêm 1 dòng dictionary.
6. **Chuỗi regex chuẩn hóa text**: trích (`text.match`) → làm sạch (`text.replace`
   nhiều bước) → hậu xử lý quy tắc ngôn ngữ.
7. **Tách nhóm ký tự bằng lookahead**: `\d{1,3}(?=(?:\d{3})*$)` để duyệt từng cụm
   3 chữ số.

## Nhóm UI / MENU

8. **Menu 2 cấp + phản hồi xúc giác**: `choosefrommenu` lồng nhau, mỗi mục chạy
   `vibrate` trước action chính.
9. **choosefromlist cho menu động**: khi danh sách mục lấy từ dữ liệu (dictionary keys,
   kết quả tải về) thì dùng `choosefromlist` thay vì `choosefrommenu` cứng.
10. **Comment mở đầu làm tài liệu**: `comment` đầu shortcut ghi mô tả + link cập nhật.

## Nhóm HỆ THỐNG

11. **App Intent cho trợ năng**: `AXToggleColorFiltersIntent` (bộ lọc màu),
    `AXToggleAssistiveTouchIntent` — những thứ URL scheme không làm được.
12. **prefs:root= mở sâu Cài đặt**: `prefs:root=Privacy&path=LOCATION` mở thẳng trang
    Vị trí khi Shortcuts không toggle được GPS. (Không chính thức, có thể gãy theo iOS.)
13. **Toggle đúng cách**: đọc trạng thái hiện tại (`dnd.getfocus`) → `conditional` →
    đặt ngược lại, thay vì bật/tắt mù.
14. **Đọc plist hệ thống qua file://**: `file://.../com.apple.MobileGestalt.plist` +
    `getvalueforkey` để lấy thông tin thiết bị sâu. (Có thể bị bịt ở iOS mới.)
15. **Render HTML → chụp → overlay ảnh**: dựng `data:text/html;base64,...` →
    `getwebpagecontents` → `detect.images` → `overlayimageonimage` — cách duy nhất
    vẽ chữ/đồ họa tùy biến lên ảnh trong Shortcuts.
16. **Test phần cứng bằng repeat.count**: lặp `vibrate`/`flashlight`/`playsound` kèm
    `delay`.
17. **Mở app hệ thống qua Intent**: `OpenCameraAction`, `RecordVoiceMemoIntent`,
    `MTCreateAlarmIntent`, gọi điện bằng `phonenumber` + `com.apple.mobilephone.call`.

## Nhóm PHÂN PHỐI / UPDATE

18. **Meta dictionary chuẩn đầu shortcut**: `{ver, id, by}` — `id` là ID bài viết,
    `ver` để so sánh bản mới.
19. **Kiểm tra cập nhật tự động**: GET `check-update?id=<id>` → `conditional` so sánh
    số bản → alert + `openurl ?p=<id>` + `exit`.
20. **Kiểm tra cập nhật thủ công trong menu**: mục "Cập nhật phím tắt" thay vì tự chạy
    đầu — ít làm phiền hơn.
21. **Phát hiện offline không cần mạng**: URL
    `data:text/html,<body/><script>if(navigator.onLine){document.write("online")};</script>`
    → `conditional` contains `"online"` — chỉ gọi API khi chắc có mạng.
22. **Đặt logic nặng lên server** khi Shortcuts không làm được (cắt audio, dịch ảnh,
    tra IPSW): upload → xử lý phía server → trả kết quả. Đổi lại là phụ thuộc server —
    luôn có fallback khi server lỗi.
23. **x-callback-url tới web app**: `openxcallbackurl` mở web UI rồi quay lại đúng vị
    trí trong luồng, bọc trong vòng lặp có cờ thoát.

## Pattern từ cộng đồng quốc tế (RoutineHub, Viticci, Cassinelli)

24. **Nhúng asset base64 trong shortcut**: file nhỏ (âm thanh, ảnh, config) nằm gọn
    trong 1 action `gettext` → decode (`base64encode` chế độ Decode) khi chạy →
    shortcut offline hoàn toàn, không cần server/CDN. (Water Eject nhúng file M4A
    ~215KB: setvolume max → decode → playsound → trả volume về cũ.)
25. **Updater dùng chung thay vì tự viết**: thay vì mỗi shortcut gọi API riêng,
    dùng 1 shortcut updater chung (UpdateKit / Swing Updater): `getmyworkflows` →
    kiểm tra đã cài updater chưa → `dictionary {Shortcut Name, Current Version}` →
    `runworkflow` gọi updater. Chỉ 3 action để "đăng ký" update.
26. **Update qua RoutineHub API** (không cần server riêng):
    `GET routinehub.co/api/v1/shortcuts/<id>/versions/latest` → JSON
    `{Version, URL, Notes, Release}`. Giới hạn 20 call/phút, 300 call/ngày/IP.
27. **Version manifest** (quy ước mở): file `iCloud Drive/Shortcuts/RoutineHub/versions.json`
    dạng `{"<id>": "<version>"}`; shortcut nào cũng được đọc/ghi (chỉ sửa key của mình).
28. **Menu đệ quy**: mục "← Back" gọi `runworkflow` chính shortcut đó → quay lại menu
    chính, không cần vòng lặp hay cờ.
29. **Shortcut-như-hàm**: một shortcut vừa chạy độc lập vừa nhận input từ shortcut
    khác qua Run Shortcut và trả output về — tách logic dùng chung ra "hàm".
30. **Phát hiện loại nội dung rồi dispatch**: nhận URL → nhận diện loại (bài báo,
    video, sản phẩm...) → rẽ nhánh xử lý riêng cho từng loại (kiểu Universal Clipper
    của Viticci).
31. **Chuỗi RSS → Choose from List → mở URL**: lấy feed → hiện N item mới nhất →
    mở mục đã chọn (kiểu Cassinelli cho YouTube/podcast).
32. **Khung shortcut chuẩn**: `comment` (credit) → menu chính (chức năng / Settings)
    → submenu Settings gồm: Cập nhật, Xem trang shortcut, Giới thiệu.
33. **Release tử tế**: version dạng `X.Y`, mỗi bản có release notes + ngày UTC +
    version history; badge markdown khi hỗ trợ updater.

## Nguyên tắc productization (từ cộng đồng quốc tế)

34. **Shortcut gọn, server làm việc nặng**: giữ shortcut vài action điều phối,
    logic phức tạp đẩy lên server/API — dễ bảo trì, update không cần phát hành lại.
35. **Webhook cho automation**: dùng dịch vụ webhook (vd ntfy.sh) làm cầu nối khi
    cần trigger từ ngoài gọi vào mà không có Pushcut.

## Điểm mạnh / yếu trong phong cách của họ

**Mạnh**: dictionary-driven (dễ mở rộng); on-device first cho logic thuần túy;
UX tiếng Việt tốt (menu emoji, prompt rõ, vibrate phản hồi); phòng thủ input
(giới hạn, kiểm tra offline); meta `{ver,id,by}` nhất quán.

**Yếu**: phụ thuộc server cho tính năng cốt lõi ở 3/6 shortcut (sập server = chết,
không fallback); endpoint update không nhất quán; phụ thuộc `prefs:root=`, link
YouTube ngoài; logic phức tạp ít comment; lỗi mạng bị bỏ qua lặng lẽ.
