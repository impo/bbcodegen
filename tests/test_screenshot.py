import pytest
from pathlib import Path

from bbcodegen import screenshot

SAMPLE_VIDEO_INTERVAL = 10 # Seconds
SAMPLE_VIDEO_LENGTH = 60 # Seconds
SAMPLE_VIDEO_SHOTS = 6 # Number of screenshots that should be generated from sample video
SAMPLE_MAX_SHOTS = 4 # Number of screenshots to retain

@pytest.fixture
def sample_video_path():
    return Path.cwd() / "tests" / "data" / "fruit-and-vegetable-detection.mp4"

def test_mkScreenshot(sample_video_path, tmp_path):
    assert screenshot.mkScreenshot(sample_video_path, tmp_path, 10) == True

def test_getDuration(sample_video_path):
    assert screenshot.getDuration(sample_video_path, SAMPLE_VIDEO_INTERVAL) == SAMPLE_VIDEO_LENGTH

def test_getDurationCount(sample_video_path):
    assert screenshot.getDurationCount(sample_video_path, SAMPLE_VIDEO_INTERVAL) == (SAMPLE_VIDEO_LENGTH, SAMPLE_VIDEO_SHOTS)

def test_mkScreenshots(sample_video_path):
    (tmpdir, screenshots) = screenshot.mkScreenshots(sample_video_path, SAMPLE_VIDEO_INTERVAL, SAMPLE_MAX_SHOTS)
    assert len(screenshots) == 4
    assert Path.exists(Path(tmpdir.name)) == True
    for shot in screenshots:
        assert Path.exists(Path(shot)) == True