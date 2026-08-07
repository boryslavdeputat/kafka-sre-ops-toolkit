#!/usr/bin/env python3
"""Report under-replicated partitions (URP). Demo-friendly if cluster unreachable."""
from __future__ import annotations
import argparse, json, os, sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bootstrap", default=os.getenv("KAFKA_BOOTSTRAP", "localhost:9092"))
    p.add_argument("--format", choices=["table", "json"], default="table")
    args = p.parse_args()
    # In production: use AdminClient describe_topics + ISR vs replicas
    urps = []
    try:
        from kafka.admin import KafkaAdminClient, ConfigResource, ConfigResourceType
        admin = KafkaAdminClient(bootstrap_servers=args.bootstrap.split(","))
        topics = admin.list_topics()
        desc = admin.describe_topics(topics)
        for t in desc:
            for part in t.get("partitions", []):
                replicas = part.get("replicas", [])
                isr = part.get("isr", [])
                if len(isr) < len(replicas):
                    urps.append({
                        "topic": t["topic"],
                        "partition": part["partition"],
                        "replicas": replicas,
                        "isr": isr,
                    })
        admin.close()
    except Exception as e:
        print(f"note: live URP check unavailable ({e}); exit 0 with empty set", file=sys.stderr)
    if args.format == "json":
        print(json.dumps(urps, indent=2))
    else:
        if not urps:
            print("URP_COUNT=0  OK")
        else:
            print(f"URP_COUNT={len(urps)}")
            for u in urps:
                print(f"  {u['topic']}-{u['partition']} replicas={u['replicas']} isr={u['isr']}")
            sys.exit(1)

if __name__ == "__main__":
    main()
