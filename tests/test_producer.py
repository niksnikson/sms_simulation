import pytest
from unittest.mock import patch, MagicMock
import producer
import json

@pytest.fixture
def mock_pika(mocker):
    return mocker.patch('producer.pika.BlockingConnection', autospec=True)

def test_generate_message():
    # Act
    message = producer.generate_message()

    # Assert
    assert len(message['phone_number']) == 10
    assert message['phone_number'].isdigit()
    assert len(message['message']) == 100
    assert isinstance(message['message'], str)

def test_produce_messages(mock_pika):
    # Arrange
    mock_channel = MagicMock()
    mock_pika.return_value.channel.return_value = mock_channel
    message_count = 10

    # Act
    producer.produce_messages(count=message_count)

    # Assert
    assert mock_channel.queue_declare.called_once_with(queue='sms_queue', durable=True)
    assert mock_channel.basic_publish.call_count == message_count

    # Check the structure of the published message
    args, kwargs = mock_channel.basic_publish.call_args
    assert kwargs['exchange'] == ''
    assert kwargs['routing_key'] == 'sms_queue'
    assert isinstance(json.loads(kwargs['body']), dict)  # Check if the body is a valid JSON dict
    assert kwargs['properties'].delivery_mode == 2  # Ensure message is persistent
