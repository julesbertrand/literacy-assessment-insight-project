import numpy.typing as npt
from typing import Union

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from sklearn.pipeline import Pipeline

from litreading.config import BASELINE_MODEL_PREDICTION_COL, PREPROCESSING_STEPS
from litreading.preprocessor import LCSPreprocessor
from litreading.utils.files import open_file


@dataclass
class Dataset:
    X_train_raw: pd.DataFrame
    X_test_raw: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    X_train: pd.DataFrame = field(init=False, default=None)
    X_test: pd.DataFrame = field(init=False, default=None)


class BaseModel:
    _preprocessor = LCSPreprocessor(**PREPROCESSING_STEPS)

    def __init__(self, baseline_mode: bool = False) -> None:
        if not isinstance(baseline_mode, bool):
            raise TypeError("baseline_mode must be a boolean")
        self._baseline_mode = baseline_mode
        self._model = None  # Must be redefined in child class

    @property
    def model(self) -> Pipeline:
        return self._model

    @property
    def preprocessor(self) -> LCSPreprocessor:
        return self._preprocessor

    @property
    def baseline_mode(self) -> bool:
        return self._baseline_mode

    def _predict(self, X: pd.DataFrame) -> npt.ArrayLike:
        X_processed = self.preprocessor.preprocess_data(X, verbose=False)
        if self.baseline_mode:
            y_pred = X_processed[BASELINE_MODEL_PREDICTION_COL].values
        else:
            y_pred = self.model.predict(X_processed)
        return y_pred


def load_model_from_file(model_filepath: Union[str, Path]) -> Pipeline:
    model_filepath = Path(model_filepath)
    if not Path(model_filepath).is_file():
        raise FileNotFoundError(model_filepath)
    if model_filepath.suffix != ".pkl":
        raise ValueError("Please give a path to pickle file")

    model = open_file(model_filepath)

    if not isinstance(model, Pipeline):
        raise ValueError("Incompatible model: please give a filepath to a sklearn pipeline object")

    return model