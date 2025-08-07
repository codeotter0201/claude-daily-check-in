# Claude Code Session Reset Scheduler

An automated Claude Code Session reset scheduling system based on ADR-001, ADR-002, and ADR-003 decisions. Uses GitHub Actions to trigger Claude Code at optimal times with reliability-optimized scheduling, starting a 5-hour reset countdown to ensure new Session quotas during core working hours. Includes a simple Q&A health check feature for basic functionality verification.

## 🕐 Session Reset Schedule

Automatically executes 4 session reset triggers daily (UTC+8), optimized for three core working periods:

| Trigger Time | Reset Time         | Target Work Period | Description                     |
| :----------- | :----------------- | :----------------- | :------------------------------ |
| **05:23**    | **10:00**          | 08:00-12:00        | Mid-morning work period reset   |
| **10:23**    | **15:00**          | 13:00-17:00        | Mid-afternoon work period reset |
| **17:23**    | **22:00**          | 20:00-00:00        | Mid-evening work period reset   |
| **22:23**    | **Next day 03:00** | Late night period  | Additional usage coverage       |

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

#### Method 1: Using Python Script Directly

Test the Q&A logging functionality locally:

```bash
# Using uv (recommended)
uv run --python 3.13 python src/log_qa_check.py --token TOKEN_1

# Or using system Python
python3 src/log_qa_check.py --token TOKEN_2
```

#### Method 2: Using Claude Code with Prompt

Simulate the GitHub Actions workflow locally:

```bash
# Simple Q&A test
claude -p "1+1=?"

# Then run the logging script
uv run --python 3.13 python src/log_qa_check.py --token TOKEN_1
```

#### Method 3: Complete Simulation

Test the complete workflow locally:

```bash
# Step 1: Ask Claude the Q&A question
claude -p "1+1=? # Answer should be 2. Do not answer anything else."

# Step 2: Log the Q&A session reset trigger
uv run --python 3.13 python src/log_qa_check.py --token TOKEN_1

# Step 3: Check the generated CSV file
cat logs/$(date +%Y%m)-session-log.csv
```

**Note**: Local testing only updates files, manual git operations required:

```bash
git add logs/*.csv
git commit -m "chore: Manual Q&A session reset trigger test"
git push
```

## 📊 Data Format

Session reset records are stored in monthly CSV files (`logs/YYYYMM-session-log.csv`):

```csv
timestamp,event_type,token_id,reset_time_utc8
2025-08-04 05:24:27,SESSION-RESET-TRIGGER,TOKEN_1,2025-08-04 18:24:27
2025-08-07 15:00:29,SESSION-RESET-TRIGGER,TOKEN_2,2025-08-07 23:00:29
```

**Event Types:**

- `SESSION-RESET-TRIGGER`: Traditional session reset countdown activation
- `SESSION-RESET-TRIGGER`: Integrated Q&A health check + session reset (ADR-003)

**CSV Format:**

- `timestamp`: UTC time in `YYYY-MM-DD HH:MM:SS` format
- `event_type`: Event classification
- `token_id`: TOKEN_1 or TOKEN_2 identifier
- `reset_time_utc8`: Expected session reset time in UTC+8 timezone

## 🛠️ How It Works

1. **GitHub Actions** scheduled triggers (4 times daily, based on ADR-001 decision)
2. **Integrated Q&A Check** Asks Claude "1+1=?" with minimal response requirement (ADR-003)
3. **Python Function** (`src/log_qa_check.py`) logs SESSION-RESET-TRIGGER to monthly CSV in logs/ directory
4. **Time Calculation** Automatically calculates expected reset time (current UTC + 8 hours)
5. **Token Identification** Maps OAuth tokens to TOKEN_1/TOKEN_2 identifiers
6. **5-hour countdown activation** Each trigger starts Claude Code 5-hour reset countdown
7. **Smart time scheduling** Ensures reset times correspond to mid-core working periods
8. **GitHub Actions** executes git operations (add, commit, push)
9. **Version control** Automatically records all integrated Q&A session reset triggers

## 📁 Project Structure

```
claude-daily-check-in/
├── .github/
│   └── workflows/
│       └── auto-checkin.yml            # GitHub Actions workflow
├── src/
│   └── log_qa_check.py                 # Q&A session reset trigger logging script
├── logs/                               # Session log directory (auto-generated)
│   ├── 202408-session-log.csv         # Monthly session reset records
│   └── 202409-session-log.csv
├── ADR-001-session-reset-schedule.md  # Architecture decision record
├── ADR-002-github-actions-cron-timing-optimization.md  # Timing optimization ADR
├── ADR-003-simple-qa-logging-feature.md  # Q&A health check ADR
├── pyproject.toml                      # uv/Python project configuration
├── README.md                           # Project documentation
├── API.md                              # API documentation
└── PRD.md                              # Product requirements document
```

## 🔧 Advanced Configuration

### Custom Reset Times

Based on ADR-001 decision, current optimal schedule:

```yaml
schedule:
  - cron: "23 21,2,9,14 * * *" # UTC time, optimized for reliability and work periods
```

For adjustments, refer to [ADR-001](./ADR-001-session-reset-schedule.md) for timing principles, [ADR-002](./ADR-002-github-actions-cron-timing-optimization.md) for reliability optimization, and [ADR-003](./ADR-003-simple-qa-logging-feature.md) for Q&A health check feature.

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

# Test Q&A functionality locally
claude -p "1+1=?"

# Run local Q&A session reset trigger
uv run --python 3.13 python src/log_qa_check.py --token TOKEN_1

# Manually execute Session reset trigger
claude -p "Execute test Session reset trigger and show detailed logs"

# Check Session status
claude session status
```

## 📈 Monitoring & Maintenance

### Check Execution Status

1. **GitHub Actions**: Review workflow execution history
2. **CSV Files**: Confirm monthly session reset record integrity in logs/ directory
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

### v2.2.0

- Implemented ADR-003: Integrated Q&A-Session-Reset-Trigger feature
- Combined Q&A health check with session reset trigger logging
- Python script (`src/log_qa_check.py`) with uv support and proper directory structure
- Enhanced CSV format with calculated reset times (UTC+8)
- Local testing capabilities with direct Python script execution

### v2.1.0

- Implemented ADR-002: GitHub Actions cron timing optimization
- Changed trigger time from :00 to :23 minutes for improved reliability
- Updated all timing references to reflect 23-minute offset
- Enhanced documentation with reliability considerations

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

**Key Point**: Based on ADR-001, ADR-002, and ADR-003 decisions, this is an automated system optimized for Claude Code Session resets with reliability-enhanced scheduling and health checking, ensuring optimal Session availability during core working hours.

**Technical Support**: For issues, please check the [Issues](../../issues) page or submit new issues.
