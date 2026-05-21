# 每日资讯日报 - 定时触发配置说明

## 方案：GitHub Actions 定时触发

已为你配置好 GitHub Actions，每天北京时间 9:00 自动触发日报推送。

---

## 📋 配置步骤

### 第一步：获取扣子服务 URL

1. 在扣子平台上找到你的项目
2. 点击「部署」或查看部署记录
3. 找到 **服务访问地址**（类似 `https://xxx.coze.cn` 或 `https://xxx.aidap-global.cn`）
4. 复制这个地址

### 第二步：推送到 GitHub

1. 在 GitHub 创建一个新仓库（可以是私有仓库）
2. 将项目代码推送上去：

```bash
git init
git add .
git commit -m "每日资讯日报 Agent"
git branch -M main
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

### 第三步：配置 GitHub Secret

1. 打开你的 GitHub 仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 填写：
   - **Name**: `COZE_SERVICE_URL`
   - **Value**: 你在第一步复制的服务地址（如 `https://xxx.coze.cn`）
5. 点击 **Add secret**

### 第四步：启用 GitHub Actions

1. 在仓库中点击 **Actions** 标签
2. 如果看到提示，点击 **I understand my workflows, go ahead and enable them**
3. 找到 **Daily News Report** 工作流
4. 可以点击 **Run workflow** 手动测试一次

---

## ✅ 完成！

配置完成后：
- 每天北京时间 9:00 自动触发
- GitHub Actions 会调用你的扣子服务
- 服务执行日报推送
- 结果可在 Actions 日志中查看

---

## 🔧 手动测试

如果想立即测试，可以：
1. 在 GitHub Actions 页面点击 **Run workflow**
2. 或直接访问服务地址：`https://你的服务地址/trigger/daily_report`

---

## ❓ 常见问题

### Q: GitHub Actions 免费吗？
A: 是的，公开仓库无限制，私有仓库每月 2000 分钟。每天触发一次只消耗约 1 分钟，完全够用。

### Q: 服务地址是什么？
A: 是扣子平台部署后提供的访问地址，在扣子平台的部署记录中可以找到。

### Q: 如果触发失败怎么办？
A: 在 GitHub Actions 日志中查看失败原因，常见问题是服务地址配置错误或服务未部署。
