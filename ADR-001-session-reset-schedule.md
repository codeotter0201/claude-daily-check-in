# ADR-001: Claude Code Session Automated Reset Schedule Design

**Status:** Decided  
**Date:** 2024-08-04  
**Decision Makers:** Development Team  

## Context

The team intensively uses Claude Code during three fixed periods (08:00-12:00, 13:00-17:00, 20:00-00:00) and has observed that the single Session usage limit is reached after approximately 2 hours, causing workflow interruptions. To solve this problem, we need to design an automated Session reset mechanism that ensures each core working period receives a new Session quota, while maximizing the total daily available quota.

### User Requirements Analysis
- **Primary work periods:** `08:00-12:00`, `13:00-17:00`, `20:00-00:00` (UTC+8)
- **Usage pattern:** Session usage limit is reached approximately **2 hours** after each work period begins
- **Core objective:** Obtain Session reset during mid-work periods (around 10:00, 15:00, 22:00)

### Technical Constraints
- Claude Code Sessions automatically reset **5 hours after first trigger**
- Therefore, to reset at time `T`, trigger must be scheduled at `T-5` hours

## Decision

We decided to set **four** automatic trigger time points to start Claude Code's 5-hour reset countdown. This schedule aims to precisely provide new Sessions during the middle of each work period.

**Final adopted trigger time points:** 
- `05:00 (UTC+8)` / `21:00 (UTC, previous day)`
- `10:00 (UTC+8)` / `02:00 (UTC)`  
- `17:00 (UTC+8)` / `09:00 (UTC)`
- `22:00 (UTC+8)` / `14:00 (UTC)`

### Trigger and Reset Time Mapping Table

| Trigger Time (UTC+8) | Trigger Time (UTC) | Expected Reset Time (UTC+8) | Corresponding Work Period |
|:---|:---|:---|:---|
| **05:00** | **21:00 (previous day)** | **10:00** | Perfect coverage for **morning** work period (08:00-12:00) |
| **10:00** | **02:00** | **15:00** | Perfect coverage for **afternoon** work period (13:00-17:00) |
| **17:00** | **09:00** | **22:00** | Perfect coverage for **evening** work period (20:00-00:00) |
| **22:00** | **14:00** | **Next day 03:00** | Provides additional late night to early morning usage |

### GitHub Actions Cron Configuration
```yaml
schedule:
  - cron: '0 21,2,9,14 * * *'  # UTC time
```

## Consequences

### Positive Impact
- **Improved productivity:** Perfectly solves usage bottlenecks in three core work periods, users no longer need to wait manually or interrupt their thinking
- **Automation & predictability:** Schedule is fully automated with fixed reset times, allowing team to rely on and plan work
- **Maximized usage:** Through the fourth trigger point (22:00), increases total daily available Session quota, providing additional support for non-standard work hours
- **Load distribution:** Multiple OAuth tokens execute simultaneously, providing backup mechanism

### Trade-off Considerations
- The `22:00` trigger corresponds to `03:00` reset time, which is not within the defined core work periods. This decision aims to **meet four-period requirements** and provide maximum usage flexibility, rather than directly corresponding to a specific work block. This is an acceptable trade-off.
- Transformation from original "check-in system" to "Session reset system" changes the system's primary purpose

### Technical Implementation Impact
- Need to update GitHub Actions workflow cron schedule
- Need to update documentation to reflect new purpose and time points
- CSV records will change from "CHECK-IN" events to "SESSION-RESET" events
- Maintain multiple token support to ensure backup mechanism

## Alternatives Considered

1. **Maintain original 5 trigger times:** Does not meet actual work period requirements
2. **Set only 3 trigger points:** Cannot provide additional quota for fourth period
3. **Manual Session reset management:** Does not meet automation goals

## Related Documents

- [PRD.md](./PRD.md) - Product Requirements Document
- [README.md](./README.md) - Usage Documentation  
- [.github/workflows/auto-checkin.yml](./.github/workflows/auto-checkin.yml) - GitHub Actions Workflow

## Follow-up Actions

- [ ] Update GitHub Actions workflow file
- [ ] Update README.md documentation
- [ ] Update PRD.md requirements document
- [ ] Test new schedule configuration
- [ ] Monitor Session reset effects

---

**Last Updated:** 2024-08-04  
**Next Review:** 2024-09-04