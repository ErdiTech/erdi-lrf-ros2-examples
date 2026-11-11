import os
import py_compile
import sys
from glob import glob

import pytest
import yaml

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
from erdi_lrf_examples.filters import MedianFilter, SlewLimiter  # noqa: E402


def test_median_rejects_single_spike():
    f = MedianFilter(5)
    out = [f.update(v) for v in [2.0, 2.0, 99.0, 2.0, 2.0]]
    assert out[-1] == 2.0


def test_median_ignores_nan():
    f = MedianFilter(3)
    f.update(1.0)
    assert f.update(float("nan")) == 1.0


def test_median_window_must_be_odd():
    with pytest.raises(ValueError):
        MedianFilter(4)


def test_slew_limiter_rejects_jump():
    s = SlewLimiter(max_rate=10.0)
    assert s.update(5.0, 0.0) == 5.0
    assert s.update(500.0, 0.1) is None
    assert s.update(5.2, 0.2) == 5.2


@pytest.mark.parametrize("path", glob(os.path.join(ROOT, "launch", "*.py")) + glob(os.path.join(ROOT, "erdi_lrf_examples", "*.py")))
def test_python_files_compile(path):
    py_compile.compile(path, doraise=True)


@pytest.mark.parametrize("path", glob(os.path.join(ROOT, "config", "*.yaml")) + glob(os.path.join(ROOT, "rviz", "*.rviz")))
def test_yaml_parses(path):
    assert yaml.safe_load(open(path)) is not None
