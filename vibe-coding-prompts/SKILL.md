---
name: vibe-coding-prompts
description: 15 Vietnamese Vibe Coding Prompts for specific project phases (PRD, Ultra Plan, Guardrails, etc.). Use this skill to structure your interactions with the agent at any stage of development.
---

# 15 Vibe Coding Prompts (Tiếng Việt)

Vibe coding không có nghĩa là gõ đại prompt rồi hy vọng là AI sẽ trả lời đúng. Khác biệt giữa một agent làm được việc và một agent phá nát repo nằm ở chỗ bạn đưa cho nó cái gì.

Dưới đây là 15 prompts chuẩn hóa cho từng giai đoạn dự án. Khi người dùng yêu cầu một trong các tính năng này, hãy tuân thủ cách làm việc tương ứng.

## 01. Viết một bản PRD đầy đủ
Tạo tài liệu Yêu cầu Sản phẩm (Product Requirements Document) chi tiết. Trước khi code, phải chốt PRD.

## 02. Tạo file CLAUDE.md / AGENTS.md
Xây dựng "bộ não" cho dự án. Khai báo các quy tắc lập trình, kiến trúc, và cách giao tiếp chuẩn mực trong file cấu hình gốc.

## 03. Chế độ Ultra Plan (Quan trọng nhất)
**Kích hoạt:** Khi nhận lệnh "Ultra Plan", Agent phải bắt buộc ĐỌC HẾT các file liên quan, đề xuất 2-3 hướng giải quyết kèm theo Trade-off (Đánh đổi) cho mỗi hướng.
**Quy tắc:** Tuyệt đối DỪNG LẠI và đợi người dùng duyệt phương án trước khi chạm vào bất cứ dòng code nào.

## 04. Phát triển theo Spec
Bắt buộc Agent đọc file Spec/PRD trước, phân rã thành các task nhỏ và code theo đúng bản thiết kế đã chốt.

## 05. Design Brief UI & UX đầy đủ
Yêu cầu Agent liệt kê các components, màu sắc, font chữ, trạng thái (hover, active, disabled) trước khi sinh ra HTML/CSS/UI code.

## 06. Kế hoạch triển khai
Vẽ ra lộ trình (Roadmap) từng bước cho một tính năng lớn để tránh bị ngợp context.

## 07. Kết nối một MCP Server
Phân tích yêu cầu, gọi đúng MCP Server cần thiết (ví dụ: truy vấn DB, đọc file, gọi API ngoài) thay vì cố đoán.

## 08. Kết nối Database của bạn
Cấu hình chuẩn chỉ các file `.env` (ẩn thông tin nhạy cảm), tạo connection pool, và check kết nối an toàn.

## 09. Tìm lỗ hổng bảo mật
Liên kết với các skill như `redamon-reference` hoặc các công cụ quét bảo mật tĩnh (Static Analysis) để rà soát XSS, SQLi, CSRF.

## 10. Debug lỗi thật nhanh
Tuân thủ vòng lặp: Tái hiện lỗi -> Thu hẹp phạm vi -> Đặt giả thuyết -> Thêm Log -> Sửa lỗi. (Tương tự `diagnosing-bugs`).

## 11. Viết E2E Test cho ứng dụng
Sử dụng Playwright, Cypress hoặc công cụ tương tự để mô phỏng hành vi người dùng cuối. Bắt buộc test phải chạy qua (Green) mới tính là xong.

## 12. Dọn sạch Dead Code
Quét và phân tích những hàm/biến không còn sử dụng. LUÔN HỎI LẠI TRƯỚC KHI XÓA.

## 13. Viết Git Commit gọn gàng
Tạo commit message theo chuẩn Conventional Commits (feat, fix, refactor, chore) dựa trên diff.

## 14. Dùng Hooks làm Guardrails (Quan trọng)
Tự động kích hoạt lint + typecheck sau mỗi lần sửa file.
**Quy tắc:** Chặn cứng (block) việc tự động sửa đổi các đường dẫn nhạy cảm như file `migrations`, file `.env`, trừ khi người dùng cấp quyền xác nhận thủ công.

## 15. Biến một tác vụ thành Skill
Việc nào làm đi làm lại thì đóng gói thành một thư mục skill riêng lẻ có file `SKILL.md` bên trong để tái sử dụng mãi mãi.
