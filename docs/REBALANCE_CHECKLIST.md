# Safe consumer rebalance checklist

- [ ] Freeze deploys during change window
- [ ] Confirm partition count >= desired consumer max
- [ ] Set `partition.assignment.strategy` intentionally (CooperativeSticky preferred for newer clients)
- [ ] Raise `session.timeout.ms` / tune `max.poll.interval.ms` before heavy processing changes
- [ ] Drain or dual-run consumers if protocol change
- [ ] Watch lag and rebalance rate metrics for 30m after
- [ ] Rollback plan: previous consumer image + config
