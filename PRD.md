## Claude Code Session Reset Scheduler: Product Requirements Document (PRD)

| Version | Date       | Author | Change Description |
| ------- | ---------- | ------ | ------------------ |
| v3.0    | 2025-08-04 | Claude | Updated for session reset system with timing optimization |
| v2.0    | 2024-08-04 | Claude | Transformed to session reset system per ADR-001 |
| v1.0    | 2023-10-27 | Claude | Initial check-in system draft |

### 1. Project Overview

This project provides a fully automated Claude Code Session reset scheduling system. The system leverages **GitHub Actions** with reliability-optimized cron timing and **Claude Code Action** to execute session reset triggers. Based on ADR-001 and ADR-002 decisions, the system ensures optimal Session quota availability during core work periods through strategic 5-hour countdown triggers. All session reset records are stored in monthly CSV files within the GitHub repository.

### 2. Goals & Objectives

- **Automated Session Management:** Eliminate manual Claude Code Session monitoring by automatically triggering resets at optimal times for core work periods.
- **Reliability:** Ensure consistent execution through GitHub Actions cron timing optimization (minute 23) and multi-token backup mechanisms.
- **Work Period Optimization:** Provide fresh Session quotas during mid-work periods (10:23, 15:23, 22:23 UTC+8) to prevent workflow interruptions.
- **Traceability:** Maintain comprehensive session reset history through version-controlled CSV logs and commit tracking.

### 3. Functional Requirements

| ID       | Requirement Description                                                                                                                                                                                                                                                                                                     | Priority |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| **FR-1** | **Scheduled Trigger**<br>The system must execute automatically at four specified times each day with reliability optimization. The target times are: `05:23`, `10:23`, `17:23`, `22:23` (in UTC+8 timezone) to trigger 5-hour countdowns.<br>_(Technical Note: Uses minute 23 per ADR-002 for improved GitHub Actions reliability.)_ | High     |
| **FR-2** | **Log File Management**<br>1. Session reset records must be stored in monthly CSV files.<br>2. The file must follow the naming convention `YYYYMM-session-log.csv` (e.g., `202408-session-log.csv`).<br>3. The system must automatically identify the correct file for the current month. If the file does not exist, it must be created automatically. | High     |
| **FR-3** | **Data Logging**<br>1. On each run, Claude must read the current month's CSV file and append a new row for the session reset trigger.<br>2. The CSV columns must be: `timestamp`, `event_type`, `token_id`, `reset_time_utc8`.<br>3. Example row: `2024-08-04T02:23:15Z,SESSION-RESET-TRIGGER,TOKEN_1,2024-08-04T15:23:15`. The timestamp must be in ISO 8601 UTC format. | High     |
| **FR-4** | **Version Control Integration**<br>1. After Claude updates the CSV file, GitHub Actions must automatically add, commit and push the changes to the `main` branch.<br>2. The commit message should be descriptive, e.g., `chore(bot): Session reset trigger at 2024-08-04T02:23:15Z`.                        | High     |
| **FR-5** | **Authentication**<br>The system must support multiple Claude Code OAuth tokens for redundancy and load distribution. Tokens are stored with suffixes (e.g., `CLAUDE_CODE_OAUTH_TOKEN_1`, `CLAUDE_CODE_OAUTH_TOKEN_2`) in GitHub Secrets. Each available token will perform independent session reset triggers. | High     |

### 4. Non-Functional Requirements

| ID        | Requirement Description                                                                                                                         |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **NFR-1** | **Security**<br>All `CLAUDE_CODE_OAUTH_TOKEN` variants must never be hard-coded in the workflow file and must always be referenced via GitHub Secrets.   |
| **NFR-2** | **Maintainability**<br>The GitHub Actions workflow file (`.github/workflows/auto-checkin.yml`) should be well-commented for future maintenance. |
| **NFR-3** | **Performance**<br>Each check-in action should complete within a few minutes to stay well within the execution limits of GitHub Actions.        |

### 5. Technical Implementation Plan

1.  **Create Workflow File**: Create a new YAML file at `.github/workflows/auto-checkin.yml` in the repository.

2.  **Configure Cron Trigger**:

    - Use `on.schedule.cron` to define the session reset trigger schedule. The UTC+8 times are converted to UTC with minute 23 optimization:
      - `05:23 (UTC+8)` -> `21:23 (UTC, previous day)`
      - `10:23 (UTC+8)` -> `02:23 (UTC)`
      - `17:23 (UTC+8)` -> `09:23 (UTC)`
      - `22:23 (UTC+8)` -> `14:23 (UTC)`
    - The resulting cron expression will be: `'23 21,2,9,14 * * *'` (per ADR-002 timing optimization)

3.  **Configure Claude Code Action**:

    - Use the action `anthropics/claude-code-action@beta`.
    - Set `mode: agent` for this automated, non-interactive task.
    - Create separate steps for each token: `CLAUDE_CODE_OAUTH_TOKEN_1`, `CLAUDE_CODE_OAUTH_TOKEN_2`, etc.
    - Use conditional execution to only run steps where tokens exist.
    - Use the `direct_prompt` input to provide clear instructions to Claude.

4.  **Design Separation of Concerns**:
    - **Claude Code Action**: Handles only file operations (read/write CSV files)
    - **GitHub Actions**: Handles all git operations (add, commit, push)
    
    The `direct_prompt` will contain the following instructions for Claude:
    ```
    1. Get the current UTC time and determine today's date.
    2. Based on the current date, determine the log filename in the format 'YYYYMM-session-log.csv'.
    3. Check if this file exists. If it does not, create it and write the header 'timestamp,event_type,token_id,reset_time_utc8'.
    4. Calculate the expected session reset time (current time + 5 hours, converted to UTC+8).
    5. Append a new line with: current UTC timestamp, 'SESSION-RESET-TRIGGER', token identifier, and expected UTC+8 reset time.
    IMPORTANT: Only perform file operations. Do NOT run git commands.
    ```
    
    GitHub Actions will then handle:
    ```
    1. git add *.csv
    2. git commit -m "chore(bot): Session reset trigger at [timestamp]"
    3. git push origin main
    ```

### 6. Out of Scope

The following features are explicitly **not** included in this project:

- Traditional check-in/check-out functionality.
- Attendance tracking or timesheet generation.
- Statistical reports or analytics dashboards.
- A graphical user interface (UI).
- Any event types other than `SESSION-RESET-TRIGGER`.
- Direct Claude Code session monitoring (the system only triggers resets).
- Real-time session status checking or alerts.

### 7. References

- [ADR-001: Session Reset Scheduling](./ADR-001-session-reset-schedule.md) - Architecture decision record for work period optimization
- [ADR-002: GitHub Actions Cron Timing Optimization](./ADR-002-github-actions-cron-timing-optimization.md) - Reliability enhancement decision
- Core work periods: 08:00-12:00, 13:00-17:00, 20:00-00:00 (UTC+8)
- Claude Code session reset behavior: 5-hour countdown from first trigger
- Timing optimization: Minute 23 for improved GitHub Actions reliability

---
