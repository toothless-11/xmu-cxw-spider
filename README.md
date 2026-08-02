
# 📧 厦大科创比赛监控 / XMU Competition Monitor

自动监控厦门大学本科生创新网，发现新比赛时邮件提醒。

---

## 🚀 如何使用 / How to Use

### 1️⃣ 配置 Secrets

仓库 → **Settings** → **Secrets and variables** → **Actions** → 添加：

| Secret | 说明 |
|--------|------|
| `MAIL_USER` | 你的QQ邮箱 |
| `MAIL_PASS` | QQ邮箱授权码（不是密码） |
| `MAIL_RECIPIENTS` | 收件人邮箱(逗号分隔) |
### 2️⃣ 开启 Actions

仓库 → **Actions** → 找到 **Monitor** → 点击 **"I understand my workflows, go ahead and enable them"**

### 3️⃣ 完事

- 定时自动运行：**每天8:00和20:00**（北京时间）
- 想立即测试：Actions → Monitor → **Run workflow**

---

## 📁 文件说明

| 文件 | 作用 |
|------|------|
| `.github/workflows/monitor.yml` | Actions配置 |
| `monitor.py` | 监控脚本 |
| `notified_ids.txt` | 已通知记录（自动维护） |

---

## ❓ 常见问题

**收不到邮件？**
- 检查Secrets配置是否正确
- 查看垃圾邮件箱
- 看Actions运行日志

**重复收到通知？**
- 检查 `notified_ids.txt` 是否正常提交到仓库
