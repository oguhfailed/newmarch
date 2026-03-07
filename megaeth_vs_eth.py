#!/usr/bin/env python3
"""
Comparison between Ethereum (L1) and MegaETH (L2) metrics.
"""


# --- Ethereum L1 benchmark data ---
# These are approximate real-world figures for Ethereum mainnet.
ETH = {
    "name": "Ethereum (L1)",
    "tps": 15,                 # ~15 transactions per second on mainnet
    "block_time_ms": 12000,    # 12 second block time post-Merge
    "avg_gas_fee_usd": 5.00,   # average gas fee in USD (varies widely)
    "finality_sec": 900,       # ~15 minutes for probabilistic finality
    "evm_compatible": True,    # Ethereum IS the EVM standard
    "layer": "L1",
    "status": "Mainnet",
}

# --- MegaETH L2 benchmark data ---
# Figures based on MegaETH published benchmarks (testnet, 2025).
MEGAETH = {
    "name": "MegaETH (L2)",
    "tps": 100_000,            # target 100k TPS via high-performance sequencer
    "block_time_ms": 1,        # 1ms "micro-block" intervals
    "avg_gas_fee_usd": 0.001,  # near-zero fees due to L2 efficiency
    "finality_sec": 1,         # near real-time soft finality on L2
    "evm_compatible": True,    # fully EVM-compatible, deploy existing contracts as-is
    "layer": "L2 (settles on Ethereum)",
    "status": "Testnet (2025)",
}


def format_tps_bar(tps, max_tps=100_000, bar_width=40):
    """Build an ASCII progress bar scaled relative to max_tps."""
    filled = int((tps / max_tps) * bar_width)   # how many '#' chars to fill
    bar = "#" * filled + "-" * (bar_width - filled)
    return f"[{bar}] {tps:,} TPS"


def format_block_time(ms):
    """Convert milliseconds to a readable string (seconds if >= 1000ms)."""
    if ms >= 1000:
        return f"{ms / 1000:.1f}s"   # e.g. 12000ms -> "12.0s"
    return f"{ms}ms"                  # e.g. 1ms -> "1ms"


def compare(eth, mega):
    """Print a full side-by-side comparison of two chain dicts."""

    # --- Section 1: Header ---
    print("=" * 62)
    print("       ETHEREUM vs MegaETH — Side-by-Side Comparison")
    print("=" * 62)

    # Build a list of (label, eth_value, mega_value) rows for the table
    metrics = [
        ("Layer",           eth["layer"],                           mega["layer"]),
        ("Status",          eth["status"],                          mega["status"]),
        ("Throughput",      f"{eth['tps']:,} TPS",                  f"{mega['tps']:,} TPS"),
        ("Block Time",      format_block_time(eth["block_time_ms"]),format_block_time(mega["block_time_ms"])),
        ("Avg Gas Fee",     f"${eth['avg_gas_fee_usd']:.2f}",       f"${mega['avg_gas_fee_usd']:.4f}"),
        ("Finality",        f"{eth['finality_sec']}s (~15 min)",    f"{mega['finality_sec']}s (real-time)"),
        ("EVM Compatible",  str(eth["evm_compatible"]),             str(mega["evm_compatible"])),
    ]

    # --- Section 2: Metrics table ---
    label_w = 16   # width of the left "Metric" column
    col_w = 28     # width of each chain value column
    header = f"{'Metric':<{label_w}}{'Ethereum (L1)':<{col_w}}{'MegaETH (L2)':<{col_w}}"
    print(f"\n{header}")
    print("-" * 62)
    for label, eth_val, mega_val in metrics:
        print(f"{label:<{label_w}}{eth_val:<{col_w}}{mega_val:<{col_w}}")

    # --- Section 3: Visual throughput bars ---
    print("\n" + "=" * 62)
    print("  THROUGHPUT VISUALIZED")
    print("=" * 62)
    print(f"\nEthereum : {format_tps_bar(eth['tps'])}")
    print(f"MegaETH  : {format_tps_bar(mega['tps'])}")

    # --- Section 4: Speed multipliers ---
    # Show how many times faster/cheaper MegaETH is vs Ethereum
    print("\n" + "=" * 62)
    print("  SPEED IMPROVEMENTS (MegaETH over Ethereum)")
    print("=" * 62)
    tps_x   = mega["tps"] / eth["tps"]                        # throughput ratio
    block_x = eth["block_time_ms"] / mega["block_time_ms"]    # block time ratio
    fee_x   = eth["avg_gas_fee_usd"] / mega["avg_gas_fee_usd"] # fee ratio

    print(f"\n  Throughput : {tps_x:,.0f}x faster")
    print(f"  Block Time : {block_x:,.0f}x faster")
    print(f"  Gas Fees   : {fee_x:,.0f}x cheaper")

    # --- Section 5: Important context notes ---
    print("\n" + "=" * 62)
    print("  NOTES")
    print("=" * 62)
    print("""
  - MegaETH is an Ethereum L2, NOT a replacement for Ethereum.
  - It settles transactions back to Ethereum mainnet for security.
  - MegaETH uses a single high-performance sequencer node.
  - All MegaETH contracts are EVM-compatible (deploy as-is).
  - Figures are approximate / based on published benchmarks.
    """)


# Entry point — run the comparison when the script is executed directly
if __name__ == "__main__":
    compare(ETH, MEGAETH)
