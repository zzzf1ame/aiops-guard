# 推送到 GitHub 的步骤

## 方法 1：GitHub Desktop（推荐）

1. 在 GitHub Desktop 中，点击顶部菜单 `Repository` → `Repository settings...`
2. 删除当前的 origin remote
3. 点击 `Repository` → `Publish repository`
4. 填写信息后点击 `Publish repository`

## 方法 2：命令行

### 步骤 1：在 GitHub 网站创建新仓库
1. 访问 https://github.com/new
2. Repository name: `aiops-guard`
3. Description: `Lightweight Python library for monitoring LLM calls with automatic cost tracking`
4. 选择 Public
5. 不要勾选任何初始化选项（README, .gitignore, license）
6. 点击 `Create repository`

### 步骤 2：推送本地代码
复制 GitHub 显示的仓库 URL（类似 https://github.com/你的用户名/aiops-guard.git）

然后在命令行执行：

```bash
cd aiops-guard

# 删除旧的 remote
git remote remove origin

# 添加新的 remote（替换成你的实际 URL）
git remote add origin https://github.com/你的用户名/aiops-guard.git

# 推送代码
git push -u origin master
```

## 验证
推送成功后，访问你的仓库页面应该能看到所有文件和 README。
