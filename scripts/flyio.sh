#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: scripts/flyio.sh <py|python|rs|rust> <workload> [maelstrom args...]" >&2
  exit 1
fi

lang="$1"
workload="$2"
shift 2

case "$workload" in
  generate|unique-id|unique-ids)
    maelstrom_workload="unique-ids"
    ;;
  echo)
    maelstrom_workload="echo"
    ;;
  *)
    maelstrom_workload="$workload"
    ;;
esac

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd -- "$script_dir/.." && pwd)"

node_count_set=false
time_limit_set=false
for arg in "$@"; do
  case "$arg" in
    --node-count|--node-count=*) node_count_set=true ;;
    --time-limit|--time-limit=*) time_limit_set=true ;;
  esac
done

default_args=()
if [[ "$node_count_set" == false ]]; then
  default_args+=(--node-count 1)
fi
if [[ "$time_limit_set" == false ]]; then
  default_args+=(--time-limit 10)
fi

case "$lang" in
  py|python)
    main_py="$repo_root/dist-sys/python/flyio/main.py"
    if [[ ! -f "$main_py" ]]; then
      echo "Python entrypoint not found: $main_py" >&2
      exit 1
    fi
    tmpdir="$(mktemp -d)"
    trap 'rm -rf "$tmpdir"' EXIT
    bin="$tmpdir/run-python-flyio.sh"
    cat > "$bin" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cd "$repo_root/dist-sys/python"
uv run python flyio/main.py
EOF
    chmod +x "$bin"
    ;;
  rs|rust)
    manifest="$repo_root/dist-sys/rust/flyio/$workload/Cargo.toml"
    if [[ ! -f "$manifest" ]]; then
      echo "Rust manifest not found: $manifest" >&2
      exit 1
    fi
    tmpdir="$(mktemp -d)"
    trap 'rm -rf "$tmpdir"' EXIT
    bin="$tmpdir/run-rust-$workload.sh"
    cat > "$bin" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cd "$repo_root/dist-sys/rust"
cargo run --quiet --manifest-path "flyio/$workload/Cargo.toml"
EOF
    chmod +x "$bin"
    ;;
  *)
    echo "Unknown language: $lang. Use py|python|rs|rust" >&2
    exit 1
    ;;
esac

exec "$HOME/.local/bin/maelstrom" test -w "$maelstrom_workload" --bin "$bin" "${default_args[@]}" "$@"
