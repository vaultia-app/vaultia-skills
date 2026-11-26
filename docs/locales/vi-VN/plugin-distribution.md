# Phân phối plugin

[English](../en-US/plugin-distribution.md) · **Tiếng Việt**

Skill gốc trong `skills/` được `scripts/build_plugins.py` đóng gói cho từng nền tảng. Plugin và marketplace có được commit để các nền tảng cài thẳng từ GitHub. **Không bao giờ sửa tay file được sinh ra**: sửa `skills/` rồi build lại.

## Những gì được build

| Đầu ra | Có commit | Nền tảng | Mục đích |
|---|---|---|---|
| `.claude-plugin/marketplace.json` | Có | Claude Code | Marketplace liệt kê mọi plugin |
| `plugins/claude/<plugin>/` | Có | Claude Code | Plugin để cài |
| `.agents/plugins/marketplace.json` | Có | Codex CLI, ChatGPT | Marketplace liệt kê mọi plugin |
| `plugins/openai/<plugin>/` | Có | Codex CLI, ChatGPT | Plugin để cài, kèm icon thương hiệu |
| `dist/skills/<skill>.zip` | Không (đính kèm release là `<skill>-skill.zip`) | claude.ai | Upload từng skill |
| `dist/plugins/<plugin>.zip` | Không (đính kèm release là `<plugin>-plugin.zip`) | ChatGPT, Claude Desktop | Upload plugin |

| Plugin | Gồm |
|---|---|
| `product-requirements` | `product-requirements` |
| `architecture-requirements` | `architecture-requirements` |
| `vaultia-skills` (tên hiển thị "Vaultia", file zip `vaultia.zip`) | mọi skill |

Thư mục `tests/` của skill không được đưa vào plugin và zip.

```bash
python3 scripts/build_plugins.py          # sinh lại plugin + marketplace
python3 scripts/build_plugins.py --zip    # build thêm dist/skills/*.zip và dist/plugins/*.zip
python3 scripts/build_plugins.py --check  # CI: fail nếu file sinh ra đã cũ
```

Version của plugin lấy từ `version` trong `pyproject.toml`. Hãy tăng version mỗi lần release: các nền tảng cache plugin theo version nên có thể không nhận thay đổi nếu version giữ nguyên.

## Claude Code

```bash
claude plugin marketplace add vaultia-app/vaultia-skills
claude plugin install vaultia-skills@vaultia-skills          # tất cả skill
claude plugin install product-requirements@vaultia-skills    # hoặc một skill
```

Trong session cũng dùng được `/plugin marketplace add …` và `/plugin install …`. Skill có tiền tố theo tên plugin, ví dụ `/vaultia-skills:product-requirements`.

Team có thể cấu hình sẵn marketplace trong `.claude/settings.json` của project:

```json
{
  "extraKnownMarketplaces": {
    "vaultia-skills": { "source": { "source": "github", "repo": "vaultia-app/vaultia-skills" } }
  },
  "enabledPlugins": { "vaultia-skills@vaultia-skills": true }
}
```

**Cập nhật** sau khi có bản mới: `claude plugin marketplace update vaultia-skills`, rồi mở session mới.

**Thử bản local** trước khi push: chạy `claude plugin marketplace add ./` ở thư mục gốc của repo.

Kiểm tra trước khi publish:

```bash
claude plugin validate .                              # marketplace
claude plugin validate plugins/claude/vaultia-skills  # một plugin
```

## Codex CLI

```bash
codex plugin marketplace add vaultia-app/vaultia-skills
codex plugin list
codex plugin add vaultia-skills@vaultia-skills
```

Mở session Codex mới sau khi cài. Cập nhật bằng `codex plugin marketplace upgrade vaultia-skills`.

## ChatGPT

ChatGPT đọc cùng định dạng plugin với Codex:

1. **Ứng dụng máy tính:** thêm marketplace bằng `codex plugin marketplace add …`, cài từ mục **Plugins**, rồi mở chat mới.
2. **Upload:** upload `vaultia-plugin.zip` từ trang release (hoặc `dist/plugins/vaultia.zip` khi tự build).
3. **Workspace (Business / Enterprise / Edu):** admin có thể import marketplace GitHub này trong phần cài đặt plugin của workspace.
4. **Đăng công khai:** gửi qua cổng đăng ký plugin của OpenAI (cần giấy phép, chính sách quyền riêng tư và qua kiểm duyệt).

Khả năng dùng skill khác nhau theo gói ChatGPT và nền tảng; hãy xem tài liệu hiện tại của OpenAI.

## claude.ai (web, desktop, mobile)

Upload từng file `<skill>-skill.zip` từ trang release (hoặc `dist/skills/<skill>.zip` khi tự build) ở **Settings → Capabilities → Skills → Upload skill**. Mỗi zip chứa một thư mục `<skill-name>/` với `SKILL.md` ở trên cùng. Muốn cập nhật thì xóa skill cũ rồi upload zip mới.

## Checklist phát hành

Bản phát hành được [workflow Release](../../../.github/workflows/release.yml) tạo tự động khi bạn push một tag version.

1. Tăng `version` trong `pyproject.toml` và badge release trong mọi README (có test kiểm tra hai chỗ này khớp nhau).
2. Trong `CHANGELOG.md`, chuyển các mục *Unreleased* xuống một tiêu đề mới `## [X.Y.Z] - YYYY-MM-DD`. Phần này sẽ thành release notes.
3. Chạy kiểm tra ở máy:
   ```bash
   python3 scripts/validate.py
   python3 scripts/build_plugins.py
   python3 -m unittest discover -s tests
   ```
4. Commit `skills/`, `plugins/`, hai file `marketplace.json` và docs lên một nhánh, mở pull request, rồi merge khi CI qua. Nhánh `main` được bảo vệ nên không push thẳng được (xem `.github/rulesets/`).
5. Cập nhật `main` ở máy, rồi tạo tag và push tag (chỉ admin của repo mới tạo được tag `v*`):
   ```bash
   git switch main && git pull
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

Sau đó workflow kiểm tra tag khớp với `pyproject.toml` và `CHANGELOG.md` có phần cho version đó, chạy validate và test, build file zip, rồi tạo GitHub Release kèm file zip với tên `<skill>-skill.zip` và `<plugin>-plugin.zip` (vì zip skill và zip plugin trùng tên trong `dist/`). Push lại cùng tag (sau khi xóa tag cũ) sẽ cập nhật release đã có.

Xem trước release notes ở máy bằng `python3 scripts/release_notes.py X.Y.Z`.
