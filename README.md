# My AI Skills

Đây là kho lưu trữ cá nhân tổng hợp các kỹ năng (Skills) và quy trình chuẩn (SOPs) dành cho AI Coding Agents (như Antigravity, Claude Code, Codex, v.v.).

Kho lưu trữ này bao gồm các bộ quy tắc khắt khe nhất để đảm bảo AI hoạt động có kỷ luật, không "vibe coding" (code mò), và tuân thủ các tiêu chuẩn Engineering khắt khe.

## Danh sách các Skills

### 1. Kỷ luật Lõi (Core Discipline)
- **`skill-agent`**: 9 nguyên tắc làm việc thép dành cho AI (Tier 1 & Tier 2). Bắt buộc phải xác minh, không suy đoán bừa bãi.
- **`vibe-coding-prompts`**: 15 Prompts chuẩn hóa bằng tiếng Việt cho từng giai đoạn của dự án (PRD, Ultra Plan, Guardrails, v.v.).

### 2. Định tuyến Công cụ (Tool Pointers)
- **`redamon-reference`**: Sợi dây liên kết để AI biết cách tìm và kích hoạt hệ thống bảo mật Offensive Security (RedAmon) được cài đặt cục bộ trên máy.

### 3. Quy trình Kỹ thuật & Năng suất (Engineering & Productivity)
*(Được chọn lọc và tinh chỉnh từ repository của Matt Pocock)*
- **`grill-me` / `grill-with-docs`**: Bắt AI "vặn vẹo" và hỏi ngược lại người dùng cho đến khi requirements thực sự rõ ràng.
- **`handoff`**: Đóng gói Context của phiên làm việc hiện tại để bàn giao cho một Agent khác.
- **`tdd`**: Ép AI code theo quy trình Test-Driven Development (Red-Green-Refactor).
- **`diagnosing-bugs`**: Quy trình chẩn đoán lỗi chuyên nghiệp.
- **`improve-codebase-architecture`**: Quét mã nguồn để tìm ra các module cần tái cấu trúc.
- **`to-spec` / `to-tickets`**: Tự động chuyển đổi kế hoạch thành Spec và chia nhỏ thành các Ticket.

## Hướng dẫn sử dụng
Copy các thư mục này vào `~/.gemini/config/skills/` (đối với Antigravity) hoặc thư mục cấu hình tương ứng của Agent bạn đang sử dụng.

### 4. Custom User Skills
- **`shortcut-iphone-skill`**: Kỹ năng chuyên sâu để thao tác, tạo và tùy chỉnh Apple Shortcuts (Phím tắt iPhone) trực tiếp thông qua CLI và cấu hình JSON/PList.
