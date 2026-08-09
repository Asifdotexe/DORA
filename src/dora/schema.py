"""
Defines the Pydantic schemas for the DORA configuration.
"""

from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class Config(BaseModel):
    """Main configuration for the DORA analysis."""

    input_file: Path
    output_dir: Path
    report_title: str = "EDA Report"
    target_variable: str | None = None

    profile_enabled: bool = True
    univariate_enabled: bool = True
    bivariate_enabled: bool = True
    multivariate_enabled: bool = True

    univariate_plot_types: dict[str, list[str]] = Field(
        default_factory=lambda: {
            "numerical": ["histogram", "boxplot"],
            "categorical": ["barplot"],
        }
    )
    univariate_max_categories: int = 20
    bivariate_target_centric: bool = True
    bivariate_max_categories: int = 20
    multivariate_correlation_cols: list[str] = Field(default_factory=list)

    @field_validator("univariate_max_categories", "bivariate_max_categories")
    @classmethod
    def validate_max_categories(cls, v: int) -> int:
        if v <= 0:
            raise ValueError(f"max_categories must be greater than 0, got {v}")
        return v
