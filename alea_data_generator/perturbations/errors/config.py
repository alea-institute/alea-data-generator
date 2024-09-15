"""
Error configuration module.
"""

# future
from __future__ import annotations


# imports
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class ErrorSampleType(Enum):
    """
    Error sample types, e.g., independent rate, fixed count, sampled count
    per transformation.
    """

    INDEPENDENT_RATE = "independent_rate"
    FIXED_COUNT = "fixed_count"
    SAMPLED_COUNT = "sampled_count"


class ErrorDistributionType(Enum):
    """
    Error distribution types used for sampled counts, e.g., uniform, normal, poisson.
    """

    UNIFORM = "uniform"
    NORMAL = "normal"
    POISSON = "poisson"


@dataclass
class ErrorConfig:
    """
    Error configuration for a specific error method.
    """

    error_sample_type: ErrorSampleType
    error_distribution_type: Optional[ErrorDistributionType] = None
    rate: Optional[float] = None
    distribution_kwargs: Dict[str, Any] = field(default_factory=dict)
    method_kwargs: Dict[str, Any] = field(default_factory=dict)
    seed: Optional[int] = None

    @staticmethod
    def from_dict(config: Dict[str, Any]) -> ErrorConfig:
        """
        Create an error configuration from a dictionary.

        Args:
            config: Configuration dictionary.

        Returns:
            Error configuration.
        """
        # check that all keys and values are correctly typed
        error_sample_type = ErrorSampleType(config["error_sample_type"])
        error_distribution_type = (
            ErrorDistributionType(config.get("error_distribution_type"))
            if config.get("error_distribution_type")
            else None
        )

        rate = config.get("rate")
        distribution_kwargs = config.get("distribution_args", {})

        method_kwargs = config.get("method_args", {})
        seed = config.get("seed")

        if not isinstance(distribution_kwargs, dict):
            raise ValueError("distribution_args must be a dictionary")

        if not isinstance(method_kwargs, dict):
            raise ValueError("method_args must be a dictionary")

        if not isinstance(seed, int) and seed is not None:
            raise ValueError("seed must be an integer")

        return ErrorConfig(
            error_sample_type,
            error_distribution_type,
            rate,
            distribution_kwargs,
            method_kwargs,
            seed,
        )
