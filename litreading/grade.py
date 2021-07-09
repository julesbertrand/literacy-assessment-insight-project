import numpy.typing as npt
from typing import Union

from pathlib import Path

import pandas as pd
from loguru import logger

from litreading.base import BaseModel, load_model_from_file
from litreading.config import PREPROCESSING_STEPS
from litreading.preprocessor import LCSPreprocessor


class Grader(BaseModel):

    _preprocessor = LCSPreprocessor(**PREPROCESSING_STEPS)

    def __init__(
        self, model_filepath: Union[str, Path] = None, baseline_mode: bool = False
    ) -> None:
        super().__init__(baseline_mode)
        if not baseline_mode:
            self._model = load_model_from_file(model_filepath)
            logger.info(f"Model loaded from {model_filepath}: {self._model}")

    def grade(self, X: pd.DataFrame) -> npt.ArrayLike:
        y_pred = self._predict(X)
        return y_pred
