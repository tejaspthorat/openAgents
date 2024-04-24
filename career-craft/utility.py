import json
import re
from openai import OpenAI
import os

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

client = OpenAI(
  api_key=TOGETHER_API_KEY,
  base_url='https://api.together.xyz/v1',
)

def askLLM(prompt):
    completion = client.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    messages=[
      {
        "role": "user",
        "content": prompt,
      }
    ],
    n=1,
    max_tokens=4000,
    temperature=0.1,
    top_p=0.9,
   )
    return completion.choices[0].message.content

def separate_text_and_json(input_string):
    """
    Returns an output by separating json from string
    """
    text_pattern = r'.*?(?={"|\[)'
    json_pattern = r'({.*})'

    # Find text using the text pattern
    text_match = re.match(text_pattern, input_string, re.DOTALL)

    # Extract JSON using the JSON pattern
    json_match = re.search(json_pattern, input_string)

    if text_match and json_match:
        text = text_match.group(0)
        json_data = json.loads(json_match.group(1))
        return text, json_data
    else:
        return None, None
    
def RawJSONDecoder(index):
    class _RawJSONDecoder(json.JSONDecoder):
        end = None

        def decode(self, s, *_):
            data, self.__class__.end = self.raw_decode(s, index)
            return data
    return _RawJSONDecoder

def extract_json(s, index=0):
    while (index := s.find('{', index)) != -1:
        try:
            yield json.loads(s, cls=(decoder := RawJSONDecoder(index)))
            index = decoder.end
        except json.JSONDecodeError:
            index += 1

def add_non_empty_details(current_details, new_details):
        non_empty_details = {k: v for k, v in new_details.dict().items() if v not in [None, ""]}
        updated_details = current_details.copy(update=non_empty_details)
        return updated_details

def check_what_is_empty(user_peronal_details):
    ask_for = []
    for field, value in user_peronal_details.dict().items():
        if value in [None, "", 0]:
            ask_for.append(f'{field}')
    return ask_for