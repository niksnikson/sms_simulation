import json
import pytest
from unittest.mock import MagicMock
import sender

@pytest.fixture
def mock_redis(mocker):
    return mocker.patch('sender.redis.Redis', autospec=True)

@pytest.fixture
def mock_pika(mocker):
    return mocker.patch('sender.pika.BlockingConnection', autospec=True)

def test_send_message_success(mock_redis, mock_pika):
    # Arrange
    mock_channel = MagicMock()
    mock_method = MagicMock()
    mock_method.delivery_tag = 'test_delivery_tag'
    mock_pika.return_value.channel.return_value = mock_channel

    # Simulate message
    message = {'phone_number': '1234567890', 'message': 'Hello'}
    body = json.dumps(message)
    r = mock_redis.return_value

    # Act
    sender.send_message(mock_channel, mock_method, None, body, r, 1.0, 0)

    # Assert
    r.incr.assert_any_call('sent_count')
    mock_channel.basic_ack.assert_called_once_with(delivery_tag='test_delivery_tag')

def test_send_message_failure(mock_redis, mock_pika):
    
    mock_channel = MagicMock()
    mock_method = MagicMock()
    mock_method.delivery_tag = 'test_delivery_tag'
    mock_pika.return_value.channel.return_value = mock_channel

    # Simulate message with failure
    message = {'phone_number': '1234567890', 'message': 'Hello'}
    body = json.dumps(message)
    r = mock_redis.return_value

    # Act
    sender.send_message(mock_channel, mock_method, None, body, r, 1.0, 1.0)

    # Assert
    r.incr.assert_any_call('sent_count')
    r.incr.assert_any_call('failed_count')
    mock_channel.basic_ack.assert_called_once_with(delivery_tag='test_delivery_tag')
