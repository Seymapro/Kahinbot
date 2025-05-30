# MIT License
#
# Copyright (c) 2024 Şeyma Yardım
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Turkish Text Paraphrasing Module

This module provides functionality for paraphrasing Turkish text using Google's Gemini AI model.
It transforms input text into more natural-sounding and expressive Turkish while preserving
the original meaning.

The module uses the Google Generative AI (Gemini) API with custom content generation settings
and safety parameters optimized for Turkish language processing.

Example:
    >>> from kahinbot.paraphraser import paraphrase
    >>> text = "Merhaba dünya"
    >>> paraphrase(text)
    'Selam, dünya!'

Note:
    All safety thresholds are set to BLOCK_NONE to ensure unrestricted language processing
    capability, which is necessary for accurate Turkish paraphrasing.
"""

import os
from google import genai
from google.genai import types

__author__ = "Seymapro"
__version__ = "1.1.0"

# Initialize Gemini API client using environment variable
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Configure content generation settings with custom instructions and safety parameters
content_config = types.GenerateContentConfig(
    # Define system role and output requirements
    system_instruction="You are a professional paraphraser specialized in Turkish language. Paraphrase the given text to a more natural-sounding and expressive version. Do not use Markdown, use only plain text.",
    response_mime_type="text/plain",
    # Set safety thresholds to allow all content categories
    # This is required for unrestricted language processing
    safety_settings=[
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY, threshold=types.HarmBlockThreshold.BLOCK_NONE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_NONE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_NONE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_NONE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_NONE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_UNSPECIFIED, threshold=types.HarmBlockThreshold.BLOCK_NONE
        ),
    ],
)


def paraphrase(content: str) -> str:
    """Paraphrases the given Turkish text using Google's Gemini AI model.

    This function takes a Turkish text input and uses the Gemini AI model to generate
    a more natural-sounding and expressive version while maintaining the original meaning.
    The paraphrasing is performed with specific safety settings that allow unrestricted
    language processing.

    Args:
        content (str): The input text to be paraphrased. Should be in Turkish language.

    Returns:
        str: The paraphrased version of the input text, with leading and trailing
            whitespace removed.

    Raises:
        ValueError: If the model's response cannot be converted to a string.
        RuntimeError: If the API call fails or if there are connectivity issues.

    Examples:
        >>> text = "Merhaba dünya"
        >>> paraphrase(text)
        'Selam, dünya!'
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=content,
        config=content_config,
    )

    if isinstance(paraphrased := response.text, str):
        return paraphrased.strip()

    raise ValueError("Paraphrased content is not a string.")
