import pytest
from unittest.mock import MagicMock, patch
import monitor

@pytest.fixture
def mock_redis(mocker):
    return mocker.patch('monitor.redis.Redis', autospec=True)

@patch('time.sleep', return_value=None)
def test_monitor_progress(mock_sleep, mock_redis):
    # Arrange
    mock_redis_instance = MagicMock()
    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.side_effect = lambda x: {
        'sent_count': 10,
        'failed_count': 2,
        'total_time': 50.0
    }[x]

    # Act
    monitor.monitor_progress(interval=1, iterations=2)  # Run only 2 iterations for testing

    # Assert
    assert mock_redis_instance.get.call_count == 6  # 3 keys * 2 iterations
    mock_redis_instance.get.assert_any_call('sent_count')
    mock_redis_instance.get.assert_any_call('failed_count')
    mock_redis_instance.get.assert_any_call('total_time')
    mock_sleep.assert_called_with(1)
