#!/usr/bin/env python3
"""Rough topic capacity estimator (disk / partitions)."""
from __future__ import annotations
import argparse, math

def main():
    p = argparse.ArgumentParser(description="Kafka topic capacity estimate")
    p.add_argument("--rate-mbs", type=float, required=True, help="average ingest MB/s")
    p.add_argument("--retention-days", type=float, required=True)
    p.add_argument("--replication", type=int, default=3)
    p.add_argument("--partition-target-mbs", type=float, default=10.0, help="target MB/s per partition")
    p.add_argument("--overhead", type=float, default=1.25, help="index/compaction overhead factor")
    args = p.parse_args()

    seconds = args.retention_days * 86400
    raw_gb = (args.rate_mbs * seconds) / 1024.0
    with_rep_gb = raw_gb * args.replication * args.overhead
    partitions = max(1, math.ceil(args.rate_mbs / args.partition_target_mbs))

    print("=== Topic capacity estimate ===")
    print(f"ingest_MBps          = {args.rate_mbs}")
    print(f"retention_days       = {args.retention_days}")
    print(f"replication          = {args.replication}")
    print(f"raw_single_replica_GB= {raw_gb:.2f}")
    print(f"cluster_disk_GB      = {with_rep_gb:.2f}  (with RF * overhead)")
    print(f"suggested_partitions = {partitions}")
    print(f"per_partition_MBps   = {args.rate_mbs / partitions:.2f}")
    print("\nNotes: validate against broker disk, network, and consumer parallelism.")

if __name__ == "__main__":
    main()
