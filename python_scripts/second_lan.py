#!/usr/bin/env python3
"""
Configure a secondary NIC (NetworkManager) on many nodes over SSH from an admin host.

Optional: patch osd_network in /etc/ustor/ustor.conf on each node (same CIDR on all nodes).

Required: SSH access; on each node, sudo for nmcli (NOPASSWD) or root SSH.
"""
from __future__ import annotations

import argparse
import ipaddress
import re
import subprocess
import sys
from pathlib import Path

# Remote bash snippet: $1=iface $2=host CIDR; $3–$6 = ustor patch (or "-" to skip).
# osd_network patch runs FIRST so a failing NM step cannot skip ustor.conf updates on peers.
REMOTE_BASH = r"""set -euo pipefail
SECOND_IFACE="$1"
IP_CIDR="$2"
CON_NAME="second-lan-static"

# Optional ustor.conf osd_network patch (args 3–6; use "-" to skip patch).
USTOR_PATH="${3:--}"
OSD_CID="${4:--}"
OSD_MODE="${5:--}"
if [[ "$USTOR_PATH" != "-" && "$OSD_CID" != "-" && "$OSD_MODE" != "-" ]]; then
  if [[ ! -f "$USTOR_PATH" ]]; then
    echo "ERROR: ustor.conf not found at $USTOR_PATH (copy it here or run etcd-start first)." >&2
    exit 3
  fi
  echo "Patching osd_network in $USTOR_PATH (mode=$OSD_MODE, cidr=$OSD_CID) ..."
  sudo python3 /dev/stdin "$USTOR_PATH" "$OSD_CID" "$OSD_MODE" <<'USTOR_PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
cidr = sys.argv[2]
mode = sys.argv[3]

data = json.loads(path.read_text(encoding="utf-8"))
old = data.get("osd_network", "")
if mode == "replace":
    data["osd_network"] = cidr
else:
    # append: comma-separated CIDR list for multi-homed clusters
    parts = [x.strip() for x in str(old).split(",") if x.strip()] if old else []
    if cidr not in parts:
        parts.append(cidr)
    data["osd_network"] = ",".join(parts) if parts else cidr

path.write_text(
    json.dumps(data, indent=2, ensure_ascii=True) + "\n",
    encoding="utf-8",
)
print("osd_network is now:", data.get("osd_network"))
USTOR_PY
  OWN="${6:--}"
  [[ "$OWN" == "-" || -z "$OWN" ]] && OWN="ustor:ustor"
  sudo chown "$OWN" "$USTOR_PATH" || true
  sudo chmod 0440 "$USTOR_PATH" || true
  echo "ustor.conf osd_network patch finished on $(hostname)."
fi

if ! ip link show "${SECOND_IFACE}" &>/dev/null; then
  echo "On $(hostname): interface ${SECOND_IFACE} not found" >&2
  ip -br link >&2
  exit 2
fi

run_nmcli() { sudo -n "$@" 2>/dev/null || sudo "$@"; }

if nmcli -t -f NAME connection show | grep -Fxq "${CON_NAME}"; then
  run_nmcli nmcli connection modify "${CON_NAME}" connection.interface-name "${SECOND_IFACE}"
  run_nmcli nmcli connection modify "${CON_NAME}" ipv4.method manual ipv4.addresses "${IP_CIDR}"
  run_nmcli nmcli connection modify "${CON_NAME}" ipv4.gateway ""
  run_nmcli nmcli connection modify "${CON_NAME}" ipv4.ignore-auto-dns yes
  run_nmcli nmcli connection modify "${CON_NAME}" connection.autoconnect yes
else
  run_nmcli nmcli connection add type ethernet con-name "${CON_NAME}" ifname "${SECOND_IFACE}" \
    ipv4.method manual ipv4.addresses "${IP_CIDR}" \
    ipv4.ignore-auto-dns yes connection.autoconnect yes
fi

run_nmcli nmcli connection up "${CON_NAME}"
echo "OK $(hostname): ${SECOND_IFACE} -> ${IP_CIDR}"
ip -4 addr show dev "${SECOND_IFACE}"
"""

