# Kafka SRE Ops Toolkit

**Languages:** [English](README.md) · [Українська](README.uk.md)

> Practical reference by [Boryslav Deputat](https://github.com/boryslavdeputat) - Cloud / SRE / Platform.
> Sites: [Portfolio](https://boryslavdeputat.com/) · [ClawDBot / KLAV (UA AI)](https://clawdbot.llc/) · [Walk ATX Pet](https://walkatxpet.com/) · [DepuTater](https://deputater.com/)

Python toolkit for **Apache Kafka / Amazon MSK**: consumer lag, under-replicated partitions, rebalance helpers, topic capacity, and incident runbooks.

## Features

| Tool | What it does |
|------|----------------|
| `kafka_lag_snapshot.py` | Consumer group lag snapshot (JSON / table) |
| `under_replicated.py` | Detect under-replicated partitions |
| `topic_capacity.py` | Estimate partition / retention capacity |
| `rebalance_checklist.md` | Safe rebalance steps |
| `incident_lag.md` | High lag incident runbook |

## Quick start

```bash
git clone https://github.com/boryslavdeputat/kafka-sre-ops-toolkit.git
cd kafka-sre-ops-toolkit
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Lag snapshot (uses kafka-python or MSK IAM via bootstrap)
python scripts/kafka_lag_snapshot.py \
  --bootstrap $BOOTSTRAP \
  --group my-consumer-group \
  --format table

# Under-replicated check
python scripts/under_replicated.py --bootstrap $BOOTSTRAP

# Capacity estimate
python scripts/topic_capacity.py --rate-mbs 12 --retention-days 7 --replication 3
```

## Environment

| Variable | Description |
|----------|-------------|
| `KAFKA_BOOTSTRAP` | `b-1.xxx.kafka.us-east-1.amazonaws.com:9092` |
| `KAFKA_SECURITY` | `PLAINTEXT` / `SSL` / `SASL_SSL` |
| `KAFKA_SASL_MECHANISM` | e.g. `AWS_MSK_IAM` or `SCRAM-SHA-512` |

## Architecture

```
Producers --> MSK / Kafka cluster --> Consumers
                    |
         lag monitor / URP check / capacity model
                    |
              Alertmanager / Pager / Grafana
```

## Production checklist

- [ ] Multi-AZ brokers, rack awareness
- [ ] Replication factor >= 3 for critical topics
- [ ] Min ISR and unclean leader election policy set deliberately
- [ ] Consumer lag SLO + alerts
- [ ] Disk / retention alarms
- [ ] Runbook for partition reassignment and rolling bounce
- [ ] Backup of configs (topic ACLs, quotas)

## Repository layout

```
kafka-sre-ops-toolkit/
├── scripts/           # CLI tools
├── docs/              # runbooks
├── examples/          # sample configs / dashboards notes
├── requirements.txt
├── README.md
└── README.uk.md
```

## Disclaimer

Educational and practical reference. Validate against your compliance, cost, and SLO requirements before production use.

## Contact

- Portfolio: https://boryslavdeputat.com/
- ClawDBot / KLAV (UA AI): https://clawdbot.llc/
- Email: info@boryslavdeputat.com

## License

MIT - see [LICENSE](LICENSE).

---

## Discoverability

- Author: [Boryslav Deputat](https://github.com/boryslavdeputat) · [https://boryslavdeputat.com/](https://boryslavdeputat.com/)
- AI context: [https://boryslavdeputat.github.io/llms.txt](https://boryslavdeputat.github.io/llms.txt)
- This repo: [llms.txt](llms.txt)

