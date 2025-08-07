# ADR-003: Simple Q&A Logging Feature

## Status

Accepted

## Context

The current Claude Code Session Reset Scheduler successfully triggers session resets and logs the events. There's a need to add a simple verification mechanism that combines health checking with session reset triggering:

1. Asks Claude a simple question ("1+1=?")
2. Expects the simplest possible answer ("2")
3. Combines this health check with session reset trigger logging

This integrated approach provides:

- A simple health check to verify Claude is responding correctly
- Minimal token usage with the simplest possible interaction
- Unified logging that combines health check and session reset trigger
- Eliminates separate Q&A check events

## Decision

We will implement an integrated Q&A-Session-Reset-Trigger feature that:

1. **Asks a simple mathematical question**: "1+1=?"
2. **Expects the minimal answer**: Just "2" without any additional text
3. **Logs the combined event**: Using a Python function that:
   - Opens the existing monthly CSV file in logs/ directory (logs/YYYYMM-session-log.csv)
   - Appends a new row with event type "SESSION-RESET-TRIGGER"
   - Records the timestamp, token ID, and calculated reset time (UTC+8)

### Implementation Details

#### CSV Record Format

The existing CSV format is enhanced with integrated Q&A-Session-Reset events:

```csv
timestamp,event_type,token_id,reset_time_utc8
2025-08-04 05:24:27,SESSION-RESET-TRIGGER,TOKEN_1,2025-08-04 18:24:27
2025-08-07 15:00:29,SESSION-RESET-TRIGGER,TOKEN_2,2025-08-07 23:00:29
```

For SESSION-RESET-TRIGGER events:

- The `reset_time_utc8` field contains the calculated reset time (current UTC + 8 hours)
- Uses standard timestamp format: `YYYY-MM-DD HH:MM:SS`
- Combines health check verification with session reset trigger logging

#### Python Function

A Python function (`src/log_qa_check.py`) will:

1. Determine the current month's CSV filename in logs/ directory
2. Open or create the CSV file with appropriate headers
3. Calculate the expected reset time (current UTC + 8 hours)
4. Append the SESSION-RESET-TRIGGER record
5. Map OAuth token identifiers to TOKEN_1/TOKEN_2
6. Handle file operations safely with proper directory creation

#### GitHub Actions Integration

The workflow integrates Q&A with session reset:

1. Claude is asked the simple question: "1+1=? # Answer should be 2. Do not answer anything else."
2. After Claude's response, Python function logs the SESSION-RESET-TRIGGER event
3. OAuth tokens from secrets are passed to the Python script for proper token identification
4. All CSV files are stored in the logs/ directory following project structure

## Consequences

### Positive

- Provides a simple health check mechanism
- Minimal token usage (shortest possible Q&A)
- Integrates seamlessly with existing logging
- No additional infrastructure required
- Easy to verify Claude's basic functionality

### Negative

- Slightly increases workflow execution time
- Combines two concepts (health check + session reset) in a single event type
- Requires OAuth token parameter passing for proper identification

### Neutral

- The existing CSV structure is enhanced rather than duplicated
- Creates unified event logging instead of separate event types
- Files are properly organized in logs/ directory structure

## Implementation Priority

1. ✅ Create the integrated Python logging function (`src/log_qa_check.py`)
2. ✅ Update the GitHub Actions workflow with simplified prompts
3. ✅ Set up proper directory structure (logs/) and uv/pyproject.toml
4. ✅ Update documentation (README.md)
5. ✅ Test the complete integrated workflow

## References

- ADR-001: Session Reset Schedule
- ADR-002: GitHub Actions Cron Timing Optimization
- README.md: Project documentation and CSV format
