import hashlib
import json
import time

from aider.dump import dump  # noqa: F401
from aider.exceptions import LiteLLMExceptions
from aider.llm import litellm

from dataclasses import dataclass
from typing import List
import time

import random
import string

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


def generate_random_string(length=29):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def prepare_text(content: str) -> ModelResponse:
    random_string_1 = generate_random_string() # 'chatcmpl-9XEpc5YaNIltTVcv1sxmbsLJi1ZO7'
    message = Message(content=content, role='assistant')
    choice = Choices(finish_reason='stop', index=0, message=message)
    usage = Usage(completion_tokens=0, prompt_tokens=0, total_tokens=0)
    model_response = ModelResponse(
        id='chatcmpl-'+random_string_1,
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

RETRY_TIMEOUT = 60


def send_completion(
    model_name,
    messages,
    functions,
    stream,
    temperature=0,
    extra_params=None,
):
    kwargs = dict(
        model=model_name,
        messages=messages,
        stream=stream,
    )
    if temperature is not None:
        kwargs["temperature"] = temperature

    if functions is not None:
        function = functions[0]
        kwargs["tools"] = [dict(type="function", function=function)]
        kwargs["tool_choice"] = {"type": "function", "function": {"name": function["name"]}}

    if extra_params is not None:
        kwargs.update(extra_params)

    key = json.dumps(kwargs, sort_keys=True).encode()

    # Generate SHA1 hash of kwargs and append it to chat_completion_call_hashes
    hash_object = hashlib.sha1(key)

    if not stream and CACHE is not None and key in CACHE:
        return hash_object, CACHE[key]

    # del kwargs['stream']

    input("Press Enter to continue...")
    # Ensure the file exists by opening in append mode and then closing it
    with open('response.txt', 'a'):
        pass

    # Now read the file
    with open('response.txt', 'r') as file:
        res = file.read()
    # res = res.encode().decode('unicode_escape')
    res = prepare_text(res)

    # res = litellm.completion(**kwargs)

    if not stream and CACHE is not None:
        CACHE[key] = res

    return hash_object, res

# def simple_send_with_retries(model_name, messages):
#     try:
#         _hash, response = send_with_retries(
#             model_name=model_name,
#             messages=messages,
#             functions=None,
#             stream=False,
#         )
#         return response.choices[0].message.content
#     except (AttributeError, openai.BadRequestError):
#         return

def simple_send_with_retries(model, messages):
    litellm_ex = LiteLLMExceptions()

    retry_delay = 0.125
    while True:
        try:
            kwargs = {
                "model_name": model.name,
                "messages": messages,
                "functions": None,
                "stream": False,
                "temperature": None if not model.use_temperature else 0,
                "extra_params": model.extra_params,
            }

            _hash, response = send_completion(**kwargs)
            if not response or not hasattr(response, "choices") or not response.choices:
                return None
            return response.choices[0].message.content
        except litellm_ex.exceptions_tuple() as err:
            ex_info = litellm_ex.get_ex_info(err)

            print(str(err))
            if ex_info.description:
                print(ex_info.description)

            should_retry = ex_info.retry
            if should_retry:
                retry_delay *= 2
                if retry_delay > RETRY_TIMEOUT:
                    should_retry = False

            if not should_retry:
                return None

            print(f"Retrying in {retry_delay:.1f} seconds...")
            time.sleep(retry_delay)
            continue
        except AttributeError:
            return None
