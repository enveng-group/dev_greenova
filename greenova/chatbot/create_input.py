#!/usr/bin/env python3
# This file creates inputs for the chatbot to respond with.
# Please run this command at most once, to avoid duplicate data.

import os
from typing import Any

# Import ChatBotPrompts from the generated protobuf module
from . import chatdata_pb2


def create_response(prompt_list_obj: Any,
                    response_id: int,
                    prompt_text: str,
                    response_text: str) -> Any:
    """Create a response in the prompt list object.

    Args:
        prompt_list_obj: The ChatBotPrompts object to add responses to
        response_id: Unique ID for the response
        prompt_text: The user prompt text
        response_text: The chatbot response text

    Returns:
        The created response object
    """
    response = prompt_list_obj.responses.add()
    response.id = response_id
    response.prompt = prompt_text
    response.response = response_text
    return response


def list_prompts(prompt_list_obj: Any) -> None:
    """List all prompts in the ChatBotPrompts object.

    Args:
        prompt_list_obj: The ChatBotPrompts object containing responses
    """
    for response in prompt_list_obj.responses:
        print('Response ID:      ', response.id)
        print('Response Prompt:  ', response.prompt)
        print('Response Response:', response.response)


def main() -> None:
    """Main function to create and serialize chatbot responses."""
    # Create a new tutorial.ChatBotPrompts object
    prompt_list_obj = chatdata_pb2.ChatBotPrompts()

    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Set output file path
    prompt_list_fname = os.path.join(data_dir, 'chatdata-serialised.protobin')

    # Delete existing file if it exists, we are starting new
    if os.path.exists(prompt_list_fname):
        os.remove(prompt_list_fname)
    else:
        # Create an empty file
        with open(prompt_list_fname, 'w', encoding='utf-8') as f:
            pass

    # Write all our information...
    create_response(
        prompt_list_obj,
        1,
        'Hello',
        "Hello, I am Greenova's chatbot! How can I help you today?"
    )

    # Add more predefined responses
    create_response(
        prompt_list_obj,
        2,
        'What is environmental compliance?',
        'Environmental compliance refers to conforming to environmental laws, '
        'regulations, standards and other requirements related to the environment.'
    )

    create_response(
        prompt_list_obj,
        3,
        'How do I track obligations?',
        'You can track obligations in Greenova by navigating to the Obligations '
        'section and creating a new obligation with the + button. You can then '
        'assign responsibilities and link it to relevant projects.'
    )

    # Display all prompts for verification
    list_prompts(prompt_list_obj)

    # Write the new prompts to disk
    with open(prompt_list_fname, 'wb') as f:
        f.write(prompt_list_obj.SerializeToString())

    print(
        f'Successfully wrote {len(prompt_list_obj.responses)} responses '
        f'to {prompt_list_fname}'
    )


if __name__ == '__main__':
    main()
