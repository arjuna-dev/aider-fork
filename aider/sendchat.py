import hashlib
import json

import backoff
import httpx
import openai

from aider.dump import dump  # noqa: F401
from aider.litellm import litellm

from dataclasses import dataclass
from typing import List
import time

@dataclass
class Usage:
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

@dataclass
class Message:
    content: str
    role: str

@dataclass
class Choices:
    finish_reason: str
    index: int
    message: Message

@dataclass
class ModelResponse:
    id: str
    choices: List[Choices]
    created: int
    model: str
    object: str
    system_fingerprint: str
    usage: Usage

def rectify_text(content: str) -> ModelResponse:
    message = Message(content=content, role='assistant')
    choice = Choices(finish_reason='stop', index=0, message=message)
    usage = Usage(completion_tokens=37, prompt_tokens=1576, total_tokens=1613)
    model_response = ModelResponse(
        id='chatcmpl-9XEpc5YaNIltTVcv1sxmbsLJi1ZO7',
        choices=[choice],
        created=int(time.time()),
        model='gpt-4o-2024-05-13',
        object='chat.completion',
        system_fingerprint='fp_319be4768e',
        usage=usage
    )
    return model_response


# from diskcache import Cache


CACHE_PATH = "~/.aider.send.cache.v1"
CACHE = None
# CACHE = Cache(CACHE_PATH)


def should_giveup(e):
    if not hasattr(e, "status_code"):
        return False

    if type(e) in (
        httpx.ConnectError,
        httpx.RemoteProtocolError,
        httpx.ReadTimeout,
    ):
        return False

    return not litellm._should_retry(e.status_code)


@backoff.on_exception(
    backoff.expo,
    (
        httpx.ConnectError,
        httpx.RemoteProtocolError,
        httpx.ReadTimeout,
        litellm.exceptions.APIConnectionError,
        litellm.exceptions.APIError,
        litellm.exceptions.RateLimitError,
        litellm.exceptions.ServiceUnavailableError,
        litellm.exceptions.Timeout,
    ),
    giveup=should_giveup,
    max_time=60,
    on_backoff=lambda details: print(
        f"{details.get('exception','Exception')}\nRetry in {details['wait']:.1f} seconds."
    ),
)
def send_with_retries(model_name, messages, functions, stream, temperature=0):
    kwargs = dict(
        model=model_name,
        messages=messages,
        temperature=temperature,
        stream=stream,
    )
    if functions is not None:
        kwargs["functions"] = functions

    key = json.dumps(kwargs, sort_keys=True).encode()

    # Generate SHA1 hash of kwargs and append it to chat_completion_call_hashes
    hash_object = hashlib.sha1(key)

    if not stream and CACHE is not None and key in CACHE:
        return hash_object, CACHE[key]

    # del kwargs['stream']
    # sentinel = "END"
    # res = ""
    # for line in iter(input, sentinel):
    #     res += line + "\n"
    # res = input("Paste your chatGPT response here: ")

    res = rectify_text('Documents/mydocs/Programming/aider_test/main.py\n```python\n<<<<<<< SEARCH\nfor i in range(5):\n=======\nfor i in range(10):\n>>>>>>> REPLACE\n```')

    # res = litellm.completion(**kwargs)
    print('resresres: ', res)

    if not stream and CACHE is not None:
        CACHE[key] = res

    return hash_object, res


def simple_send_with_retries(model_name, messages):
    try:
        _hash, response = send_with_retries(
            model_name=model_name,
            messages=messages,
            functions=None,
            stream=False,
        )
        return response.choices[0].message.content
    except (AttributeError, openai.BadRequestError):
        return
