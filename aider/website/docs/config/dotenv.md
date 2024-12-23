---
parent: Configuration
nav_order: 20
description: Using a .env file to store LLM API keys for aider.
---

# Config with .env

You can use a `.env` file to store API keys and other settings for the
models you use with aider.
You can also set many general aider options
in the `.env` file.

Aider will look for a `.env` file in these locations:

- Your home directory.
- The root of your git repo.
- The current directory.
- As specified with the `--env-file <filename>` parameter.

If the files above exist, they will be loaded in that order. Files loaded last will take priority.

{% include keys.md %}

## Sample .env file

Below is a sample `.env` file, which you
can also
[download from GitHub](https://github.com/Aider-AI/aider/blob/main/aider/website/assets/sample.env).

<!--[[[cog
from aider.args import get_sample_dotenv
from pathlib import Path
text=get_sample_dotenv()
Path("aider/website/assets/sample.env").write_text(text)
cog.outl("```")
cog.out(text)
cog.outl("```")
]]]-->
```
##########################################################
# Sample aider .env file.
# Place at the root of your git repo.
# Or use `aider --env <fname>` to specify.
##########################################################

#################
# LLM parameters:
#
# Include xxx_API_KEY parameters and other params needed for your LLMs.
# See https://aider.chat/docs/llms.html for details.

## OpenAI
#OPENAI_API_KEY=

## Anthropic
#ANTHROPIC_API_KEY=

##...

#############
# Main model:

## Specify the model to use for the main chat
#AIDER_MODEL=

## Use claude-3-opus-20240229 model for the main chat
#AIDER_OPUS=

## Use claude-3-5-sonnet-20241022 model for the main chat
#AIDER_SONNET=

## Use claude-3-5-haiku-20241022 model for the main chat
#AIDER_HAIKU=

## Use gpt-4-0613 model for the main chat
#AIDER_4=

## Use gpt-4o model for the main chat
#AIDER_4O=

## Use gpt-4o-mini model for the main chat
#AIDER_MINI=

## Use gpt-4-1106-preview model for the main chat
#AIDER_4_TURBO=

## Use gpt-3.5-turbo model for the main chat
#AIDER_35TURBO=

## Use deepseek/deepseek-coder model for the main chat
#AIDER_DEEPSEEK=

## Use o1-mini model for the main chat
#AIDER_O1_MINI=

## Use o1-preview model for the main chat
#AIDER_O1_PREVIEW=

########################
# API Keys and settings:

## Specify the OpenAI API key
#AIDER_OPENAI_API_KEY=

## Specify the Anthropic API key
#AIDER_ANTHROPIC_API_KEY=

## Specify the api base url
#AIDER_OPENAI_API_BASE=

## (deprecated, use --set-env OPENAI_API_TYPE=<value>)
#AIDER_OPENAI_API_TYPE=

## (deprecated, use --set-env OPENAI_API_VERSION=<value>)
#AIDER_OPENAI_API_VERSION=

## (deprecated, use --set-env OPENAI_API_DEPLOYMENT_ID=<value>)
#AIDER_OPENAI_API_DEPLOYMENT_ID=

## (deprecated, use --set-env OPENAI_ORGANIZATION=<value>)
#AIDER_OPENAI_ORGANIZATION_ID=

## Set an environment variable (to control API settings, can be used multiple times)
#AIDER_SET_ENV=

## Set an API key for a provider (eg: --api-key provider=<key> sets PROVIDER_API_KEY=<key>)
#AIDER_API_KEY=

#################
# Model settings:

## List known models which match the (partial) MODEL name
#AIDER_LIST_MODELS=

## Specify a file with aider model settings for unknown models
#AIDER_MODEL_SETTINGS_FILE=.aider.model.settings.yml

## Specify a file with context window and costs for unknown models
#AIDER_MODEL_METADATA_FILE=.aider.model.metadata.json

## Add a model alias (can be used multiple times)
#AIDER_ALIAS=

## Verify the SSL cert when connecting to models (default: True)
#AIDER_VERIFY_SSL=true

## Timeout in seconds for API calls (default: None)
#AIDER_TIMEOUT=

## Specify what edit format the LLM should use (default depends on model)
#AIDER_EDIT_FORMAT=

## Use architect edit format for the main chat
#AIDER_ARCHITECT=

## Specify the model to use for commit messages and chat history summarization (default depends on --model)
#AIDER_WEAK_MODEL=

## Specify the model to use for editor tasks (default depends on --model)
#AIDER_EDITOR_MODEL=

## Specify the edit format for the editor model (default: depends on editor model)
#AIDER_EDITOR_EDIT_FORMAT=

## Only work with models that have meta-data available (default: True)
#AIDER_SHOW_MODEL_WARNINGS=true

## Soft limit on tokens for chat history, after which summarization begins. If unspecified, defaults to the model's max_chat_history_tokens.
#AIDER_MAX_CHAT_HISTORY_TOKENS=

#################
# Cache settings:

## Enable caching of prompts (default: False)
#AIDER_CACHE_PROMPTS=false

## Number of times to ping at 5min intervals to keep prompt cache warm (default: 0)
#AIDER_CACHE_KEEPALIVE_PINGS=false

###################
# Repomap settings:

## Suggested number of tokens to use for repo map, use 0 to disable (default: 1024)
#AIDER_MAP_TOKENS=

## Control how often the repo map is refreshed. Options: auto, always, files, manual (default: auto)
#AIDER_MAP_REFRESH=auto

## Multiplier for map tokens when no files are specified (default: 2)
#AIDER_MAP_MULTIPLIER_NO_FILES=true

################
# History Files:

## Specify the chat input history file (default: .aider.input.history)
#AIDER_INPUT_HISTORY_FILE=.aider.input.history

## Specify the chat history file (default: .aider.chat.history.md)
#AIDER_CHAT_HISTORY_FILE=.aider.chat.history.md

## Restore the previous chat history messages (default: False)
#AIDER_RESTORE_CHAT_HISTORY=false

## Log the conversation with the LLM to this file (for example, .aider.llm.history)
#AIDER_LLM_HISTORY_FILE=

##################
# Output settings:

## Use colors suitable for a dark terminal background (default: False)
#AIDER_DARK_MODE=false

## Use colors suitable for a light terminal background (default: False)
#AIDER_LIGHT_MODE=false

## Enable/disable pretty, colorized output (default: True)
#AIDER_PRETTY=true

## Enable/disable streaming responses (default: True)
#AIDER_STREAM=true

## Set the color for user input (default: #00cc00)
#AIDER_USER_INPUT_COLOR=#00cc00

## Set the color for tool output (default: None)
#AIDER_TOOL_OUTPUT_COLOR=

## Set the color for tool error messages (default: #FF2222)
#AIDER_TOOL_ERROR_COLOR=#FF2222

## Set the color for tool warning messages (default: #FFA500)
#AIDER_TOOL_WARNING_COLOR=#FFA500

## Set the color for assistant output (default: #0088ff)
#AIDER_ASSISTANT_OUTPUT_COLOR=#0088ff

## Set the color for the completion menu (default: terminal's default text color)
#AIDER_COMPLETION_MENU_COLOR=

## Set the background color for the completion menu (default: terminal's default background color)
#AIDER_COMPLETION_MENU_BG_COLOR=

## Set the color for the current item in the completion menu (default: terminal's default background color)
#AIDER_COMPLETION_MENU_CURRENT_COLOR=

## Set the background color for the current item in the completion menu (default: terminal's default text color)
#AIDER_COMPLETION_MENU_CURRENT_BG_COLOR=

## Set the markdown code theme (default: default, other options include monokai, solarized-dark, solarized-light, or a Pygments builtin style, see https://pygments.org/styles for available themes)
#AIDER_CODE_THEME=default

## Show diffs when committing changes (default: False)
#AIDER_SHOW_DIFFS=false

###############
# Git settings:

## Enable/disable looking for a git repo (default: True)
#AIDER_GIT=true

## Enable/disable adding .aider* to .gitignore (default: True)
#AIDER_GITIGNORE=true

## Specify the aider ignore file (default: .aiderignore in git root)
#AIDER_AIDERIGNORE=.aiderignore

## Only consider files in the current subtree of the git repository
#AIDER_SUBTREE_ONLY=false

## Enable/disable auto commit of LLM changes (default: True)
#AIDER_AUTO_COMMITS=true

## Enable/disable commits when repo is found dirty (default: True)
#AIDER_DIRTY_COMMITS=true

## Attribute aider code changes in the git author name (default: True)
#AIDER_ATTRIBUTE_AUTHOR=true

## Attribute aider commits in the git committer name (default: True)
#AIDER_ATTRIBUTE_COMMITTER=true

## Prefix commit messages with 'aider: ' if aider authored the changes (default: False)
#AIDER_ATTRIBUTE_COMMIT_MESSAGE_AUTHOR=false

## Prefix all commit messages with 'aider: ' (default: False)
#AIDER_ATTRIBUTE_COMMIT_MESSAGE_COMMITTER=false

## Commit all pending changes with a suitable commit message, then exit
#AIDER_COMMIT=false

## Specify a custom prompt for generating commit messages
#AIDER_COMMIT_PROMPT=

## Perform a dry run without modifying files (default: False)
#AIDER_DRY_RUN=false

## Skip the sanity check for the git repository (default: False)
#AIDER_SKIP_SANITY_CHECK_REPO=false

## Enable/disable watching files for ai coding comments (default: False)
#AIDER_WATCH_FILES=false

########################
# Fixing and committing:

## Lint and fix provided files, or dirty files if none provided
#AIDER_LINT=false

## Specify lint commands to run for different languages, eg: "python: flake8 --select=..." (can be used multiple times)
#AIDER_LINT_CMD=

## Enable/disable automatic linting after changes (default: True)
#AIDER_AUTO_LINT=true

## Specify command to run tests
#AIDER_TEST_CMD=

## Enable/disable automatic testing after changes (default: False)
#AIDER_AUTO_TEST=false

## Run tests, fix problems found and then exit
#AIDER_TEST=false

############
# Analytics:

## Enable/disable analytics for current session (default: random)
#AIDER_ANALYTICS=

## Specify a file to log analytics events
#AIDER_ANALYTICS_LOG=

## Permanently disable analytics
#AIDER_ANALYTICS_DISABLE=false

############
# Upgrading:

## Check for updates and return status in the exit code
#AIDER_JUST_CHECK_UPDATE=false

## Check for new aider versions on launch
#AIDER_CHECK_UPDATE=true

## Show release notes on first run of new version (default: None, ask user)
#AIDER_SHOW_RELEASE_NOTES=

## Install the latest version from the main branch
#AIDER_INSTALL_MAIN_BRANCH=false

## Upgrade aider to the latest version from PyPI
#AIDER_UPGRADE=false

########
# Modes:

## Specify a single message to send the LLM, process reply then exit (disables chat mode)
#AIDER_MESSAGE=

## Specify a file containing the message to send the LLM, process reply, then exit (disables chat mode)
#AIDER_MESSAGE_FILE=

## Run aider in your browser (default: False)
#AIDER_GUI=false

## Enable automatic copy/paste of chat between aider and web UI (default: False)
#AIDER_COPY_PASTE=false

## Apply the changes from the given file instead of running the chat (debug)
#AIDER_APPLY=

## Apply clipboard contents as edits using the main model's editor format
#AIDER_APPLY_CLIPBOARD_EDITS=false

## Do all startup activities then exit before accepting user input (debug)
#AIDER_EXIT=false

## Print the repo map and exit (debug)
#AIDER_SHOW_REPO_MAP=false

## Print the system prompts and exit (debug)
#AIDER_SHOW_PROMPTS=false

#################
# Voice settings:

## Audio format for voice recording (default: wav). webm and mp3 require ffmpeg
#AIDER_VOICE_FORMAT=wav

## Specify the language for voice using ISO 639-1 code (default: auto)
#AIDER_VOICE_LANGUAGE=en

## Specify the input device name for voice recording
#AIDER_VOICE_INPUT_DEVICE=

#################
# Other settings:

## specify a file to edit (can be used multiple times)
#AIDER_FILE=

## specify a read-only file (can be used multiple times)
#AIDER_READ=

## Use VI editing mode in the terminal (default: False)
#AIDER_VIM=false

## Specify the language to use in the chat (default: None, uses system settings)
#AIDER_CHAT_LANGUAGE=

## Always say yes to every confirmation
#AIDER_YES_ALWAYS=

## Enable verbose output
#AIDER_VERBOSE=false

## Load and execute /commands from a file on launch
#AIDER_LOAD=

## Specify the encoding for input and output (default: utf-8)
#AIDER_ENCODING=utf-8

## Specify the .env file to load (default: .env in git root)
#AIDER_ENV_FILE=.env

## Enable/disable suggesting shell commands (default: True)
#AIDER_SUGGEST_SHELL_COMMANDS=true

## Enable/disable fancy input with history and completion (default: True)
#AIDER_FANCY_INPUT=true

## Enable/disable multi-line input mode with Meta-Enter to submit (default: False)
#AIDER_MULTILINE=false

## Enable/disable detection and offering to add URLs to chat (default: True)
#AIDER_DETECT_URLS=true

## Specify which editor to use for the /editor command
#AIDER_EDITOR=
```
<!--[[[end]]]-->