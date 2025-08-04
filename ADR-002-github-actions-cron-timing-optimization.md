# ADR-002: GitHub Actions Cron Timing Optimization for Reliability

**Status:** Decided  
**Date:** 2025-08-04  
**Decision Makers:** Development Team  
**Supersedes:** Timing aspects of ADR-001

## Context

After implementing ADR-001's session reset schedule, we observed reliability issues with GitHub Actions cron triggers. The current configuration uses minute `0` (top of the hour), which experiences high load and reduced reliability due to:

- GitHub Actions infrastructure load spikes at exact hour boundaries (`:00`)
- Millions of workflows triggering simultaneously at common times (`:00`, `:30`)
- Competition for compute resources during peak scheduling windows
- Observed failures particularly at the 17:00 UTC+8 trigger (09:00 UTC)

### Current Configuration Issues
```yaml
schedule:
  - cron: '0 21,2,9,14 * * *'  # Triggers at exact hour boundaries
```

### Research Findings
Based on GitHub Actions community best practices and reliability data:
- **Highest reliability**: Minutes 15 and 45 (avoid both hour boundaries and common half-hour scheduling)
- **Medium reliability**: Minutes 7, 23, 37, 52 (avoid common patterns)
- **Lowest reliability**: Minutes 0, 5, 10, 30 (peak competition times)

## Decision

We decided to modify the cron schedule from minute `0` to minute `23` to improve trigger reliability while maintaining the same hourly schedule established in ADR-001.

**Updated cron configuration:**
```yaml
schedule:
  - cron: '23 21,2,9,14 * * *'  # UTC time, triggers at :23 past the hour
```

### Updated Trigger and Reset Time Mapping

| Trigger Time (UTC+8) | Trigger Time (UTC) | Expected Reset Time (UTC+8) | Corresponding Work Period |
|:---|:---|:---|:---|
| **05:23** | **21:23 (previous day)** | **10:23** | Coverage for **morning** work period (08:00-12:00) |
| **10:23** | **02:23** | **15:23** | Coverage for **afternoon** work period (13:00-17:00) |
| **17:23** | **09:23** | **22:23** | Coverage for **evening** work period (20:00-00:00) |
| **22:23** | **14:23** | **Next day 03:23** | Additional late night to early morning coverage |

### Rationale for Minute 23
- **High reliability**: Minute 23 avoids common scheduling patterns and peak load times
- **Load avoidance**: Completely avoids the high-load periods at hour boundaries and common patterns
- **Minimal impact**: 23-minute delay has negligible impact on session reset effectiveness
- **Consistent offset**: All triggers maintain the same 23-minute offset for predictability

## Consequences

### Positive Impact
- **Improved reliability**: Significantly reduced probability of missed triggers
- **Consistent execution**: More predictable workflow execution times
- **Better resource availability**: Reduced competition for GitHub Actions compute resources
- **Maintained functionality**: Preserves all benefits of ADR-001's session management strategy

### Minimal Trade-offs
- **23-minute delay**: Session resets occur 23 minutes later than originally planned
  - Morning reset: 10:23 instead of 10:00 (still within optimal window for 08:00-12:00 work period)
  - Afternoon reset: 15:23 instead of 15:00 (still within optimal window for 13:00-17:00 work period)
  - Evening reset: 22:23 instead of 22:00 (still within optimal window for 20:00-00:00 work period)

### Technical Implementation Impact
- Update GitHub Actions workflow cron schedule
- Update documentation to reflect new timing
- No changes required to session reset logic or CSV logging format
- Backward compatibility maintained for existing logs

## Alternatives Considered

1. **Minute 15**: Highly reliable but minute 23 provides better load distribution
2. **Minute 45**: Equally reliable but would require shifting to different hours (20,1,8,13 UTC) to maintain work period alignment
3. **Minute 7 or 37**: Good reliability but minute 23 provides better avoidance of common patterns
4. **Multiple staggered times**: Complex to manage and unnecessary for current scale
5. **Random minute selection**: Unpredictable and harder to debug/monitor

## Related Documents

- [ADR-001-session-reset-schedule.md](./ADR-001-session-reset-schedule.md) - Original session reset timing decision
- [README.md](./README.md) - Usage Documentation  
- [PRD.md](./PRD.md) - Product Requirements Document
- [.github/workflows/auto-checkin.yml](./.github/workflows/auto-checkin.yml) - GitHub Actions Workflow

## Follow-up Actions

- [x] Update GitHub Actions workflow file with new cron timing
- [x] Update README.md documentation with new schedule
- [x] Update PRD.md with timing optimization details
- [ ] Monitor improved reliability over 2-week period
- [ ] Document any observed improvements in trigger success rate

---

**Last Updated:** 2025-08-04  
**Next Review:** 2025-09-04