IFACE_RE = re.compile(r"^[a-zA-Z0-9._-]+$")
FUTURE_RE = re.compile(
    r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})$"
)
CURRENT_USER_PREFIX_RE = re.compile(
    r"^([a-zA-Z0-9._-]+)@(\d{1,3}\.\d{1,3}\.\d{1,3})$"
)
CURRENT_PREFIX_ONLY_RE = re.compile(r"^(\d{1,3}\.\d{1,3}\.\d{1,3})$")
IPV4_FULL_RE = re.compile(
    r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
)
LAST_OCTET_ONLY_RE = re.compile(r"^(\d{1,3})$")
# Allow typical SSH target characters (hostnames, IPs, user@host).
SSH_TARGET_SAFE_RE = re.compile(r"^[a-zA-Z0-9._@:\[\]-]+$")


def _octet_ok(x: int) -> bool:
    return 0 <= x <= 255


def parse_future_spec(spec: str) -> tuple[int, int, int, int, int]:
    """Parse A.B.C.D/plen into octets and prefix length."""
    m = FUTURE_RE.match(spec.strip())
    if not m:
        raise ValueError(
            f"FUTURE address must look like A.B.C.D/plen, got: {spec!r}"
        )
    o1, o2, o3, o4, plen = (int(m.group(i)) for i in range(1, 6))
    for o in (o1, o2, o3, o4):
        if not _octet_ok(o):
            raise ValueError(f"Invalid octet in {spec!r}")
    if not (8 <= plen <= 30):
        raise ValueError(f"Invalid prefix length in {spec!r}")
    return o1, o2, o3, o4, plen


def parse_current_net(
    current_net: str, default_ssh_user: str
) -> tuple[str | None, str | None]:
    """
    Returns (ssh_user_or_empty, a_b_c_prefix_or_None).
    Use prefix None when current_net is '-' (full SSH targets only).
    """
    if current_net.strip() == "-":
        return None, None
    s = current_net.strip()
    m = CURRENT_USER_PREFIX_RE.match(s)
    if m:
        return m.group(1), m.group(2)
    m = CURRENT_PREFIX_ONLY_RE.match(s)
    if m:
        parts = m.group(1).split(".")
        if not all(_octet_ok(int(p)) for p in parts):
            raise ValueError(f"Invalid prefix in CURRENT: {current_net!r}")
        return default_ssh_user, m.group(1)
    raise ValueError(
        "CURRENT must be A.B.C, user@A.B.C, or '-' when all nodes are full SSH targets"
    )


def read_nodes_file(path: Path) -> list[str]:
    """Load non-empty, non-comment lines from a nodes file."""
    out: list[str] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            out.append(line)
    return out


def read_nodes_stdin() -> list[str]:
    """Read node lines from stdin (same comment/blank rules as file)."""
    out: list[str] = []
    for raw in sys.stdin:
        line = raw.split("#", 1)[0].strip()
        if line:
            out.append(line)
    return out


def resolve_ssh_target(
    line: str,
    current_user: str | None,
    current_prefix: str | None,
    default_ssh_user: str,
) -> str:
    """Turn one node line into an ssh(1) destination (user@host)."""
    line = line.strip()
    m = IPV4_FULL_RE.match(line)
    if m:
        octets = tuple(int(m.group(i)) for i in range(1, 5))
        if not all(_octet_ok(o) for o in octets):
            raise ValueError(f"Invalid IPv4: {line!r}")
        return f"{default_ssh_user}@{line}"

    m = LAST_OCTET_ONLY_RE.match(line)
    if m:
        last = int(m.group(1))
        if not _octet_ok(last):
            raise ValueError(f"Invalid host octet: {line!r}")
        if not current_prefix or not current_user:
            raise ValueError(
                f"Short node form {line!r} requires CURRENT (A.B.C or user@A.B.C), not '-'"
            )
        return f"{current_user}@{current_prefix}.{last}"

    if "@" in line:
        return line
    return f"{default_ssh_user}@{line}"


def validate_ssh_target(target: str) -> None:
    if not SSH_TARGET_SAFE_RE.match(target):
        raise ValueError(f"Refusing suspicious SSH target: {target!r}")


OWNER_RE = re.compile(r"^[^:]+:[^:]+$")


