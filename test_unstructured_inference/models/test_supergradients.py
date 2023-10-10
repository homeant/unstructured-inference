import torch
import numpy as np
from PIL import Image
from unittest import mock
from unstructured_inference.models import super_gradients
from unstructured_inference.constants import Source


def test_supergradients_model():
    model_path = ""
    model = super_gradients.UnstructuredSuperGradients()
    with mock.patch("builtins.open", mock.mock_open()), mock.patch(
        "yaml.safe_load", mock.MagicMock(return_value={"names": ["a", "b"]})
    ) as mock_yaml_load, mock.patch("torch.load", lambda x: torch.nn.Linear(2, 1)):
        model.initialize(
            model_arch="resnet18",
            model_path=model_path,
            dataset_yaml_path="test_yaml_path",
            callback=lambda img_arr, model: [[np.zeros(4), 0, 0.7, 1]],
        )
    img = Image.open("sample-docs/loremipsum.jpg")
    el, *_ = model(img)
    mock_yaml_load.assert_called_once()
    assert el.source == Source.SUPER_GRADIENTS
    assert el.prob == 0.7