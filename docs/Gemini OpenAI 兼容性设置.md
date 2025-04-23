OpenAI 兼容性

您可以使用 OpenAI 库（Python 和 TypeScript/JavaScript）以及 REST API 访问 Gemini 模型，只需更新三行代码并使用 Gemini API 密钥即可。如果您尚未使用 OpenAI 库，我们建议您直接调用 Gemini API。

Python
JavaScript
REST

from openai import OpenAI

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.0-flash",
    n=1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
)

print(response.choices[0].message)
具体变化只需三行代码！

api_key="GEMINI_API_KEY"：只需将“GEMINI_API_KEY”替换为您的实际 Gemini API 密钥即可，您可以在 Google AI Studio 中获取该密钥。

base_url="https://generativelanguage.googleapis.com/v1beta/openai/"：这会指示 OpenAI 库向 Gemini API 端点发送请求，而不是向标准 OpenAI 端点发送请求。

model="gemini-2.0-flash"：我们将指定功能强大且高效的 gemini-2.0-flash 模型。

列出模型
获取可用 Gemini 模型的列表：

Python
JavaScript
REST

from openai import OpenAI

client = OpenAI(
  api_key="GEMINI_API_KEY",
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

models = client.models.list()
for model in models:
  print(model.id)
检索模型
检索 Gemini 模型：

Python
JavaScript
REST

from openai import OpenAI

client = OpenAI(
  api_key="GEMINI_API_KEY",
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = client.models.retrieve("gemini-2.0-flash")
print(model.id)
流式
Gemini API 支持流式响应。

Python
JavaScript
REST

from openai import OpenAI

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
  model="gemini-2.0-flash",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  stream=True
)

for chunk in response:
    print(chunk.choices[0].delta)
函数调用
借助函数调用，您可以更轻松地从生成式模型获取结构化数据输出，并且Gemini API 支持函数调用。

Python
JavaScript
REST

from openai import OpenAI

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

tools = [
  {
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get the weather in a given location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state, e.g. Chicago, IL",
          },
          "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
      },
    }
  }
]

messages = [{"role": "user", "content": "What's the weather like in Chicago today?"}]
response = client.chat.completions.create(
  model="gemini-2.0-flash",
  messages=messages,
  tools=tools,
  tool_choice="auto"
)

print(response)
图片理解
Gemini 模型是原生多模态模型，在许多常见的视觉任务中都能提供出色的性能。

Python
JavaScript
REST

import base64
from openai import OpenAI

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Getting the base64 string
base64_image = encode_image("Path/to/agi/image.jpeg")

response = client.chat.completions.create(
  model="gemini-2.0-flash",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is in this image?",
        },
        {
          "type": "image_url",
          "image_url": {
            "url":  f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
)

print(response.choices[0])
生成图片
注意： 图片生成功能仅适用于付费层级。
生成图片：

Python
JavaScript
REST

import base64
from openai import OpenAI
from PIL import Image
from io import BytesIO

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

response = client.images.generate(
    model="imagen-3.0-generate-002",
    prompt="a portrait of a sheepadoodle wearing a cape",
    response_format='b64_json',
    n=1,
)

for image_data in response.data:
  image = Image.open(BytesIO(base64.b64decode(image_data.b64_json)))
  image.show()
音频理解
分析音频输入：

Python
JavaScript
REST

import base64
from openai import OpenAI

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

with open("/path/to/your/audio/file.wav", "rb") as audio_file:
  base64_audio = base64.b64encode(audio_file.read()).decode('utf-8')

response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Transcribe this audio",
        },
        {
              "type": "input_audio",
              "input_audio": {
                "data": base64_audio,
                "format": "wav"
          }
        }
      ],
    }
  ],
)

print(response.choices[0].message.content)
结构化输出
Gemini 模型可以以您定义的任何结构输出 JSON 对象。

Python
JavaScript

from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

completion = client.beta.chat.completions.parse(
    model="gemini-2.0-flash",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "John and Susan are going to an AI conference on Friday."},
    ],
    response_format=CalendarEvent,
)

print(completion.choices[0].message.parsed)
Embeddings
文本嵌入可衡量文本字符串的相关性，并且可以使用 Gemini API 生成。

Python
JavaScript
REST

from openai import OpenAI

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.embeddings.create(
    input="Your text string goes here",
    model="text-embedding-004"
)

print(response.data[0].embedding)
当前限制
我们正在扩大功能支持范围，因此对 OpenAI 库的支持仍处于 Beta 版阶段。

如果您对支持的参数、即将推出的功能有任何疑问，或者在开始使用 Gemini 时遇到任何问题，请加入我们的开发者论坛。