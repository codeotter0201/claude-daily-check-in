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

### 2. 設定 GitHub Secret
1. 進入儲存庫 **Settings** → **Secrets and variables** → **Actions**
2. 新增 secret: 
   - Name: `CLAUDE_CODE_OAUTH_TOKEN`
   - Value: 你的 OAuth token

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
claude --prompt "執行自動簽到：1) 取得UTC時間 2) 建立/更新當月YYYYMM-log.csv 3) 附加CHECK-IN記錄 4) 提交變更"
```

## 📊 資料格式

簽到記錄存在月度 CSV 檔案 (`YYYYMM-log.csv`):

```csv
timestamp,event_type
2024-08-04T00:00:15Z,CHECK-IN
2024-08-04T05:00:12Z,CHECK-IN
```

## 🛠️ 運作原理

1. **GitHub Actions** 定時觸發 (每天 5 次)
2. **Claude Code Action** 執行簽到邏輯
3. **CSV 檔案** 記錄時間戳記和事件
4. **自動提交** 版本控制所有變更

---

**重點**: 無論 GitHub 或本地，都使用 Claude 來讀取、修改和提交檔案。