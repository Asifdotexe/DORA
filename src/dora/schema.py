"""
Defines the Pydantic schemas for the DORA configuration.
"""

from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class ProfileStep(BaseModel):
    """
    Configuration for the data profiling step.

    :param enabled: Whether to enable the profiling step.
    """

    enabled: bool = True


class UnivariateStep(BaseModel):
    """
    Configuration for the univariate analysis step.

    :param enabled: Whether to enable the univariate analysis.
    :param plot_types: Dictionary mapping variable types to list of plot types.
    :param max_categories: Maximum number of categories to display in categorical plots (default: 20).
    """

    enabled: bool = True
    plot_types: Dict[str, List[str]] = Field(
        default_factory=lambda: {
            "numerical": ["histogram", "boxplot"],
            "categorical": ["barplot"],
        }
    )
    max_categories: int = 20

    @field_validator("max_categories")
    @classmethod
    def validate_max_categories(cls, v: int) -> int:
        """
        Validates that max_categories is greater than 0.

        :param v: The value to validate.
        :raises ValueError: If v is less than or equal to 0.
        :return: The validated value.
        """
        if v <= 0:
            raise ValueError(f"max_categories must be greater than 0, got {v}")
        return v


class BivariateStep(BaseModel):
    """
    Configuration for the bivariate analysis step.

    :param enabled: Whether to enable the bivariate analysis.
    :param target_centric: If True, focuses on relationships with the target variable.
    :param max_categories: Maximum number of categories to display in categorical vs numerical plots (default: 20).
    """

    enabled: bool = True
    target_centric: bool = True
    max_categories: int = 20

    @field_validator("max_categories")
    @classmethod
    def validate_max_categories(cls, v: int) -> int:
        """
        Validates that max_categories is greater than 0.

        :param v: The value to validate.
        :raises ValueError: If v is less than or equal to 0.
        :return: The validated value.
        """
        if v <= 0:
            raise ValueError(f"max_categories must be greater than 0, got {v}")
        return v


class MultivariateStep(BaseModel):
    """
    Configuration for the multivariate analysis step.

    :param enabled: Whether to enable the multivariate analysis.
    :param correlation_cols: List of columns to include in correlation analysis.
                             Empty list implies all numerical columns.
    """

    enabled: bool = True
    correlation_cols: List[str] = Field(default_factory=list)


class AnalysisStep(BaseModel):
    """
    Container for a single step in the analysis pipeline.
    Only one field should be populated per instance.

    :param profile: Configuration for profiling, if this is a profiling step.
    :param univariate: Configuration for univariate analysis, if applicable.
    :param bivariate: Configuration for bivariate analysis, if applicable.
    :param multivariate: Configuration for multivariate analysis, if applicable.
    """

    profile: Optional[ProfileStep] = None
    univariate: Optional[UnivariateStep] = None
    bivariate: Optional[BivariateStep] = None
    multivariate: Optional[MultivariateStep] = None

    @model_validator(mode="after")
    def check_exactly_one_field(self) -> "AnalysisStep":
        """
        Validates that exactly one configuration field is set.

        :raises ValueError: If zero or more than one field is set.
        :return: The model instance.
        """
        fields = [self.profile, self.univariate, self.bivariate, self.multivariate]
        count = sum(1 for f in fields if f is not None)
        if count != 1:
            raise ValueError(
                "Exactly one analysis step must be provided (profile, univariate, bivariate, or multivariate)."
            )
        return self


class Config(BaseModel):
    """
    Main configuration for the DORA analysis.

    :param input_file: Path to the input dataset (CSV, Excel, etc.).
    :param output_dir: Directory where the report and charts will be saved.
    :param report_title: Title of the generated HTML report.
    :param target_variable: The name of the target variable for supervised analysis.
    :param analysis_pipeline: List of analysis steps to execute.
    """

    input_file: Path
    output_dir: Path
    report_title: str = "EDA Report"
    target_variable: Optional[str] = None
    analysis_pipeline: List[AnalysisStep] = Field(default_factory=list)
