import time
import matplotlib.pyplot as plt
import sys

# Increase recursion limit (Ackermann function is very deep)
sys.setrecursionlimit(100000)

def ackermann(n, m):
    """
    Ackermann function implementation
    a(0, m) = m + 1
    a(n + 1, 0) = a(n, 1)
    a(n + 1, m + 1) = a(n, a(n + 1, m))
    """
    if n == 0:
        return m + 1
    elif m == 0:
        return ackermann(n - 1, 1)
    else:
        return ackermann(n - 1, ackermann(n, m - 1))

def compute_with_timeout(n, m, timeout=10):
    """
    Try to compute ackermann(n, m) with a timeout
    Returns (value, time) or (None, None) if timeout
    """
    start_time = time.time()
    try:
        result = ackermann(n, m)
        elapsed_time = time.time() - start_time
        return result, elapsed_time
    except RecursionError:
        print(f"RecursionError for a({n}, {m})")
        return None, None

# Compute a(i, i) for increasing values of i
results = []
times = []
values = []
indices = []

print("Computing Ackermann function a(i, i):")
print("=" * 50)

for i in range(5):  # Try up to a(9, 9), but we'll likely stop much earlier
    print(f"\nComputing a({i}, {i})...", end=" ", flush=True)

    start = time.time()
    value, compute_time = compute_with_timeout(i, i, timeout=30)

    if value is None:
        print(f"Could not compute (too large or recursion limit)")
        break

    elapsed = time.time() - start
    print(f"= {value}, time = {elapsed:.6f} seconds")

    indices.append(i)
    values.append(value)
    times.append(elapsed)

    # Stop if computation took more than 5 seconds
    if elapsed > 5:
        print(f"\nStopping: computation time exceeded 5 seconds")
        break

print("\n" + "=" * 50)
print("\nResults Summary:")
print("-" * 50)
for i, v, t in zip(indices, values, times):
    print(f"a({i}, {i}) = {v:>20}, time = {t:.6f} s")

# Create plots
if len(indices) > 0:
    fig, axes = plt.subplots(figsize=(14, 5))

    # Plot 1: Runtime vs i (linear scale)
    axes.plot(indices, times, 'bo-', markersize=8, linewidth=2)
    axes.set_xlabel('i', fontsize=12)
    axes.set_ylabel('runtime (sec)', fontsize=12)
    axes.set_title('a(i, i) runtime', fontsize=14)
    axes.grid(True, alpha=0.3)
    axes.set_xticks(indices)

    # Plot 2: Runtime vs i (log scale)
    #axes[1].semilogy(indices, times, 'ro-', markersize=8, linewidth=2)
    #axes[1].set_xlabel('i', fontsize=12)
    #axes[1].set_ylabel('Runtime (seconds, log scale)', fontsize=12)
    #axes[1].set_title('Ackermann Function a(i, i): Runtime (Log Scale)', fontsize=14)
    #axes[1].grid(True, alpha=0.3, which='both')
    #axes[1].set_xticks(indices)

    plt.tight_layout()
    plt.savefig(fname='image', dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: ackermann_runtime.png")

    # Additional plot: Values of a(i, i)
    fig2, ax = plt.subplots(figsize=(10, 6))
    ax.semilogy(indices, values, 'go-', markersize=8, linewidth=2)
    ax.set_xlabel('i', fontsize=12)
    ax.set_ylabel('a(i, i) value (log scale)', fontsize=12)
    ax.set_title('Ackermann Function a(i, i): Function Values', fontsize=14)
    ax.grid(True, alpha=0.3, which='both')
    ax.set_xticks(indices)

    plt.tight_layout()
    plt.savefig(fname='image2', dpi=300, bbox_inches='tight')
    print(f"Value plot saved to: ackermann_values.png")

    plt.close('all')
else:
    print("\nNo values computed successfully. Cannot create plots.")