# ADR-004: Workflow Timeout Configuration

## Status

Accepted

## Context

The GitHub Actions workflow experienced execution timeout issues:

- **Symptom**: Workflow ran for 6 hours before being cancelled
- **Root Causes**:
  1. Missing timeout configuration, defaulting to GitHub Actions' 6-hour maximum
  2. Claude Code OAuth token authentication failure (401 Bad credentials)
  3. Action hung instead of failing fast, waiting until default timeout limit
- **Expected Duration**: The entire workflow should complete within 1-3 minutes

## Decision

Implement multi-level timeout protection:

### 1. Job-Level Timeout
```yaml
timeout-minutes: 5
```
- Entire job terminates after 5 minutes maximum
- Prevents runaway executions at job level

### 2. Step-Level Timeout
```yaml
timeout_minutes: 2
```
- Each Claude Code action step terminates after 2 minutes maximum
- Ensures individual steps fail fast instead of waiting indefinitely

### Implementation

Modified `.github/workflows/auto-checkin.yml`:

```yaml
jobs:
  session-reset:
    runs-on: ubuntu-latest
    timeout-minutes: 5  # Job-level timeout
    permissions:
      id-token: write
      contents: write
      pull-requests: write

    steps:
      - name: Execute Session Reset Logic (Token 1)
        uses: anthropics/claude-code-action@beta
        continue-on-error: true
        with:
          mode: agent
          timeout_minutes: 2  # Step-level timeout
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN_1 }}
          direct_prompt: |
            1+1=? # Answer should be 2. Do not answer anything else.

      - name: Execute Session Reset Logic (Token 2)
        uses: anthropics/claude-code-action@beta
        continue-on-error: true
        with:
          mode: agent
          timeout_minutes: 2  # Step-level timeout
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN_2 }}
          direct_prompt: |
            1+1=? # Answer should be 2. Do not answer anything else.
```

## Consequences

### Positive

- **Resource savings**: Reduced from 6 hours to maximum 5 minutes (99.86% reduction)
- **Fail fast**: Issues detected immediately instead of waiting hours
- **Cost optimization**: Significantly reduced GitHub Actions execution time and costs
- **Multi-layer protection**: Job and step-level timeouts ensure safety

### Negative

- Timeout values may need adjustment based on actual execution patterns
- Does not address the root cause of authentication failures

### Neutral

- Normal execution time unaffected (still 1-3 minutes)
- Timeout mechanism only triggers in abnormal situations

## Recommendations

If authentication errors (401) persist, consider regenerating OAuth tokens:

```bash
# Run locally
claude setup-token
```

Then update GitHub Secrets:
- `CLAUDE_CODE_OAUTH_TOKEN_1`
- `CLAUDE_CODE_OAUTH_TOKEN_2`

Note: Token regeneration is optional and only needed if authentication failures occur.

## References

- ADR-003: Simple Q&A Logging Feature
- GitHub Actions Documentation: [Workflow syntax - timeout-minutes](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idtimeout-minutes)
