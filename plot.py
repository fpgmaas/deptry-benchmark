import matplotlib.pyplot as plt
import numpy as np
import json

input_file = 'benchmark_results/benchmark_summary.json'

def read_from_file():
    with open(input_file, 'r') as f:
        return json.load(f)

def plot_data(data):
    fig, ax = plt.subplots(figsize=(8, 6))  # Adjusted for potentially more bars
    
    repositories = set()
    for version_data in data.values():
        for repo, _ in version_data:
            repositories.add(repo)
    repositories = sorted(repositories)
    
    positions = np.arange(len(repositories))
    bar_width = 0.2  # Adjusted to fit more versions
    offset_increment = bar_width
    
    # Define a larger color palette, ensure no green if not liked
    color_palette = ['#4c78a8', '#f58518', '#e45756', '#72b7b2', '#ff9da6', '#79706e', '#d67195', '#b279a2']
    
    version_keys = sorted(data.keys())
    for version_index, version in enumerate(version_keys):
        offset = version_index * offset_increment
        times = [next((time for repo, time in data[version] if repo == r), 0) for r in repositories]
        ax.barh(positions + offset, times, bar_width, label=version, color=color_palette[version_index % len(color_palette)])
    
    ax.set_xlabel('Time (ms)')
    ax.set_title('deptry Benchmark Comparison Across Versions')
    ax.set_yticks(positions + bar_width / 2)
    ax.set_yticklabels(repositories)
    ax.legend()
    
    plt.tight_layout()
    plt.grid(visible=False)
    plt.show()

data = read_from_file()
plot_data(data)
