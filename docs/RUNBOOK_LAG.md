# Runbook: Consumer lag high

## Severity

| Lag vs SLO | Severity |
|------------|----------|
| > SLO for 5m | SEV-3 |
| > 5x SLO or business impact | SEV-2 |
| data loss risk / stuck critical path | SEV-1 |

## Diagnose

1. Identify group and topics: `python scripts/kafka_lag_snapshot.py --bootstrap $B --group $G`
2. Check consumer pods / instances healthy (restarts, OOM, deploy in progress)
3. Check broker health: URP, disk, CPU (`under_replicated.py`)
4. Check producer spike vs consumer throughput
5. Check max.poll.interval / session.timeout misconfig

## Mitigate

- Scale consumers (if partitions allow)
- Pause non-critical producers
- Temporary retention increase if risk of retention loss
- Fix poison pill messages if stuck on one partition

## Verify

- Lag trend down for 15m
- No URP growth
- Downstream SLOs recovering

## Escalate

Platform on-call if broker-side; app on-call if consumer code.
