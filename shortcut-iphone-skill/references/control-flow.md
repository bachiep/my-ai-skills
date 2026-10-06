# Control flow, điều kiện & biến

## Quy tắc sắt của If / Repeat / Menu

Các action mở/đóng khối dùng chung một `GroupingIdentifier` (1 UUID cho cả khối):

| Vai trò | `WFControlFlowMode` |
|---|---|
| Mở khối (If, Repeat, Menu) | `0` |
| Nhánh giữa (Otherwise, mỗi mục menu) | `1` |
| Đóng khối (End If, End Repeat, End Menu) | `2` |

`bin/shortcut-cli compile` tự sinh và cân bằng grouping nếu spec viết đúng thứ tự
mở → ... → đóng. **Lệch grouping là file hỏng, import bị cắt cụt.**

## Mã điều kiện WFCondition (đã verify từ file Apple)

| Mã | Nghĩa trong app | Dùng kèm |
|---|---|---|
| `0` / `1` / `2` / `3` | số: `<` / `<=` / `>` / `>=` | `WFNumberValue` |
| `4` / `5` | chuỗi: bằng / không bằng | `WFConditionalActionString` |
| `8` / `9` | chuỗi: bắt đầu bằng / kết thúc bằng | `WFConditionalActionString` |
| `99` | chuỗi: chứa | `WFConditionalActionString` |
| `999` | chuỗi: không chứa | `WFConditionalActionString` |
| `100` / `101` | có giá trị bất kỳ / không có giá trị | (không cần trường so sánh) |
| `1003` | số nằm trong khoảng | `WFNumberValue` (dưới) + `WFAnotherNumber` (trên) |

**Bẫy**: `4` là *bằng chuỗi*, không phải "lớn hơn". Không có mã "bằng" cho số —
muốn so sánh bằng 2 số thì gộp `>=` và `<=`.

Ví dụ If thật (kiểm tra update của Tạo Sticker):
If [đầu vào = số từ server] **lớn hơn** [số `ver` trong dictionary] → Alert → Mở URL → Exit.

## Magic Variable — tham chiếu output action khác

Action sau dùng output action trước bằng dict token đặt trong tham số:

```json
{"Value": {"Type": "ActionOutput", "OutputName": "URL",
           "OutputUUID": "42216FD6-1676-41E1-804C-D6879B8D030C",
           "Aggrandizements": [
             {"Type": "WFCoercionVariableAggrandizement",
              "CoercionItemClass": "WFRichTextContentItem"}]},
 "WFSerializationType": "WFTextTokenAttachment"}
```

- `OutputName`: tên output chuẩn (`"Text"`, `"URL"`, `"Shortcut Input"`, ...) hoặc
  tên custom qua `CustomOutputName` của action nguồn.
- `Aggrandizements`: ép kiểu (Coercion) hoặc lấy thuộc tính — vd lấy key `ver`
  trong dictionary: `{"Type": "WFDictionaryValueVariableAggrandizement",
  "DictionaryKey": "ver"}`.
- Nhúng token **giữa chuỗi văn bản**: dùng `WFTextTokenString` với ký tự
  placeholder tại vị trí token và `attachmentsByRange` chỉ vị trí:
  `{"Value": {"string": "https://api.example.com/check?id=<PH>",
  "attachmentsByRange": {"{39, 1}": {"Type": "ActionOutput", ...}}},
  "WFSerializationType": "WFTextTokenString"}`
- `{"Value": {"Type": "ExtensionInput"}, ...}` = input truyền vào action (nối chuỗi
  mặc định). `{"Value": {"Type": "Ask"}, ...}` = "Hỏi mỗi lần chạy".

## Định dạng Dictionary trong plist

```json
"WFItems": {"Value": {"WFDictionaryFieldValueItems": [
  {"WFKey": {"Value": {"string": "ver", "WFSerializationType": "WFTextTokenString"}},
   "WFItemType": 0,
   "WFValue": {"Value": {"string": "1", "WFSerializationType": "WFTextTokenString"}}}
]}, "WFSerializationType": "WFDictionaryFieldValue"}
```

`WFItemType`: 0=text, 1=number, 2=boolean, 3=array, 4=dictionary.

## Key plist cấp cao nhất (rút gọn)

Bắt buộc: `WFWorkflowActions` (array). Nên có: `WFWorkflowName`,
`WFWorkflowIcon` (`WFWorkflowIconGlyphNumber` + `WFWorkflowIconStartColor`),
`WFWorkflowInputContentItemClasses` (vd `["WFImageContentItem"]` để hiện trong
Share sheet khi xem ảnh), `WFWorkflowTypes` (vd `["ActionExtension"]` cho Share
sheet), `WFWorkflowMinimumClientVersion` (`900` ≈ iOS 14+), `WFWorkflowImportQuestions`
(câu hỏi lúc import: `ActionIndex`, `ParameterKey`, `Text`, `DefaultValue`).

Mẫu tối thiểu xem `bin/shortcut-cli` decompile bất kỳ file mẫu nào, hoặc dựng
shortcut 1 action trong app rồi export.

## Quy tắc cứng khi dựng file bằng code (đã verify)

1. **UUID viết HOA — và agent phải TỰ SINH cho mọi action.** Tool `compile` KHÔNG
   tự sinh UUID; nếu thiếu, Magic Variable sẽ trỏ vào khoảng không và shortcut
   chạy sai lặng lẽ. `info`/`verify` không phát hiện được lỗi này — chỉ kiểm tra
   bằng cách decompile ngược và đối chiếu `OutputUUID`.
2. `WFControlFlowMode` là **integer** (0=mở, 1=giữa, 2=đóng), không phải string.
2. Mọi khối control-flow mở phải có đóng **cùng GroupingIdentifier**.
3. **Tên shortcut sau import = tên file lúc ký**, không phải `WFWorkflowName`.
   Đặt tên file output đúng tên muốn hiển thị, không thêm hậu tố `_signed`.
4. Shortcut nhận input ngoài **bắt buộc** khai báo `WFWorkflowInputContentItemClasses`
   (mảng rỗng = input không bao giờ tới nơi).
5. Action xóa ảnh dùng key **`photos`** (chữ thường), không phải `WFInput`.
6. File đưa vào `shortcuts sign` bắt buộc có đuôi `.shortcut`.
7. Import trùng tên tạo bản "Tên 2" chứ không ghi đè — xóa bản cũ trước khi test lại.
8. Ký tự U+FFFC đánh dấu điểm chèn biến trong chuỗi; `attachmentsByRange` trỏ tới
   `OutputUUID` của action nguồn; biến đơn lẻ (không kèm text) dùng
   `WFTextTokenAttachment`.