def build_ssh_command(
    target: str,
    iface: str,
    ip_cidr: str,
    ssh_extra: list[str],
    batch_mode: bool,
    use_tty: bool,
    ustor_path: str,
    osd_cidr: str,
    osd_mode: str,
    ustor_owner: str,
) -> list[str]:
    """Assemble ssh argv; remote script is sent on stdin."""
    cmd: list[str] = ["ssh"]
    if use_tty:
        cmd.append("-t")
    cmd.extend(ssh_extra)
    cmd.extend(["-o", "StrictHostKeyChecking=accept-new"])
    if batch_mode:
        cmd.extend(["-o", "BatchMode=yes"])
    cmd.extend(
        [
            target,
            "bash",
            "-s",
            "--",
            iface,
            ip_cidr,
            ustor_path,
            osd_cidr,
            osd_mode,
            ustor_owner,
        ]
    )
    return cmd


def run_remote(
    target: str,
    iface: str,
    ip_cidr: str,
    args: argparse.Namespace,
    *,
    ustor_path: str,
    osd_cidr: str,
    osd_mode: str,
    ustor_owner: str,
) -> None:
    """Run REMOTE_BASH on target via ssh."""
    cmd = build_ssh_command(
        target,
        iface,
        ip_cidr,
        args.ssh_opt,
        batch_mode=not args.no_batch,
        use_tty=args.tty,
        ustor_path=ustor_path,
        osd_cidr=osd_cidr,
        osd_mode=osd_mode,
        ustor_owner=ustor_owner,
    )
    print(f"=== {target} -> {ip_cidr} ===", flush=True)
    subprocess.run(
        cmd,
        input=REMOTE_BASH,
        text=True,
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Set secondary NIC addresses (NM profile second-lan-static) on many nodes over SSH."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 192.168.98 10.0.0.11/24 enp2s0 211 212 213
  %(prog)s - 10.0.0.11/24 enp2s0 root@192.168.98.211 --patch-ustor-conf --osd-network-cidr 10.0.0.0/24
  %(prog)s root@192.168.98 10.0.0.11/24 enp2s0 -f nodes.txt --patch-ustor-conf --osd-supernet-plen 22

Node list: -f/--nodes-file, trailing arguments after INTERFACE, or stdin if not a TTY.
Addresses: first host gets FUTURE as given; each next host gets previous last octet + 1 (same prefix length).
With --patch-ustor-conf, the same osd_network CIDR is applied on every node (default: replace).
""",
    )
    parser.add_argument(
        "-f",
        "--nodes-file",
        type=Path,
        metavar="FILE",
        help="Read node lines from FILE (after stripping comments and blanks)",
    )
    parser.add_argument(
        "--ssh-user",
        default="root",
        help="Default SSH user for bare IPv4 and short last-octet nodes (default: root)",
    )
    parser.add_argument(
        "--ssh-opt",
        action="append",
        default=[],
        metavar="OPT",
        help="Extra ssh option token (repeatable), e.g. --ssh-opt -i --ssh-opt /path/to/key",
    )
    parser.add_argument(
        "--no-batch",
        action="store_true",
        help="Do not pass ssh -o BatchMode=yes (e.g. password auth)",
    )
    parser.add_argument(
        "--tty",
        action="store_true",
        help="Allocate a TTY (ssh -t), e.g. for sudo password prompts",
    )
    parser.add_argument(
        "--patch-ustor-conf",
        action="store_true",
        help=(
            "After NM setup, update osd_network in ustor.conf on each node "
            "(requires sudo + python3 on the node; ustor user for chown)"
        ),
    )
    parser.add_argument(
        "--osd-network-cidr",
        default=None,
        metavar="CIDR",
        help=(
            "Supernet written to osd_network (e.g. 10.0.0.0/24 or 10.0.0.0/22); "
            "If --patch-ustor-conf and this is omitted, uses A.B.C.0/plen from the first "
            "future address; plen from --osd-supernet-plen or the same as the host /prefix."
        ),
    )
    parser.add_argument(
        "--osd-supernet-plen",
        type=int,
        default=None,
        metavar="N",
        help=(
            "When auto-computing osd supernet (no --osd-network-cidr), use this prefix "
            "length instead of the host interface prefix (e.g. 22 to match ustor-init infer)."
        ),
    )
    parser.add_argument(
        "--osd-network-mode",
        choices=("append", "replace"),
        default="replace",
        help=(
            "replace: set osd_network to the new CIDR only (default); "
            "append: comma-merge new CIDR with existing osd_network"
        ),
    )
    parser.add_argument(
        "--ustor-conf",
        default="/etc/ustor/ustor.conf",
        metavar="PATH",
        help="Path to ustor.conf on nodes (default: /etc/ustor/ustor.conf)",
    )
    parser.add_argument(
        "--ustor-conf-owner",
        default="ustor:ustor",
        metavar="USER:GROUP",
        help="chown after JSON write (default: ustor:ustor)",
    )
    parser.add_argument(
        "current_net",
        help="A.B.C or user@A.B.C for short nodes; '-' if all nodes are full user@host or IPv4",
    )
    parser.add_argument(
        "future_spec",
        help="First static address, e.g. 10.0.0.11/24; following nodes get +1 last octet",
    )
    parser.add_argument(
        "interface",
        help="Secondary interface name on every node (e.g. enp2s0)",
    )
    parser.add_argument(
        "nodes",
        nargs="*",
        help="Additional node lines after the three required arguments",
    )
    args = parser.parse_args()

    iface = args.interface
    if not IFACE_RE.match(iface):
        print(f"Invalid interface name: {iface!r}", file=sys.stderr)
        return 2

    try:
        o1, o2, o3, start_last, plen = parse_future_spec(args.future_spec)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2

    try:
        current_user, current_prefix = parse_current_net(
            args.current_net, args.ssh_user
        )
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2

    if not OWNER_RE.match(args.ustor_conf_owner):
        print(
            f"Invalid --ustor-conf-owner (expected user:group): {args.ustor_conf_owner!r}",
            file=sys.stderr,
        )
        return 2

    if args.patch_ustor_conf:
        if args.osd_network_cidr:
            try:
                net = ipaddress.ip_network(args.osd_network_cidr.strip(), strict=False)
            except ValueError as e:
                print(f"Invalid --osd-network-cidr: {e}", file=sys.stderr)
                return 2
            if not isinstance(net, ipaddress.IPv4Network):
                print("--osd-network-cidr must be an IPv4 network", file=sys.stderr)
                return 2
            osd_network_cidr = str(net)
        else:
            pl_auto = (
                args.osd_supernet_plen if args.osd_supernet_plen is not None else plen
            )
            if not (8 <= pl_auto <= 30):
                print("--osd-supernet-plen must be between 8 and 30", file=sys.stderr)
                return 2
            osd_network_cidr = f"{o1}.{o2}.{o3}.0/{pl_auto}"
        ustor_path = str(Path(args.ustor_conf))
        osd_cidr_arg = osd_network_cidr
        osd_mode_arg = args.osd_network_mode
        ustor_owner_arg = args.ustor_conf_owner
    else:
        ustor_path = "-"
        osd_cidr_arg = "-"
        osd_mode_arg = "-"
        ustor_owner_arg = "-"

    raw_nodes: list[str] = []
    if args.nodes_file is not None:
        if not args.nodes_file.is_file():
            print(f"Nodes file not found: {args.nodes_file}", file=sys.stderr)
            return 2
        raw_nodes.extend(read_nodes_file(args.nodes_file))
    raw_nodes.extend(args.nodes)

    if not raw_nodes:
        if sys.stdin.isatty():
            print(
                "No nodes: pass them after INTERFACE, use -f, or pipe lines on stdin.",
                file=sys.stderr,
            )
            return 2
        raw_nodes.extend(read_nodes_stdin())

    if not raw_nodes:
        print("No nodes after parsing.", file=sys.stderr)
        return 2

    ssh_targets: list[str] = []
    for line in raw_nodes:
        try:
            t = resolve_ssh_target(
                line, current_user, current_prefix, args.ssh_user
            )
            validate_ssh_target(t)
        except ValueError as e:
            print(e, file=sys.stderr)
            return 2
        ssh_targets.append(t)

    n = len(ssh_targets)
    if start_last + n - 1 > 255:
        print(
            f"Last octet would exceed 255 (start={start_last}, nodes={n}).",
            file=sys.stderr,
        )
        return 2

    for i, target in enumerate(ssh_targets):
        last = start_last + i
        ip_cidr = f"{o1}.{o2}.{o3}.{last}/{plen}"
        try:
            run_remote(
                target,
                iface,
                ip_cidr,
                args,
                ustor_path=ustor_path,
                osd_cidr=osd_cidr_arg,
                osd_mode=osd_mode_arg,
                ustor_owner=ustor_owner_arg,
            )
        except subprocess.CalledProcessError as e:
            print(f"ssh failed for {target} (exit {e.returncode})", file=sys.stderr)
            return e.returncode or 1

    print(f"Done. Nodes processed: {n}.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
