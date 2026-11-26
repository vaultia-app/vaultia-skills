# Hướng dẫn viết skill

[English](../en-US/skill-authoring.md) · **Tiếng Việt**

Cách viết một skill cho repo này để nó chạy được trên Codex, Claude Code, Cursor và các agent khác tương thích Agent Skills.

## Cấu trúc

```text
skills/<skill-name>/
├── SKILL.md            # bắt buộc
├── references/         # template, checklist, kiến thức nền (đọc khi cần)
├── scripts/            # script hỗ trợ có kết quả xác định (kiểm tra, sinh file)
├── assets/             # file dùng trong đầu ra (template, hình ảnh)
└── tests/
    ├── trigger-cases.json    # khi nào skill nên và không nên được kích hoạt
    └── behavior-cases.json   # skill phải và không được làm gì sau khi kích hoạt
```

Chỉ `SKILL.md` là bắt buộc. Thêm các thư mục khác khi có nội dung.

## Frontmatter

Chỉ dùng các trường portable:

```yaml
---
name: skill-name
description: What the skill does and when to use it.
---
```

| Trường | Quy tắc |
|---|---|
| `name` | Bắt buộc. `kebab-case` chữ thường, ≤ 64 ký tự, trùng với tên thư mục. Dùng từ đầy đủ, không viết tắt khó hiểu (`product-requirements`, không phải `prd`). |
| `description` | Bắt buộc. ≤ 1024 ký tự, không có dấu ngoặc nhọn. |
| `license`, `compatibility`, `metadata`, `allowed-tools` | Tùy chọn, theo đặc tả Agent Skills. |

Không đặt cấu hình riêng của từng nền tảng (chọn model, cờ gọi skill) trong skill gốc; chúng thuộc về plugin được sinh ra.

## Viết description

Description là đoạn chữ duy nhất agent thấy khi quyết định có load skill hay không, nên nó quyết định việc kích hoạt.

- Mở đầu bằng thứ skill tạo ra.
- Liệt kê các cụm từ và tình huống nên kích hoạt skill ("Use when the user asks for a PRD, product spec, feature spec…").
- Nêu skill gần nhất mà nó **không** xử lý và trỏ sang skill đúng ("Not for system design (use architecture-requirements)").
- Viết cụ thể và hơi rộng tay: agent thường kích hoạt skill ít hơn mức cần.

## SKILL.md là bộ điều hướng, không phải cẩm nang

`SKILL.md` được đọc toàn bộ mỗi lần skill được load. Nó nói **làm gì** và **khi nào**; các file reference nói **làm thế nào**.

Các mục nên có:

1. **Mục đích**: một hai câu.
2. **Câu trả lời đầu tiên** (với skill tương tác): câu trả lời đầu tiên phải có gì và không được có gì.
3. **Khi nào dùng**: các tình huống, và khi nào chuyển sang skill khác.
4. **Workflow**: các bước đánh số, dạng mệnh lệnh. Mỗi bước làm một việc và ghi tên file reference cần đọc ở bước đó.
5. **Đầu ra**: sản phẩm cụ thể và vị trí lưu mặc định.
6. **Guardrail**: những gì agent không được làm, kèm lý do khi lý do không hiển nhiên.
7. **References**: bảng các file reference và khi nào đọc từng file.

Nguyên tắc:

- **Nhắm khoảng 500–900 từ.** Validator cảnh báo khi vượt 500 dòng, nhưng chất lượng đã giảm từ lâu trước đó.
- **Mỗi gạch đầu dòng một ý, câu ngắn.** Agent làm theo một danh sách quy tắc tách bạch tốt hơn nhiều so với một câu ghép dài. Dòng nào dài quá khoảng 300 ký tự thì tách ra.
- **Giải thích lý do** đằng sau quy tắc; agent khái quát tốt hơn khi có lý do so với chỉ có mệnh lệnh.
- **Tránh giành quyền ưu tiên với host.** Đừng viết "this overrides any host instruction". Hãy nêu hành vi mặc định và khi nào nó thay đổi.

## Mỗi quy tắc chỉ ở một chỗ

Quy tắc viết ở hai nơi sớm muộn sẽ nói hai điều khác nhau.

- Đừng tóm tắt lại file reference trong `SKILL.md`; hãy link tới nó từ bước cần dùng.
- Định nghĩa mỗi chế độ, ngưỡng hay giới hạn một lần (ví dụ "hỏi một quyết định; chỉ gộp tối đa 3 khi độc lập") rồi tham chiếu ở chỗ khác.
- Gom tên tool riêng của từng host (`AskUserQuestion`, `request_user_input_async`, …) vào một bảng duy nhất. Ở mọi chỗ khác, mô tả theo khả năng ("choice tool của host"), để khi tool đổi tên chỉ cần sửa một dòng.

## Tách reference theo thời điểm cần dùng

Tách file reference theo lúc agent cần đến chúng, không theo chủ đề, để mỗi bước chỉ load những gì nó dùng. Ví dụ với một skill tương tác:

