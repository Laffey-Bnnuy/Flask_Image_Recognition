"""Route tests: home page, real valid image, invalid input, mocked model calls."""
import io
from unittest.mock import patch

from PIL import Image

ERROR_TEXT = b"File cannot be processed."


def make_rgb_png():
    """Return an in-memory 64x64 RGB PNG file."""
    buffer = io.BytesIO()
    Image.new("RGB", (64, 64), (255, 255, 255)).save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def test_home_page_loads(client):
    """GET / returns the upload page."""
    response = client.get("/")
    assert response.status_code == 200


def test_valid_image_gives_prediction_not_error(client):
    """A real RGB image is processed without the error message."""
    response = client.post(
        "/prediction",
        data={"file": (make_rgb_png(), "digit.png")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert ERROR_TEXT not in response.data


def test_non_image_upload_shows_error(client):
    """Bytes that are not an image show the friendly error."""
    response = client.post(
        "/prediction",
        data={"file": (io.BytesIO(b"not an image"), "fake.jpg")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert ERROR_TEXT in response.data


def test_get_on_prediction_not_allowed(client):
    """/prediction accepts POST only."""
    assert client.get("/prediction").status_code == 405


def test_prediction_route_uses_model_functions(client):
    """The route calls preprocessing, then prediction (model mocked)."""
    with patch("app.preprocess_img", return_value="array") as mock_pre, \
         patch("app.predict_result", return_value=3) as mock_pred:
        response = client.post(
            "/prediction",
            data={"file": (make_rgb_png(), "digit.png")},
            content_type="multipart/form-data",
        )
    assert response.status_code == 200
    mock_pre.assert_called_once()
    mock_pred.assert_called_once_with("array")
