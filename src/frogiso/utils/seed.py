"""Deterministic seed helper for Python, NumPy, and optional torch."""

from __future__ import annotations

import os
import random

import numpy as np


def set_global_seed(seed: int) -> int:
    """Seed Python, NumPy, and torch if installed, returning the normalized seed."""

    normalized_seed = int(seed)
    os.environ["PYTHONHASHSEED"] = str(normalized_seed)
    random.seed(normalized_seed)
    np.random.seed(normalized_seed)

    try:
        import torch
    except ImportError:
        pass
    else:
        torch.manual_seed(normalized_seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(normalized_seed)

    return normalized_seed
