## deptry-benchmark

Some scripts to help benchmark different versions of `deptry`. to get started:

```sh
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

To create some benchmarks, run e.g.

```sh
. ./script.sh 0.14.2 pypi
. ./script.sh 0.15.0 test-pypi
```

Then run

```sh
python prepare-plot.py
python plot.py
```