# Doug

Doug is a CLI interface to OpenAI ChatGPT. It uses langchain to interact with ChatGPT, and implements the ConversationChain and both ConversationBufferMemory and ConversationSummaryMemory with CombinedMemory.

## Installation

To install Doug, simply clone the repository and install the necessary dependencies:

```
git clone https://github.com/houseofbaud/doug.git
cd doug
pip install -r requirements.txt
```

## Environment and API Keys

Setup your `.env` file in the root of the repository. Mandatory variables are:

```
OPENAI_API_KEY=<you api key>
OPENAI_LLM_MODEL=<llm-model>
```

You can obtain potential values for `OPENAI_LLM_MODEL` by running:
`python util/get-openai-models.py`

This will output a raw list returned from the OpenAI API of models you can base
Doug off of. Make sure you've already set your API Key in `.env` to use the utility
script.

By default, `gpt-3.5-turbo-0301` is used.

## Usage

To start using Doug, simply run the following command after setting your environment:

```
python main.py
```

Doug will then prompt you for input, and you can start chatting with ChatGPT!

## Features

Doug has the following features:

- Uses langchain for seamless integration with ChatGPT
- Implements ConversationChain for more natural conversations
- Uses CombinedMemory with ConversationBufferMemory and ConversationSummaryMemory for a more natural experience
- Swapable prompts! Customize Doug in any way you see fit. Check out `data/prompt` and add your own!

## Example Directory
Included is an `examples/` directory with example output from Doug. This output is unmodified outside of being snipped down to just the code blocks being output by Doug. More examples will be added as time goes on.

## Contributing

If you'd like to contribute to Doug, simply fork the repository and submit a pull request with your changes.

## License

Doug is licensed under the MIT license. See LICENSE for more details.
