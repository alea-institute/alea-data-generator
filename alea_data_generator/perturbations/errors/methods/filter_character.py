"""
Character-level error method for filtering characters based on a condition.
"""

# imports
from typing import List, Optional, Callable


# local imports
from alea_data_generator.perturbations.errors.config import (
    ErrorConfig,
    ErrorSampleType,
    ErrorDistributionType,
)
from alea_data_generator.perturbations.errors.methods.base_character import (
    BaseCharacterErrorMethod,
)


class FilterCharacterErrorMethod(BaseCharacterErrorMethod):
    """
    Base class for character-level error methods.
    """

    def __init__(
        self, config: ErrorConfig, filter_method: Callable[[str], bool] = lambda x: True
    ):
        """
        Initialize the character-level error method.

        Args:
            config: Error configuration.
            filter_method: Method to filter characters.
        """
        super().__init__(config)
        self.input_string: str = ""
        self.filter_method: Callable[[str], bool] = filter_method

    def get_positions(
        self, length: int, input_string: Optional[str] = None
    ) -> List[int]:
        """
        Get valid positions to replace from the input string.

        Args:
            length: Length of the input string.
            input_string: Input string to get positions from.

        Returns:
            List of positions to replace
        """
        # handle case with no input string or length
        if length == 0 or input_string is None:
            return []

        # get valid whitespace positions
        valid_positions = [
            i for i in range(length) if self.filter_method(input_string[i])
        ]

        # handle case with independent rate
        if self.config.error_sample_type == ErrorSampleType.INDEPENDENT_RATE:
            rate = self.config.rate
            if rate == 0 or rate is None:
                return []
            if rate == 1:
                return valid_positions
            return [i for i in valid_positions if self.rng.random() < rate]

        # handle case with fixed count or sampled count
        if self.config.error_sample_type == ErrorSampleType.FIXED_COUNT:
            count = min(self.config.distribution_kwargs["count"], len(valid_positions))
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
            return valid_positions

        # get numpy array with choices
        choice_array = self.rng.choice(valid_positions, size=count, replace=False)

        # return as list
        return choice_array.tolist()  # type: ignore
