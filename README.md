# Claude Code Session Reset Scheduler

An automated Claude Code Session reset scheduling system based on ADR-001 decision. Uses GitHub Actions to trigger Claude Code at optimal times, starting a 5-hour reset countdown to ensure new Session quotas during core working hours.

## 🕐 Session Reset Schedule

Automatically executes 4 session reset triggers daily (UTC+8), optimized for three core working periods:

| Trigger Time | Reset Time | Target Work Period | Description |
|:---|:---|:---|:---|
| **05:00** | **10:00** | 08:00-12:00 | Mid-morning work period reset |
| **10:00** | **15:00** | 13:00-17:00 | Mid-afternoon work period reset |
| **17:00** | **22:00** | 20:00-00:00 | Mid-evening work period reset |
| **22:00** | **Next day 03:00** | Late night period | Additional usage coverage |

## 🚀 Setup Steps

### 1. Get OAuth Token

```bash
claude setup-token
```

Copy the generated `oauth_token_...`

### 2. Configure GitHub Secrets

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Add secrets (recommend setting multiple for backup and load distribution):
   - Name: `CLAUDE_CODE_OAUTH_TOKEN_1`
   - Value: Your first OAuth token
   - Name: `CLAUDE_CODE_OAUTH_TOKEN_2` (strongly recommended)
   - Value: Your second OAuth token

### 3. Deploy

Push this repository to GitHub, and the system will automatically start working.

## 🧪 Testing

### GitHub Testing

1. Go to **Actions** tab
2. Select "Claude Code Session Reset Scheduler" workflow
3. Click **Run workflow** to manually trigger test

### Local Testing

Use Claude Code to test the same logic locally:

```bash
claude --prompt "Execute Session reset trigger: 1) Get UTC time 2) Create/update current month YYYYMM-session-log.csv 3) Append SESSION-RESET-TRIGGER record"
```

**Note**: Local testing only updates files, manual git operations required:

```bash
git add *.csv
git commit -m "chore: Manual session reset trigger test"
git push
```

## 📊 Data Format

Session reset records are stored in monthly CSV files (`YYYYMM-session-log.csv`):

```csv
timestamp,event_type,token_id,reset_time_utc8
2024-08-04T02:00:15Z,SESSION-RESET-TRIGGER,TOKEN_1,2024-08-04T15:00:15
2024-08-04T09:00:12Z,SESSION-RESET-TRIGGER,TOKEN_2,2024-08-04T22:00:12
```

## 🛠️ How It Works

1. **GitHub Actions** scheduled triggers (4 times daily, based on ADR-001 decision)
2. **Multiple Claude Code Actions** execute session reset triggers simultaneously
3. **5-hour countdown activation** Each trigger starts Claude Code 5-hour reset countdown
4. **Smart time scheduling** Ensures reset times correspond to mid-core working periods
5. **Token identification** Each token triggers independently and marks source
6. **GitHub Actions** executes git operations (add, commit, push)
7. **Version control** Automatically records all reset trigger changes

## 📁 Project Structure

```
claude-session-reset/
├── .github/
│   └── workflows/
│       └── auto-checkin.yml            # GitHub Actions workflow
├── logs/                               # Session log directory (auto-generated)
│   ├── 202408-session-log.csv         # Monthly session reset records
│   └── 202409-session-log.csv
├── ADR-001-session-reset-schedule.md  # Architecture decision record
├── README.md                           # Project documentation
├── API.md                              # API documentation
└── PRD.md                              # Product requirements document
```

## 🔧 Advanced Configuration

### Custom Reset Times

Based on ADR-001 decision, current optimal schedule:

```yaml
schedule:
  - cron: '0 21,2,9,14 * * *'  # UTC time, optimized for work periods
```

For adjustments, refer to [ADR-001](./ADR-001-session-reset-schedule.md) to understand the timing principles.

### Multiple Token Configuration

System supports multiple Claude Code OAuth tokens for improved reliability:

```yaml
# GitHub Secrets configuration
CLAUDE_CODE_OAUTH_TOKEN_1=oauth_token_xxx...
CLAUDE_CODE_OAUTH_TOKEN_2=oauth_token_yyy...
```

**Benefits:**
- **Backup mechanism**: Other tokens continue working if one fails
- **Load distribution**: Multiple tokens check in simultaneously, improving success rate
- **Identification tracking**: Each record marks token source

### Environment Variables

Additional variables can be set in GitHub Secrets:
- `TIMEZONE`: Timezone setting (default: Asia/Taipei)
- `LOG_FORMAT`: Log format (default: CSV)

## 🐛 Troubleshooting

### Common Issues

#### 1. OAuth Token Error

```
Error: Could not fetch an OIDC token
```

**Solutions:**
- Ensure GitHub Actions permissions include `id-token: write`
- Regenerate OAuth token: `claude setup-token`
- Check Secret names are correct: `CLAUDE_CODE_OAUTH_TOKEN_1`, `CLAUDE_CODE_OAUTH_TOKEN_2`
- At least one valid token must be configured

#### 2. Session Reset Failure

**Check steps:**
1. Review Actions execution logs
2. Confirm logs/ directory permissions
3. Check git configuration is correct
4. Verify Claude Code Session resets properly

#### 3. Incorrect Time

- Check system timezone settings
- GitHub Actions uses UTC time
- Be aware of timezone conversion during local testing

### Debug Commands

```bash
# Check Claude status
claude --version

# Test OAuth connection
claude auth status

# Manually execute Session reset trigger
claude --prompt "Execute test Session reset trigger and show detailed logs"

# Check Session status
claude session status
```

## 📈 Monitoring & Maintenance

### Check Execution Status

1. **GitHub Actions**: Review workflow execution history
2. **CSV Files**: Confirm monthly session reset record integrity
3. **Commit History**: Check automatic commit status
4. **Session Effects**: Monitor actual work period session availability

### Regular Maintenance

- Monthly CSV file format checks
- Clean old execution logs
- Update OAuth tokens (as needed)
- Review session reset effects and adjust timing
- Regularly review ADR-001 decision effectiveness

## 🔒 Security Considerations

- **Never** hardcode tokens in code
- Regularly rotate OAuth tokens
- Use GitHub Secrets for sensitive information
- Restrict repository access permissions

## 🤝 Contributing

1. Fork this repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push branch: `git push origin feature/new-feature`
5. Submit Pull Request

## 📝 Version History

### v2.0.0

- Repositioned as Claude Code Session reset system
- Optimized time scheduling based on ADR-001
- Smart reset for core work periods
- Added reset_time_utc8 field tracking
- Updated file naming convention (session-log.csv)

### v1.1.0

- Multiple OAuth token support
- Token identification tracking feature
- Improved backup mechanism

### v1.0.0

- Basic auto check-in functionality
- CSV log format
- GitHub Actions integration

---

**Key Point**: Based on ADR-001 decision, this is an automated system optimized for Claude Code Session resets, ensuring optimal Session availability during core working hours.

**Technical Support**: For issues, please check the [Issues](../../issues) page or submit new issues.