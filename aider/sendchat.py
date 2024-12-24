import hashlib
import json
import time

from aider.dump import dump  # noqa: F401
from aider.exceptions import LiteLLMExceptions
from aider.llm import litellm

from dataclasses import dataclass
from typing import List
import time

import pychrome
import random
import string
import subprocess
from time import sleep

chrome_started = False

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

def prepare_response(content: str) -> ModelResponse:
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

def start_chrome():
    command = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --disable-extensions --user-data-dir=/tmp/chrome-debug-profile"

    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sleep(1)

# Callback for when the page navigation is complete
def on_frame_stopped_loading(**kwargs):
    global navigation_done
    navigation_done = True
    print("Navigation stopped.")

def send_message_to_chatgpt(message):
    def escape_string_for_js(input_string):
        return (
            input_string
            .replace('\\', '\\\\')  # Escape backslashes
            .replace('"', '\\"')    # Escape double quotes
            .replace('\n', '\\n')   # Escape newlines
        )
    message = escape_string_for_js(message)
    try:
        # Connect to Chrome
        browser = pychrome.Browser(url="http://127.0.0.1:9222")

        # Use the first available tab (or create a new one if desired)
        tabs = browser.list_tab()
        tab = tabs[0] if tabs else browser.new_tab()

        # Add the event listener for navigation
        tab.Page.frameStoppedLoading = on_frame_stopped_loading

        # Start the tab
        tab.start()

        # Navigate to the initial URL
        print("Navigating to https://chatgpt.com...")
        tab.Page.navigate(url="https://chatgpt.com")

        # Wait for the initial navigation to complete
        tab.wait(4)
        print("Initial navigation complete.")

        # Monitor until the user navigates to the desired URL
        navigation_done = False
        print("Waiting for user to navigate to https://chatgpt.com/?model=gpt-4o...")
        while not navigation_done:
            # Check the current URL
            response = tab.Runtime.evaluate(expression="window.location.href")
            print("Evaluate response:", response)
            current_url = response["result"]["value"]
            print(f"Current URL: {current_url}")

            if current_url == "https://chatgpt.com/?model=gpt-4o":
                print("Desired URL detected!")
                break

            # Sleep briefly to avoid busy waiting
            time.sleep(2)

        # Write to the <p> element
        script = f"""
        var pElement = document.querySelector('p[data-placeholder="Message ChatGPT"]');
        if (pElement) {{
            pElement.innerHTML = "{message}";
        }} else {{
            throw new Error("pElement not found");
        }}
        """
        response = tab.Runtime.evaluate(expression=script)
        print("Evaluate response:", response)
        print("Text written to the <p> element.")

        # Click the send button
        script = """
        var sendButton = document.querySelector('button[data-testid="send-button"]');
        if (sendButton) {{
            sendButton.click();
        }} else {{
            throw new Error("sendButton not found");
        }}
        """
        response = tab.Runtime.evaluate(expression=script)
        print("Evaluate response:", response)
        print("Send button clicked.")

        return tab

    except Exception as e:
        print("Error:", e)


def fetch_chatgpt_response(tab):
    try:
        # Fetch the entire HTML of the last <article>
        print("Fetching the HTML of the last <article>...")
        response = tab.Runtime.evaluate(expression="""
            (function() {
                const articles = document.querySelectorAll('article');
                if (articles.length === 0) return null;
                const lastArticle = articles[articles.length - 1];
                return lastArticle.innerText;
            })();
        """)

        article_html = response.get('result', {}).get('value')

        def remove_lines(text):
            lines = text.split('\n')
            # Remove the first 3 lines and the last 2 lines
            lines = lines[3:-2]
            return '\n'.join(lines)
        
        article_html = remove_lines(article_html)

        print("Article HTML:", article_html)
        # save the html to a file
        with open('article.txt', 'w') as f:
            f.write(article_html)
            f.close()
        return article_html

    except Exception as e:
        print("Error:", e)
        return None

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

    global chrome_started
    if not chrome_started:
        start_chrome()
        chrome_started = True

    with open('messages.txt', 'w') as file:
        file.write(str(messages))

    messages_str = str(messages)

    tab = send_message_to_chatgpt(messages_str)

    input("Press Enter when chatGPT response is ready")

    fetch_chatgpt_response(tab)
    with open('response.txt', 'a'):
        pass
    with open('response.txt', 'r') as file:
        res = file.read()

    res = prepare_response(res)

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
