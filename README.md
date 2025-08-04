# Claude Code Session Reset Scheduler

基於 ADR-001 決策的 Claude Code Session 自動重置排程系統。透過 GitHub Actions 在最佳時間點觸發 Claude Code，啟動 5 小時重置倒數，確保在核心工作時段獲得新的 Session 額度。

## 🕐 Session 重置排程

每天自動執行 4 次 Session 重置觸發 (UTC+8)，針對三個核心工作時段優化：

| 觸發時間 | 重置時間 | 目標工作時段 | 說明 |
|:---|:---|:---|:---|
| **05:00** | **10:00** | 08:00-12:00 | 上午工作時段中段重置 |
| **10:00** | **15:00** | 13:00-17:00 | 下午工作時段中段重置 |
| **17:00** | **22:00** | 20:00-00:00 | 晚上工作時段中段重置 |
| **22:00** | **次日 03:00** | 深夜時段 | 額外用量覆蓋 |

## 🚀 設定步驟

### 1. 取得 OAuth Token
```bash
claude setup-token
```
複製產生的 `oauth_token_...` 

### 2. 設定 GitHub Secrets
1. 進入儲存庫 **Settings** → **Secrets and variables** → **Actions**
2. 新增 secrets (建議設定多個用於備援和負載分散):
   - Name: `CLAUDE_CODE_OAUTH_TOKEN_1`
   - Value: 你的第一個 OAuth token
   - Name: `CLAUDE_CODE_OAUTH_TOKEN_2` (強烈建議)
   - Value: 你的第二個 OAuth token

### 3. 部署
推送此儲存庫到 GitHub，系統就會自動開始運作。

## 🧪 測試

### GitHub 測試
1. 進入 **Actions** 頁籤
2. 選擇 "Claude Code Session Reset Scheduler" 工作流程
3. 點擊 **Run workflow** 手動觸發測試

### 本地測試
使用 Claude Code 在本地測試相同邏輯：

```bash
claude --prompt "執行 Session 重置觸發：1) 取得UTC時間 2) 建立/更新當月YYYYMM-session-log.csv 3) 附加SESSION-RESET-TRIGGER記錄"
```

**注意**: 本地測試只會更新檔案，需手動執行 git 操作：
```bash
git add *.csv
git commit -m "chore: Manual session reset trigger test"
git push
```

## 📊 資料格式

Session 重置記錄存在月度 CSV 檔案 (`YYYYMM-session-log.csv`):

```csv
timestamp,event_type,token_id,reset_time_utc8
2024-08-04T02:00:15Z,SESSION-RESET-TRIGGER,TOKEN_1,2024-08-04T15:00:15
2024-08-04T09:00:12Z,SESSION-RESET-TRIGGER,TOKEN_2,2024-08-04T22:00:12
```

## 🛠️ 運作原理

1. **GitHub Actions** 定時觸發 (每天 4 次，基於 ADR-001 決策)
2. **多重 Claude Code Action** 同時執行 Session 重置觸發
3. **5小時倒數啟動** 每次觸發啟動 Claude Code 5小時重置倒數 
4. **智能時間安排** 確保重置時間點對應核心工作時段中段
5. **Token 識別** 每個 token 獨立觸發並標記來源
6. **GitHub Actions** 執行 git 操作 (add, commit, push)
7. **版本控制** 自動記錄所有重置觸發變更

## 📁 專案結構

```
claude-session-reset/
├── .github/
│   └── workflows/
│       └── auto-checkin.yml            # GitHub Actions 工作流程
├── logs/                               # Session 記錄目錄 (自動生成)
│   ├── 202408-session-log.csv         # 月度 Session 重置記錄
│   └── 202409-session-log.csv
├── ADR-001-session-reset-schedule.md  # 架構決策記錄
├── README.md                           # 專案說明
├── API.md                              # API 文件
└── PRD.md                              # 產品需求文件
```

## 🔧 進階設定

### 自訂重置時間
根據 ADR-001 決策，當前最佳排程為：

```yaml
schedule:
  - cron: '0 21,2,9,14 * * *'  # UTC 時間，對應工作時段優化
```

如需調整，請參考 [ADR-001](./ADR-001-session-reset-schedule.md) 了解時間安排原理。

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

#### 2. Session 重置失敗
**檢查步驟:**
1. 查看 Actions 執行記錄
2. 確認 logs/ 目錄權限
3. 檢查 git 設定是否正確
4. 驗證 Claude Code Session 是否正確重置

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

# 手動執行 Session 重置觸發
claude --prompt "執行測試 Session 重置觸發並顯示詳細記錄"

# 檢查 Session 狀態
claude session status
```

## 📈 監控與維護

### 檢查執行狀態
1. **GitHub Actions**: 查看工作流程執行歷史
2. **CSV 檔案**: 確認每月 Session 重置記錄完整性
3. **Commit 歷史**: 檢查自動提交狀況
4. **Session 效果**: 監控實際工作時段的 Session 可用性

### 定期維護
- 每月檢查 CSV 檔案格式
- 清理舊的執行記錄
- 更新 OAuth token (依需要)
- 檢討 Session 重置效果並調整時間安排
- 定期檢視 ADR-001 決策的有效性

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

### v2.0.0
- 重新定位為 Claude Code Session 重置系統
- 基於 ADR-001 的最佳化時間排程
- 針對核心工作時段的智能重置
- 新增 reset_time_utc8 欄位追蹤
- 更新檔案命名規則 (session-log.csv)

### v1.1.0
- 多重 OAuth token 支援
- Token 識別追蹤功能
- 備援機制改善

### v1.0.0
- 基本自動簽到功能
- CSV 記錄格式
- GitHub Actions 整合

---

**重點**: 基於 ADR-001 決策，這是一個針對 Claude Code Session 重置優化的自動化系統，確保在核心工作時段獲得最佳的 Session 可用性。

**技術支援**: 如遇問題請查看 [Issues](../../issues) 頁面或提交新問題。