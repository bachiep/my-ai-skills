# Action identifiers hay dùng (is.workflow.actions.*)

Mỗi action trong plist: `{"WFWorkflowActionIdentifier": "...",
"WFWorkflowActionParameters": {"UUID": "...", ...}}`.
Tham số dưới đây rút từ file thật đã decompile — khi dựng action mới, ưu tiên
tái dùng cấu trúc tham số của donor hơn là bịa.

## Văn bản / hiển thị / nhập liệu
- `gettext` — tạo đoạn text (`WFTextActionText`)
- `ask` — hộp nhập liệu (`WFAskActionPrompt`)
- `alert` — thông báo chặn (`WFAlertActionTitle`, `WFAlertActionMessage`,
  `WFAlertActionCancelButtonShown`)
- `notification` — banner thông báo; `showresult` — hiển thị kết quả;
  `speaktext` — đọc to
- `text.match` (regex), `text.replace`, `text.combine`, `text.changecase`,
  `text.split`, `text.length`
- `comment` — ghi chú (không chạy, dùng làm tài liệu)

## Biến
- `setvariable` (`WFVariableName`) — đặt biến tên để dùng lại
- `getvariable` — lấy biến; `addvariable`/`appendvariable` — cộng/nối vào biến

## Danh sách & từ điển
- `dictionary` — tạo dict (`WFItems`, xem control-flow.md)
- `getvalueforkey` — tra cứu key trong dict
- `list` — tạo danh sách; `choosefromlist` — menu từ danh sách động
- `choosefrommenu` — menu phân cấp cứng (`WFMenuItems`, `WFMenuPrompt`)
- `getitemfromlist` (`WFItemSpecifier`: First/Last/Random...), `count`

## Số & ngày giờ
- `number` (`WFNumberActionNumber`), `math` (`WFMathOperation`: `+ - * / ...`,
  `WFMathOperand`), `number.random` (`WFNumberActionNumber` min/max qua
  `WFNumberActionNumberMin`/`Max`), `count`

## Điều khiển luồng
- `conditional` — If (`WFCondition` = mã số, xem control-flow.md;
  `WFControlFlowMode`: 0 mở / 1 nhánh giữa / 2 đóng)
- `repeat.each`, `repeat.count` (`WFRepeatCount`) — vòng lặp, đóng bằng
  `WFControlFlowMode: 2`
- `exit` — dừng shortcut; `runworkflow` — gọi shortcut khác;
  `wait`/`delay` (`WFDelayTime`)

## Mạng & URL
- `url` (`WFURLActionURL`), `downloadurl` (`WFURL`, `WFHTTPMethod` = `GET`/`POST`,
  `WFJSONValues` cho POST JSON, `WFFormValues` cho POST form)
- `openurl` (`WFInput`), `openxcallbackurl`
- `getwebpagecontents` + `detect.images` — render URL/HTML rồi trích ảnh
- `urlencode`, `base64encode` (`WFEncodeMode`: Encode/Decode)

## Ảnh
- `selectphoto`, `takephoto`, `takescreenshot`
- `image.removebackground` (iOS 17+), `image.resize`, `image.convert`
  (`WFImageFormat`: JPEG/PNG...), `image.crop`, `image.rotate`,
  `overlayimageonimage`, `getimagesfrominput`

## Tệp & media
- `file.select`, `documentpicker.save` (`WFAskWhereToSave`), `savefile`,
  `getfile`, `appendfile`, `setitemname`
- `encodemedia`, `trimvideo`, `trimmedia`, `properties.music`
- `savetocameraroll`, `share`

## Clipboard
- `getclipboard`, `setclipboard` (`WFClipboard`)

## Hệ thống & thiết bị
- `getdevicedetails` (`WFDeviceDetail`: System Version, Device Name...)
- `flashlight` (`WFFlashlightSetting`: On/Off/Toggle), `vibrate`, `playsound`,
  `setvolume`, `lockscreen`, `reboot`
- `dnd.getfocus` / `dnd.set` — đọc & đặt Không làm phiền
- `vpn.set` — bật/tắt VPN đã cấu hình
- `phonenumber` + `com.apple.mobilephone.call` — gọi điện

## App Intent hệ thống (identifier dài, copy nguyên từ donor)
- `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`
- `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleAssistiveTouchIntent`
- `com.apple.ShortcutsActions.OpenCameraAction`
- `com.apple.VoiceMemos.RecordVoiceMemoIntent`
- `com.apple.mobiletimer-framework.MobileTimerIntents.MTCreateAlarmIntent`

## AI — Apple Intelligence (iOS 26+)
- `is.workflow.actions.askllm` — "Use Model" (`WFLLMPrompt`, `WFLLMModel`,
  `WFGenerativeResultType`): đưa text vào AI (On-Device / Private Cloud / ChatGPT),
  thay hàng loạt If/Regex thủ công bằng một lời nhắc.
- Writing Tools: Summarize / Rewrite / Proofread / Adjust Tone / Make List /
  Make Table / Make Text Concise. Image Playground: Create Image.
- Visual Intelligence: mở nhận diện theo ngữ cảnh.

## Hành động mới đáng chú ý (iOS 26)
- Photos: Search Photos, Filter Library, Rename Album. Messages: Find Message,
  Find Conversation. Mail: Find Message. Notes: Append Checklist Item.
- iWork: Export in Background. Screen Time: Get App & Website Data.
- `is.workflow.actions.nothing` — no-op để tách khối action hoặc chặn input
  truyền xuống. `is.workflow.actions.openapp` (`WFAppIdentifier`) — mở app.
  `is.workflow.actions.runshellscript` — chỉ macOS, chạy với PATH rút gọn
  (dùng đường dẫn tuyệt đối).
- Set Charge Limit (iOS 26.4). Calculate Expression giờ tính được đơn vị + tỷ giá
  realtime. Create QR Code tùy chỉnh màu/style.
- Đổi tên: **Show Result → Show Content** (iOS 26).

## Lưu ý tham số
- `is.workflow.actions.deletephotos` dùng key `photos`, không phải `WFInput`.
- Mọi action cần `UUID` riêng (tool tự sinh nếu thiếu).
- Tham chiếu output action khác = Magic Variable (xem control-flow.md).
