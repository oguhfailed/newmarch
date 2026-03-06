#!/usr/bin/env python3
"""
Comparison between Ethereum (L1) and MegaETH (L2) metrics.
"""


ETH = {
    "name": "Ethereum (L1)",
    "tps": 15,
    "block_time_ms": 12000,
    "avg_gas_fee_usd": 5.00,
    "finality_sec": 900,       # ~15 minutes (probabilistic finality)
    "evm_compatible": True,
    "layer": "L1",
    "status": "Mainnet",
}

MEGAETH = {
    "name": "MegaETH (L2)",
    "tps": 100_000,
    "block_time_ms": 1,
    "avg_gas_fee_usd": 0.001,
    "finality_sec": 1,         # near real-time
    "evm_compatible": True,
    "layer": "L2 (settles on Ethereum)",
    "status": "Testnet (2025)",
}


def format_tps_bar(tps, max_tps=100_000, bar_width=40):
    filled = int((tps / max_tps) * bar_width)
    return "[" + "#" * filled + "-" * (bar_width - filled) + f"] {tps:,} TPS"


def format_block_time(ms):
    if ms >= 1000:
        return f"{ms / 1000:.1f}s"
    return f"{ms}ms"


def compare(eth, mega):
    print("=" * 62)
    print("       ETHEREUM vs MegaETH — Side-by-Side Comparison")
    print("=" * 62)

    metrics = [
        ("Layer",           eth["layer"],                          mega["layer"]),
        ("Status",          eth["status"],                         mega["status"]),
        ("Throughput",      f"{eth['tps']:,} TPS",                 f"{mega['tps']:,} TPS"),
        ("Block Time",      format_block_time(eth["block_time_ms"]),format_block_time(mega["block_time_ms"])),
        ("Avg Gas Fee",     f"${eth['avg_gas_fee_usd']:.2f}",      f"${mega['avg_gas_fee_usd']:.4f}"),
        ("Finality",        f"{eth['finality_sec']}s (~15 min)",   f"{mega['finality_sec']}s (real-time)"),
        ("EVM Compatible",  str(eth["evm_compatible"]),            str(mega["evm_compatible"])),
    ]

    label_w = 16
    col_w = 28
    header = f"{'Metric':<{label_w}}{'Ethereum (L1)':<{col_w}}{'MegaETH (L2)':<{col_w}}"
    print(f"\n{header}")
    print("-" * 62)
    for label, eth_val, mega_val in metrics:
        print(f"{label:<{label_w}}{eth_val:<{col_w}}{mega_val:<{col_w}}")

    print("\n" + "=" * 62)
    print("  THROUGHPUT VISUALIZED")
    print("=" * 62)
    print(f"\nEthereum : {format_tps_bar(eth['tps'])}")
    print(f"MegaETH  : {format_tps_bar(mega['tps'])}")

    print("\n" + "=" * 62)
    print("  SPEED IMPROVEMENTS (MegaETH over Ethereum)")
    print("=" * 62)
    tps_x = mega["tps"] / eth["tps"]
    block_x = eth["block_time_ms"] / mega["block_time_ms"]
    fee_x = eth["avg_gas_fee_usd"] / mega["avg_gas_fee_usd"]

    print(f"\n  Throughput : {tps_x:,.0f}x faster")
    print(f"  Block Time : {block_x:,.0f}x faster")
    print(f"  Gas Fees   : {fee_x:,.0f}x cheaper")

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


if __name__ == "__main__":
    compare(ETH, MEGAETH)
