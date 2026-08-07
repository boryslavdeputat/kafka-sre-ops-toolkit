#!/usr/bin/env python3
"""Consumer group lag snapshot for Kafka / MSK.

Usage:
  python kafka_lag_snapshot.py --bootstrap HOST:9092 --group GROUP [--format table|json]
"""
from __future__ import annotations
import argparse, json, os, sys
from collections import defaultdict

def try_import_kafka():
    try:
        from kafka import KafkaAdminClient, KafkaConsumer, TopicPartition
        from kafka.structs import OffsetAndMetadata
        return KafkaAdminClient, KafkaConsumer, TopicPartition
    except ImportError:
        return None, None, None

def demo_rows():
    return [
        {"group": "demo-group", "topic": "orders", "partition": 0, "lag": 120, "committed": 1000, "end": 1120},
        {"group": "demo-group", "topic": "orders", "partition": 1, "lag": 5, "committed": 980, "end": 985},
        {"group": "demo-group", "topic": "events", "partition": 0, "lag": 0, "committed": 5000, "end": 5000},
    ]

def fetch_lag(bootstrap: str, group: str):
    KafkaAdminClient, KafkaConsumer, TopicPartition = try_import_kafka()
    if KafkaConsumer is None:
        print("kafka-python not installed - showing demo data. pip install -r requirements.txt", file=sys.stderr)
        return demo_rows()
    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap.split(","),
        group_id=group,
        enable_auto_commit=False,
        consumer_timeout_ms=5000,
    )
    # list topics then assign; production: use AdminClient list_consumer_group_offsets
    rows = []
    try:
        from kafka import KafkaAdminClient as Admin
        admin = Admin(bootstrap_servers=bootstrap.split(","))
        offsets = admin.list_consumer_group_offsets(group)
        end_consumer = KafkaConsumer(bootstrap_servers=bootstrap.split(","))
        tps = list(offsets.keys())
        end_offsets = end_consumer.end_offsets(tps) if tps else {}
        for tp, meta in offsets.items():
            end = end_offsets.get(tp, meta.offset)
            lag = max(0, end - meta.offset)
            rows.append({
                "group": group,
                "topic": tp.topic,
                "partition": tp.partition,
                "lag": lag,
                "committed": meta.offset,
                "end": end,
            })
        admin.close()
        end_consumer.close()
    except Exception as e:
        print(f"live fetch failed ({e}) - demo data", file=sys.stderr)
        rows = demo_rows()
    finally:
        consumer.close()
    return rows

def print_table(rows):
    if not rows:
        print("No data")
        return
    headers = ["group", "topic", "partition", "lag", "committed", "end"]
    widths = {h: max(len(h), max(len(str(r[h])) for r in rows)) for h in headers}
    line = "  ".join(h.ljust(widths[h]) for h in headers)
    print(line)
    print("  ".join("-" * widths[h] for h in headers))
    total_lag = 0
    for r in sorted(rows, key=lambda x: (-x["lag"], x["topic"], x["partition"])):
        print("  ".join(str(r[h]).ljust(widths[h]) for h in headers))
        total_lag += r["lag"]
    print(f"\nTOTAL_LAG={total_lag}")

def main():
    p = argparse.ArgumentParser(description="Kafka consumer lag snapshot")
    p.add_argument("--bootstrap", default=os.getenv("KAFKA_BOOTSTRAP", "localhost:9092"))
    p.add_argument("--group", required=True)
    p.add_argument("--format", choices=["table", "json"], default="table")
    p.add_argument("--fail-above", type=int, default=0, help="exit 2 if total lag exceeds N")
    args = p.parse_args()
    rows = fetch_lag(args.bootstrap, args.group)
    if args.format == "json":
        print(json.dumps(rows, indent=2))
    else:
        print_table(rows)
    total = sum(r["lag"] for r in rows)
    if args.fail_above and total > args.fail_above:
        sys.exit(2)

if __name__ == "__main__":
    main()
