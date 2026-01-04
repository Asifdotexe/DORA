
from typing import List, Optional, Dict, Literal
from pathlib import Path
from pydantic import BaseModel, Field, field_validator

class ProfileStep(BaseModel):
    enabled: bool = True

class UnivariateStep(BaseModel):
    enabled: bool = True
    plot_types: Dict[str, List[str]] = Field(
        default_factory=lambda: {
            "numerical": ["histogram", "boxplot"],
            "categorical": ["barplot"]
        }
    )

class BivariateStep(BaseModel):
    enabled: bool = True
    target_centric: bool = True

class MultivariateStep(BaseModel):
    enabled: bool = True
    correlation_cols: List[str] = Field(default_factory=list)

class AnalysisStep(BaseModel):
    profile: Optional[ProfileStep] = None
    univariate: Optional[UnivariateStep] = None
    bivariate: Optional[BivariateStep] = None
    multivariate: Optional[MultivariateStep] = None

class Config(BaseModel):
    input_file: Path
    output_dir: Path
    report_title: str = "EDA Report"
    target_variable: Optional[str] = None
    analysis_pipeline: List[AnalysisStep] = Field(default_factory=list)

    @field_validator("input_file")
    @classmethod
    def validate_input_file(cls, v: Path) -> Path:
        if not v.exists():
            raise ValueError(f"Input file not found: {v}")
        return v
