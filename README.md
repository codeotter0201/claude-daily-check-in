# Claude Daily Check-in System

自動化每日簽到系統，使用 Claude Code Action 在 GitHub Actions 中執行，每天自動簽到 5 次並記錄到 CSV 檔案。

## 🕐 簽到時間

每天自動執行 5 次簽到 (UTC+8):
- **08:00** - 早上簽到
- **13:00** - 午間簽到  
- **18:00** - 傘後簽到
- **23:00** - 晚間簽到
- **04:00** - 深夜簽到

## 🚀 設定步驟

### 1. 取得 OAuth Token
```bash
claude setup-token
```
複製產生的 `oauth_token_...` 

### 2. 設定 GitHub Secrets
1. 進入儲存庫 **Settings** → **Secrets and variables** → **Actions**
2. 新增 secrets (可設定多個用於備援):
   - Name: `CLAUDE_CODE_OAUTH_TOKEN_1`
   - Value: 你的第一個 OAuth token
   - Name: `CLAUDE_CODE_OAUTH_TOKEN_2` (選用)
   - Value: 你的第二個 OAuth token

### 3. 部署
推送此儲存庫到 GitHub，系統就會自動開始運作。

## 🧪 測試

### GitHub 測試
1. 進入 **Actions** 頁籤
2. 選擇 "Automated Daily Check-in" 工作流程
3. 點擊 **Run workflow** 手動觸發測試

### 本地測試
使用 Claude Code 在本地測試相同邏輯：

```bash
claude --prompt "執行自動簽到：1) 取得UTC時間 2) 建立/更新當月YYYYMM-log.csv 3) 附加CHECK-IN記錄"
```

**注意**: 本地測試只會更新檔案，需手動執行 git 操作：
```bash
git add *.csv
git commit -m "chore: Manual check-in test"
git push
```

## 📊 資料格式

簽到記錄存在月度 CSV 檔案 (`YYYYMM-log.csv`):

```csv
timestamp,event_type,token_id
2024-08-04T00:00:15Z,CHECK-IN,TOKEN_1
2024-08-04T05:00:12Z,CHECK-IN,TOKEN_2
```

## 🛠️ 運作原理

1. **GitHub Actions** 定時觸發 (每天 5 次)
2. **多重 Claude Code Action** 同時執行檔案操作 (建立/更新 CSV)
3. **Token 識別** 每個 token 獨立簽到並標記來源
4. **GitHub Actions** 執行 git 操作 (add, commit, push)
5. **版本控制** 自動記錄所有簽到變更

## 📁 專案結構

```
claude-daily-check-in/
├── .github/
│   └── workflows/
│       └── auto-checkin.yml     # GitHub Actions 工作流程
├── logs/                        # 簽到記錄目錄 (自動生成)
│   ├── 202408-log.csv          # 月度簽到記錄
│   └── 202409-log.csv
├── README.md                    # 專案說明
├── API.md                       # API 文件
└── PRD.md                       # 產品需求文件
```

## 🔧 進階設定

### 自訂簽到時間
修改 `.github/workflows/auto-checkin.yml` 中的 cron 排程：

```yaml
schedule:
  - cron: '0 0,5,10,15,23 * * *'  # 自訂時間 (UTC)
```

### 多重 Token 設定
系統支援多個 Claude Code OAuth tokens 以提高可靠性：

```yaml
# GitHub Secrets 設定
CLAUDE_CODE_OAUTH_TOKEN_1=oauth_token_xxx...
CLAUDE_CODE_OAUTH_TOKEN_2=oauth_token_yyy...
```

**優點:**
- **備援機制**: 單一 token 失效時其他 token 仍可運作
- **負載分散**: 多個 token 同時簽到，提高成功率
- **識別追蹤**: 每筆記錄標記 token 來源

### 環境變數設定
可在 GitHub Secrets 中設定額外變數：
- `TIMEZONE`: 時區設定 (預設: Asia/Taipei)
- `LOG_FORMAT`: 記錄格式 (預設: CSV)

## 🐛 故障排除

### 常見問題

#### 1. OAuth Token 錯誤
```
Error: Could not fetch an OIDC token
```
**解決方案:**
- 確認 GitHub Actions 權限包含 `id-token: write`
- 重新生成 OAuth token: `claude setup-token`
- 檢查 Secret 名稱是否正確: `CLAUDE_CODE_OAUTH_TOKEN_1`, `CLAUDE_CODE_OAUTH_TOKEN_2`
- 至少需要設定一個有效的 token

#### 2. 簽到失敗
**檢查步驟:**
1. 查看 Actions 執行記錄
2. 確認 logs/ 目錄權限
3. 檢查 git 設定是否正確

#### 3. 時間不正確
- 檢查系統時區設定
- GitHub Actions 使用 UTC 時間
- 本地測試時注意時區轉換

### 偵錯指令

```bash
# 檢查 Claude 狀態
claude --version

# 測試 OAuth 連線
claude auth status

# 手動執行簽到邏輯
claude --prompt "執行測試簽到並顯示詳細記錄"
```

## 📈 監控與維護

### 檢查執行狀態
1. **GitHub Actions**: 查看工作流程執行歷史
2. **CSV 檔案**: 確認每月記錄完整性
3. **Commit 歷史**: 檢查自動提交狀況

### 定期維護
- 每月檢查 CSV 檔案格式
- 清理舊的執行記錄
- 更新 OAuth token (依需要)

## 🔒 安全注意事項

- **永不** 在程式碼中硬編碼 token
- 定期輪換 OAuth token
- 使用 GitHub Secrets 儲存敏感資訊
- 限制儲存庫存取權限

## 🤝 貢獻指南

1. Fork 此儲存庫
2. 創建功能分支: `git checkout -b feature/new-feature`
3. 提交變更: `git commit -m 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 提交 Pull Request

## 📝 版本紀錄

### v1.1.0
- 多重 OAuth token 支援
- Token 識別追蹤功能
- 備援機制改善

### v1.0.0
- 基本自動簽到功能
- CSV 記錄格式
- GitHub Actions 整合

---

**重點**: Claude 負責檔案操作，GitHub Actions 負責版本控制操作。

**技術支援**: 如遇問題請查看 [Issues](../../issues) 頁面或提交新問題。