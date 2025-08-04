## Automated Daily Check-in System: Product Requirements Document (PRD)

| Version | Date       | Author | Change Description |
| ------- | ---------- | ------ | ------------------ |
| v1.0    | 2023-10-27 | Claude | Initial Draft      |

### 1. Project Overview

This project aims to build a fully automated, scheduled daily check-in system. The system will leverage **GitHub Actions** as a scheduling trigger and the **Claude Code Action** to execute the core check-in logic. All check-in records will be stored in a CSV file within a designated GitHub repository, creating an unattended and automated attendance log.

### 2. Goals & Objectives

- **Automation:** Completely eliminate the manual check-in process by automatically performing "check-in" actions at specified times.
- **Reliability:** Ensure the system runs on time, every day, and logs information correctly and consistently.
- **Traceability:** Maintain a clear and auditable history of all check-in activities, as each log entry will be a version-controlled commit in the GitHub repository.
- **Simplicity:** Focus exclusively on the "check-in" function, avoiding unnecessary complexity from other features.

### 3. Functional Requirements

| ID       | Requirement Description                                                                                                                                                                                                                                                                                                     | Priority |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| **FR-1** | **Scheduled Trigger**<br>The system must execute automatically at five specified times each day. The target times are: `08:00`, `13:00`, `18:00`, `23:00`, and `04:00` (in UTC+8 timezone).<br>_(Technical Note: The GitHub Actions cron schedule will be configured using UTC.)_                                           | High     |
| **FR-2** | **Log File Management**<br>1. Check-in records must be stored in a CSV file.<br>2. The file must follow the naming convention `YYYYMM-log.csv` (e.g., `202310-log.csv`).<br>3. The system must automatically identify the correct file for the current month. If the file does not exist, it must be created automatically. | High     |
| **FR-3** | **Data Logging**<br>1. On each run, Claude must read the current month's CSV file and append a new row for the check-in record.<br>2. The CSV columns must be: `timestamp`, `event_type`.<br>3. Example row: `2023-10-27T08:00:15Z,CHECK-IN`. The timestamp must be in ISO 8601 UTC format to prevent timezone ambiguity.   | High     |
| **FR-4** | **Version Control Integration**<br>1. After Claude updates the CSV file, GitHub Actions must automatically add, commit and push the changes to the `main` branch.<br>2. The commit message should be descriptive, e.g., `chore: Automated check-in at 2023-10-27T08:00:15Z`.                                  | High     |
| **FR-5** | **Authentication**<br>The system must use a `CLAUDE_CODE_OAUTH_TOKEN` stored in GitHub Secrets to authenticate the Claude Code Action.                                                                                                                                                                                      | High     |

### 4. Non-Functional Requirements

| ID        | Requirement Description                                                                                                                         |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **NFR-1** | **Security**<br>The `CLAUDE_CODE_OAUTH_TOKEN` must never be hard-coded in the workflow file and must always be referenced via GitHub Secrets.   |
| **NFR-2** | **Maintainability**<br>The GitHub Actions workflow file (`.github/workflows/auto-checkin.yml`) should be well-commented for future maintenance. |
| **NFR-3** | **Performance**<br>Each check-in action should complete within a few minutes to stay well within the execution limits of GitHub Actions.        |

### 5. Technical Implementation Plan

1.  **Create Workflow File**: Create a new YAML file at `.github/workflows/auto-checkin.yml` in the repository.

2.  **Configure Cron Trigger**:

    - Use `on.schedule.cron` to define the daily execution schedule. The UTC+8 times must be converted to UTC for the cron job:
      - `08:00 (UTC+8)` -> `00:00 (UTC)`
      - `13:00 (UTC+8)` -> `05:00 (UTC)`
      - `18:00 (UTC+8)` -> `10:00 (UTC)`
      - `23:00 (UTC+8)` -> `15:00 (UTC)`
      - `04:00 (UTC+8)` -> `20:00 (UTC)`
    - The resulting cron expression will be: `'0 0,5,10,15,20 * * *'`

3.  **Configure Claude Code Action**:

    - Use the action `anthropics/claude-code-action@beta`.
    - Set `mode: agent` for this automated, non-interactive task.
    - Set `claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}`.
    - Use the `direct_prompt` input to provide clear instructions to Claude.

4.  **Design Separation of Concerns**:
    - **Claude Code Action**: Handles only file operations (read/write CSV files)
    - **GitHub Actions**: Handles all git operations (add, commit, push)
    
    The `direct_prompt` will contain the following instructions for Claude:
    ```
    1. Get the current UTC time.
    2. Based on the current date, determine the log filename in the format 'YYYYMM-log.csv'.
    3. Check if this file exists. If it does not, create it and write the header 'timestamp,event_type'.
    4. Append a new line to the file with current UTC timestamp in ISO 8601 format and 'CHECK-IN'.
    IMPORTANT: Only perform file operations. Do NOT run git commands.
    ```
    
    GitHub Actions will then handle:
    ```
    1. git add *.csv
    2. git commit -m "chore: Automated check-in at [timestamp]"
    3. git push origin main
    ```

### 6. Out of Scope

The following features are explicitly **not** included in this project:

- "Check-out" functionality.
- Logging complex attendance states (e.g., leave, overtime, vacation).
- Generation of timesheets or statistical reports.
- A graphical user interface (UI).
- Any event types other than `CHECK-IN`.

---
