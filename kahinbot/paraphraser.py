# MIT License

# Copyright (c) 2024 Şeyma Yardım

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This module provides a function for paraphrasing Turkish text using Google Gemini Pro.
"""

import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

__author__ = "Seymapro"
__version__ = "1.0.0"

# Configure the Google Gemini API with the API key from environment variables
genai.configure(api_key=os.environ["GEMINI_API_KEY"])  # type: ignore[reportAttributeAccessIssue, reportUnknownMemberType]

# Define generation configuration for the Gemini model
generation_config: dict[str, int | float | str] = {
    "temperature": 1,  # Controls the randomness of the generated text (higher = more random)
    "top_p": 0.95,  # Controls the diversity of the generated text (higher = more diverse)
    "top_k": 64,  # Limits the vocabulary used in generation (higher = more words)
    "max_output_tokens": 8192,  # Maximum number of tokens in the generated response
    "response_mime_type": "text/plain",  # Response format (plain text)
}

# Initialize the Google Gemini Pro model with specific safety settings
model = genai.GenerativeModel(  # type: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
    # System instruction to guide the model's behavior
    system_instruction="You are a professional paraphraser specialized in Turkish language. Paraphrase the given text to a more natural-sounding and expressive version. Do not use Markdown, use only plain text.",
)


def paraphrase(content: str) -> str:
    """
    Paraphrases the given Turkish text using Google Gemini Pro.

    Args:
        content: The Turkish text to be paraphrased.

    Returns:
        The paraphrased version of the input text.
    """

    # Start a new chat session with the Gemini model
    chat_session = model.start_chat(history=[])  # type: ignore[reportUnknownMemberType, reportUnknownVariableType]

    # Send the input text to the model and get the response
    response = chat_session.send_message(content)  # type: ignore[reportUnknownMemberType, reportUnknownVariableType]

    # Return the paraphrased text from the model's response
    return response.text  # type: ignore[reportUnknownMemberType, reportUnknownVariableType]
