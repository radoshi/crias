from unittest.mock import MagicMock, patch

import pytest

from crias import llms
from crias.llms import (
    LLM,
    Completion,
    OpenAIChat,
    SystemMessage,
    UserMessage,
    create_messages,
    get,
)
from crias.prompts import Template


@pytest.fixture
def completion_mock():
    completion_mock = MagicMock()
    completion_mock.id = "test_id"
    completion_mock.object = "test_object"
    completion_mock.created = 123
    completion_mock.model = "test_model"
    completion_mock.choices = [
        llms.Choice(
            index=0,
            message=llms.UserMessage(content="test_choice"),
            finish_reason="test_reason",
        )
    ]
    completion_mock.usage = llms.Usage(
        prompt_tokens=1, completion_tokens=1, total_tokens=1
    )
    return completion_mock


def test_create(completion_mock):
    with patch(
        "openai.ChatCompletion.create", return_value=completion_mock
    ) as mocked_create:
        openai_chat = OpenAIChat(model="gpt-3.5-turbo", api_key="test_api_key")
        assert openai_chat.create() == Completion(
            id="test_id",
            object="test_object",
            created=123,
            model="test_model",
            choices=[
                llms.Choice(
                    index=0,
                    message=UserMessage(content="test_choice"),
                    finish_reason="test_reason",
                )
            ],
            usage=llms.Usage(prompt_tokens=1, completion_tokens=1, total_tokens=1),
        )
        mocked_create.assert_called_once()


@pytest.mark.asyncio
async def test_acreate(completion_mock):
    with patch(
        "openai.ChatCompletion.acreate", return_value=completion_mock
    ) as mocked_acreate:
        openai_chat = OpenAIChat(model="gpt-3.5-turbo", api_key="test_api_key")
        assert await openai_chat.acreate(api_key="test_api_key") == Completion(
            id="test_id",
            object="test_object",
            created=123,
            model="test_model",
            choices=[
                llms.Choice(
                    index=0,
                    message=UserMessage(content="test_choice"),
                    finish_reason="test_reason",
                )
            ],
            usage=llms.Usage(prompt_tokens=1, completion_tokens=1, total_tokens=1),
        )
        mocked_acreate.assert_called_once()


def test__serialize():
    openai_chat = OpenAIChat(model="gpt-3.5-turbo", api_key="test_api_key")
    expected = {"model": "gpt-3.5-turbo", "api_key": "test_api_key", "messages": []}
    assert openai_chat._serialize() == expected


def test_get():
    assert isinstance(get("gpt-3.5-turbo"), LLM)

    with pytest.raises(ValueError):
        get("non-existent-model")


def test_create_messages():
    messages = create_messages(system="system message", user="user message")
    assert len(messages) == 2
    assert messages[0]["content"] == "system message"
    assert messages[0]["role"] == "system"
    assert messages[1]["content"] == "user message"
    assert messages[1]["role"] == "user"

    messages = create_messages(system="system message")
    assert len(messages) == 1
    assert messages[0]["content"] == "system message"
    assert messages[0]["role"] == "system"

    messages = create_messages(user="user message")
    assert len(messages) == 1
    assert messages[0]["content"] == "user message"
    assert messages[0]["role"] == "user"


def test_user_message_from_template():
    template = Template(content="This is a test message")
    user_message = UserMessage.from_template(template)
    assert user_message.role == "user"
    assert user_message.content == "This is a test message"


def test_system_message_from_template():
    template = Template(content="This is a test message")
    system_message = SystemMessage.from_template(template)
    assert system_message.role == "system"
    assert system_message.content == "This is a test message"
