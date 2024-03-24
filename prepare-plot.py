from pathlib import Path
import re
import json

benchmark_folder = Path('benchmark_results')
output_file = benchmark_folder / 'benchmark_summary.json'

def extract_mean_time(file_path):
    content = file_path.read_text()  # Using read_text() on Path object
    # Search for time in milliseconds
    match_ms = re.search(r'Time \(mean ± σ\):[ \t]+([0-9.]+) ms', content)
    if match_ms:
        return float(match_ms.group(1))
    # Search for time in seconds and convert to milliseconds
    match_s = re.search(r'Time \(mean ± σ\):[ \t]+([0-9.]+) s', content)
    if match_s:
        return float(match_s.group(1)) * 1000  # Convert seconds to milliseconds
    return None

def extract_data():
    run_times = {}
    for file in benchmark_folder.glob('*_benchmark.txt'):  # Using glob to find matching files
        repo, _, version, _ = file.stem.rsplit('_', 3)  # Using stem to get the file name without suffix
        mean_time = extract_mean_time(file)
        if mean_time is not None:
            if version not in run_times:
                run_times[version] = []
            run_times[version].append((repo, mean_time))

    return run_times

def write_to_file(data):
    output_file.write_text(json.dumps(data, indent=2))  # Using write_text() on Path object

run_times = extract_data()
write_to_file(run_times)
