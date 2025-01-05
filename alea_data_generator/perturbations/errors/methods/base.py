"""
Base class for error methods.
"""

# imports
import random
from abc import ABC, abstractmethod
from typing import List, Optional

# packages
import numpy.random

from alea_data_generator.perturbations.errors.config import (
    ErrorConfig,
    ErrorDistributionType,
    ErrorSampleType,
)


class BaseErrorMethod(ABC):
    """
    Base class for error methods.
    """

    def __init__(self, config: ErrorConfig):
        """
        Initialize the error method with a configuration.

        Args:
            config: Error configuration.

        Returns:
            None.
        """
        # set the configuration
        self.config = config

        # create a method-specific rng and set seed if present in config
        self.rng: numpy.random.RandomState = numpy.random.RandomState()  # pylint: disable=no-member
        if self.config.seed is not None:
            self.rng.seed(self.config.seed)

    @abstractmethod
    def execute(self, input_string: str) -> str:
        """
        Execute the error method on the input string.

        Args:
            input_string: Input string.

        Returns:
            Modified string.
        """

    @abstractmethod
    def get_indices(self) -> List[int]:
        """
        Get the indices to sample from.  For character-level errors, this will be the indices of the characters in the
        input string, e.g., all characters or all punctuation characters.  For token-level errors, this will be the
        indices of the tokens in the input string, e.g., all tokens or all numeric tokens.

        Returns:
            List of indices.
        """

    # pylint: disable=unused-argument
    def get_positions(
        self, length: int, input_string: Optional[str] = None
    ) -> List[int]:
        """
        Get the positions to apply the error to based on the error configuration.

        If the error sample type is INDEPENDENT_RATE, the positions are sampled independently with the given rate,
        i.e., each position is sampled with probability rate.

        If the error sample type is FIXED_COUNT, the positions are sampled without replacement from the range of
        positions with the given count.

        If the error sample type is SAMPLED_COUNT, the positions are sampled without replacement from the range of
        positions with the count sampled from the given distribution.

        Args:
            length: Length of the input string.
            input_string: Input string, which may be required by some override methods.

        Returns:
            List of positions.
        """
        # jump out early if length is 0
        if length == 0:
            return []

        # handle case with independent rate
        if self.config.error_sample_type == ErrorSampleType.INDEPENDENT_RATE:
            rate = self.config.rate
            if rate == 0 or rate is None:
                return []
            if rate == 1:
                return list(range(length))
            return [i for i in range(length) if random.random() < rate]

        # handle case with fixed count or sampled count
        if self.config.error_sample_type == ErrorSampleType.FIXED_COUNT:
            count = self.config.distribution_kwargs["count"]
        elif self.config.error_sample_type == ErrorSampleType.SAMPLED_COUNT:
            if self.config.error_distribution_type == ErrorDistributionType.UNIFORM:
                count = self.rng.randint(**self.config.distribution_kwargs)
            elif self.config.error_distribution_type == ErrorDistributionType.NORMAL:
                count = self.rng.normal(**self.config.distribution_kwargs)
            elif self.config.error_distribution_type == ErrorDistributionType.POISSON:
                # sample a poisson distribution from inverse
                count = self.rng.poisson(**self.config.distribution_kwargs)
            else:
                raise ValueError(
                    f"Invalid error distribution type: {self.config.error_distribution_type}"
                )
        else:
            raise ValueError(
                f"Invalid error sample type: {self.config.error_sample_type}"
            )

        # if the count is greater than or equal to the length, return all positions
        if count >= length:
            return list(range(length))

        # get numpy array with choices
        choice_array = self.rng.choice(length, size=count, replace=False)

        # return as list
        return choice_array.tolist()  # type: ignore
