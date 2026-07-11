"""
main.py

Resource Allocation Simulator
------------------------------
Simulates distributing a fixed pool of additional education funding
across five regions under four different allocation rules, then
projects the effect on exam pass rates using a diminishing-returns
model that accounts for teacher retention.

Run:
    python3 main.py
"""

import statistics
import matplotlib.pyplot as plt

from region import DEFAULT_REGIONS
from allocator import BudgetAllocator
from impact_model import ImpactModel

TOTAL_BUDGET = 500_000_000  # TZS: additional annual budget to allocate


def run_simulation():
    regions = DEFAULT_REGIONS
    allocator = BudgetAllocator(regions, TOTAL_BUDGET)
    model = ImpactModel()

    strategies = allocator.strategies()
    projections = {
        strategy_name: model.project_all(regions, allocation)
        for strategy_name, allocation in strategies.items()
    }
    return regions, strategies, projections


# ----------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------
def print_report(regions, strategies, projections):
    print("RESOURCE ALLOCATION SIMULATOR")
    print("=" * 60)
    print(f"Total additional budget: {TOTAL_BUDGET:,} TZS\n")

    for strategy_name in strategies:
        print(f"--- {strategy_name} ---")
        allocation = strategies[strategy_name]
        result = projections[strategy_name]

        for region in regions:
            extra = allocation[region.name]
            r = result[region.name]
            print(f"  {region.name:15} +{extra:9,.0f} TZS/pupil  "
                  f"pass rate: {r['old']:>5}% -> {r['new']:>5}%  (+{r['gain']}pp)")

        gains = [result[r.name]["gain"] for r in regions]
        new_rates = [result[r.name]["new"] for r in regions]
        print(f"  {'AVG GAIN':15} {statistics.mean(gains):+.2f}pp   "
              f"{'SPREAD (stdev of new rates)':30} {statistics.stdev(new_rates):.2f}")
        print()


def write_report(regions, strategies, projections, out_path):
    lines = ["RESOURCE ALLOCATION SIMULATOR", "=" * 60,
              f"Total additional budget: {TOTAL_BUDGET:,} TZS", ""]

    for strategy_name in strategies:
        lines.append(f"--- {strategy_name} ---")
        allocation = strategies[strategy_name]
        result = projections[strategy_name]

        for region in regions:
            extra = allocation[region.name]
            r = result[region.name]
            lines.append(f"  {region.name:15} +{extra:9,.0f} TZS/pupil  "
                          f"pass rate: {r['old']:>5}% -> {r['new']:>5}%  (+{r['gain']}pp)")

        gains = [result[r.name]["gain"] for r in regions]
        new_rates = [result[r.name]["new"] for r in regions]
        lines.append(f"  {'AVG GAIN':15} {statistics.mean(gains):+.2f}pp   "
                      f"SPREAD(stdev of new rates): {statistics.stdev(new_rates):.2f}")
        lines.append("")

    with open(out_path, "w") as f:
        f.write("\n".join(lines))


# ----------------------------------------------------------------------
# Visualizations
# ----------------------------------------------------------------------
def plot_allocation_by_strategy(regions, strategies, out_path):
    fig, ax = plt.subplots(figsize=(9, 5))
    region_names = [r.name for r in regions]
    n_strategies = len(strategies)
    bar_width = 0.8 / n_strategies

    colors = ["#1F4E5F", "#4E8098", "#8FBDC9", "#C6484E"]

    for i, (strategy_name, allocation) in enumerate(strategies.items()):
        values = [allocation[name] for name in region_names]
        positions = [x + i * bar_width for x in range(len(region_names))]
        ax.bar(positions, values, width=bar_width, label=strategy_name,
               color=colors[i % len(colors)])

    ax.set_xticks([x + bar_width * (n_strategies - 1) / 2 for x in range(len(region_names))])
    ax.set_xticklabels(region_names, rotation=20)
    ax.set_ylabel("Extra funding per pupil (TZS)")
    ax.set_title("Extra Funding per Pupil by Allocation Strategy")
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_pass_rate_gain(regions, projections, out_path):
    fig, ax = plt.subplots(figsize=(9, 5))
    region_names = [r.name for r in regions]
    strategy_names = list(projections.keys())
    n_strategies = len(strategy_names)
    bar_width = 0.8 / n_strategies

    colors = ["#1F4E5F", "#4E8098", "#8FBDC9", "#C6484E"]

    for i, strategy_name in enumerate(strategy_names):
        values = [projections[strategy_name][name]["gain"] for name in region_names]
        positions = [x + i * bar_width for x in range(len(region_names))]
        ax.bar(positions, values, width=bar_width, label=strategy_name,
               color=colors[i % len(colors)])

    ax.set_xticks([x + bar_width * (n_strategies - 1) / 2 for x in range(len(region_names))])
    ax.set_xticklabels(region_names, rotation=20)
    ax.set_ylabel("Projected pass-rate gain (percentage points)")
    ax.set_title("Projected Pass-Rate Gain by Allocation Strategy\n(gain shrinks where teacher attrition is high, even with more funding)")
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_equity_efficiency_tradeoff(regions, projections, out_path):
    fig, ax = plt.subplots(figsize=(7, 5.5))

    for strategy_name, result in projections.items():
        gains = [result[r.name]["gain"] for r in regions]
        new_rates = [result[r.name]["new"] for r in regions]
        avg_gain = statistics.mean(gains)          # efficiency: bigger = better
        spread = statistics.stdev(new_rates)        # equity: smaller = better (less inequality)
        ax.scatter(spread, avg_gain, s=120)
        ax.annotate(strategy_name, (spread, avg_gain), textcoords="offset points",
                    xytext=(6, 6), fontsize=9)

    ax.set_xlabel("Inequality after allocation (stdev of regional pass rates) →")
    ax.set_ylabel("← Average pass-rate gain (efficiency)")
    ax.set_title("Equity vs Efficiency Trade-off by Strategy")
    ax.invert_xaxis()  # so "better equity" (lower stdev) is to the right, matching y-axis "better" being up
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close(fig)


def main():
    regions, strategies, projections = run_simulation()
    print_report(regions, strategies, projections)

    write_report(regions, strategies, projections, "output/report.txt")
    plot_allocation_by_strategy(regions, strategies, "output/allocation_by_strategy.png")
    plot_pass_rate_gain(regions, projections, "output/pass_rate_gain.png")
    plot_equity_efficiency_tradeoff(regions, projections, "output/equity_efficiency_tradeoff.png")
    print("Report and charts written to output/")


if __name__ == "__main__":
    main()
