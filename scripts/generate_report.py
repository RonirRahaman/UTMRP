#!/usr/bin/env python3

import os
import datetime
from parse_logs import get_journal_logs, parse_logs

def generate_report():
    logs = get_journal_logs()
    events = parse_logs(logs)
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    report_path = f"logs/report_{now}.txt"

    os.makedirs("logs", exist_ok=True)

    with open(report_path, "w") as f:
        f.write(f"Advanced Linux Threat Monitoring Report - {now}\n")
        f.write("="*60 + "\n\n")

        f.write(f"🕵️ SSH Login Failures: {len(events['ssh_failures'])}\n")
        for line, ip in events['ssh_failures']:
            f.write(f"  🔸 {ip} → {line}\n")

        f.write(f"\n⚠️ Sudo Authentication Failures: {len(events['sudo_failures'])}\n")
        for line in events['sudo_failures']:
            f.write(f"  🔸 {line}\n")

        f.write(f"\n🚫 Banned IPs (fail2ban): {len(events['banned_ips'])}\n")
        for line, ip in events['banned_ips']:
            f.write(f"  🔸 {ip} → {line}\n")

        f.write("\n✅ Log parsing completed.\n")

    print(f"✅ Report saved to: {report_path}")

if __name__ == "__main__":
    generate_report()
