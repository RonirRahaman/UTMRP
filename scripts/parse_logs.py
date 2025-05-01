#!/usr/bin/env python3

import subprocess
import re
from datetime import datetime

def get_journal_logs():
    try:
        # Fetch logs from systemd (auth-related logs for SSH/sudo)
        result = subprocess.run(
            ['journalctl', '-p', '3..4', '-u', 'sshd', '-u', 'sudo', '--no-pager'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching journal logs: {str(e)}"]

def parse_logs(log_lines):
    events = {
        'ssh_failures': [],
        'sudo_failures': [],
        'banned_ips': []
    }

    ssh_fail_re = re.compile(r'Failed password.*from (\d{1,3}(?:\.\d{1,3}){3})')
    sudo_fail_re = re.compile(r'sudo: .*authentication failure')
    ban_re = re.compile(r'Ban\s+(\d{1,3}(?:\.\d{1,3}){3})')  # fail2ban ban logs

    for line in log_lines:
        if ssh_fail_re.search(line):
            ip = ssh_fail_re.search(line).group(1)
            events['ssh_failures'].append((line, ip))
        elif sudo_fail_re.search(line):
            events['sudo_failures'].append(line)
        elif ban_re.search(line):
            ip = ban_re.search(line).group(1)
            events['banned_ips'].append((line, ip))

    return events

def main():
    log_lines = get_journal_logs()
    events = parse_logs(log_lines)

    print(f"\n🕵️ SSH Login Failures: {len(events['ssh_failures'])}")
    for line, ip in events['ssh_failures'][:5]:
        print(f"  🔸 {ip} → {line}")

    print(f"\n⚠️ Sudo Authentication Failures: {len(events['sudo_failures'])}")
    for line in events['sudo_failures'][:5]:
        print(f"  🔸 {line}")

    print(f"\n🚫 Banned IPs (fail2ban): {len(events['banned_ips'])}")
    for line, ip in events['banned_ips'][:5]:
        print(f"  🔸 {ip} → {line}")

    print("\n✅ Log parsing completed.")

if __name__ == "__main__":
    main()