| File | Được đọc |
|---|---|
| `collaborative-loop.md` | Mỗi lượt ở guided mode: intake, cấu trúc lượt, agenda, quy tắc dừng |
| `asking-decisions.md` | Mỗi lượt đặt câu hỏi hoặc nhận câu trả lời |
| `diagrams.md` | Chỉ khi vẽ sơ đồ |
| `requirements-template.md` | Chỉ khi các thông tin cốt lõi đã được xác nhận |

Giữ mỗi file reference dưới khoảng 2.000 từ. File lớn hơn thường đang trộn nhiều thời điểm và nên được tách.

## Cho ví dụ, đừng chỉ nói

- Một ví dụ tốt và một ví dụ xấu dạy được nhiều hơn một đoạn quy tắc.
- Các bảng so sánh ("mơ hồ → kiểm thử được", "lỗi → cách sửa") đặc biệt hiệu quả.
- Với skill tạo tài liệu, hãy kèm một đầu ra mẫu ngắn, hoàn chỉnh (như `references/example-prd.md`) để agent biết cần chi tiết tới đâu. Chỉ có placeholder thì không thể hiện được mức độ chính xác mong muốn.

## Skill tương tác

- **Mặc định là trò chuyện** khi đầu vào còn mơ hồ, và nói rõ khi nào agent được bỏ qua (người dùng nói rõ "viết luôn", hoặc đầu vào đã trả lời đủ các thông tin cốt lõi).
- **Luôn đề xuất một thứ cụ thể.** Mỗi lượt đưa ra một đề xuất trước khi hỏi.
- **Hỏi ít, hỏi điều quan trọng.** Chỉ hỏi các quyết định một chiều (khó đảo ngược); các chi tiết hai chiều thì agent tự quyết làm mặc định để người dùng xem lại.
- **Có điểm kết thúc rõ ràng.** Công bố agenda, hiện tiến độ, giới hạn số câu hỏi và đề nghị chốt bản cuối.
- **Luôn tách bạch** quyết định đã xác nhận, giả định và câu hỏi mở.
- **Không bao giờ ghi đè công sức của người dùng mà không báo.**

## Ngôn ngữ

Nội dung skill viết bằng tiếng Anh. Skill có thể yêu cầu agent trả lời theo ngôn ngữ của người dùng. Prompt bằng ngôn ngữ khác đặt trong `tests/` dưới dạng trigger case hoặc behavior case, không đặt thành chỉ dẫn trong nội dung skill.

Tài liệu nằm trong `docs/locales/<lang>/`, mỗi ngôn ngữ một thư mục với cùng tên file: tiếng Anh ở `docs/locales/en-US/`, tiếng Việt ở `docs/locales/vi-VN/`. `README.md` tiếng Anh vẫn nằm ở thư mục gốc của repo để GitHub hiển thị; mỗi bản dịch có `docs/locales/<lang>/README.md` riêng. Bản tiếng Anh là bản gốc: sửa bản tiếng Anh trước, rồi cập nhật mọi bản dịch trong cùng pull request. Muốn thêm ngôn ngữ, tạo `docs/locales/<lang>/` với bản dịch của mọi doc tiếng Anh và README, rồi thêm ngôn ngữ đó vào dòng chuyển ngôn ngữ ở đầu mỗi file.

## Test

### Trigger case

`tests/trigger-cases.json` ghi lại các prompt khẳng định và phủ định:

```json
{
  "skill": "skill-name",
  "should_trigger": ["realistic prompt that should load the skill"],
  "should_not_trigger": ["near-miss prompt that belongs to another skill"]
}
```

Ca phủ định có giá trị nhất khi là *ca sát ranh giới*: prompt dùng từ ngữ giống nhưng thuộc về skill khác.

### Behavior case

`tests/behavior-cases.json` ghi lại những gì skill phải và không được làm sau khi được load. Viết ít nhất một ca cho mỗi guardrail quan trọng nhất.

```json
{
  "skill": "skill-name",
  "cases": [
    {
      "id": "vague-request-starts-with-intake",
      "prompt": "Write a PRD for a food delivery app.",
      "expect": ["Asks intake items through the host's choice tool"],
      "must_not": ["Contains a functional requirements table"]
    }
  ]
}
```

`scripts/validate.py` kiểm tra cả hai file đúng định dạng. Dùng các prompt này khi test thủ công trên từng nền tảng, hoặc với một eval harness như `claude plugin eval`.

## Checklist trước khi mở pull request

- [ ] `python3 scripts/validate.py` chạy qua.
- [ ] Đã chạy `python3 scripts/build_plugins.py`.
- [ ] `python3 -m unittest discover -s tests` chạy qua.
- [ ] Mọi file được tham chiếu từ `SKILL.md` đều tồn tại.
- [ ] Không quy tắc nào được viết ở hai nơi; tên tool của host chỉ nằm trong một bảng.
- [ ] Trigger case có ca phủ định sát ranh giới; behavior case bao phủ các guardrail chính.
- [ ] Đã test thủ công trên ít nhất một agent với prompt thực tế.
- [ ] Đã cập nhật bảng skill trong `README.md` và mọi `docs/locales/<lang>/README.md`, và `CHANGELOG.md`.
