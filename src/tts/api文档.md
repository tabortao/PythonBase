API documentation
http://localhost:7860/

API Recorder

4 API endpoints


Choose a language to see the code snippets for interacting with the API.

1. Install the python client (docs) if you don't already have it installed.

copy
$ pip install gradio_client
2. Find the API endpoint below corresponding to your desired function in the app. Copy the code snippet, replacing the placeholder values with your own input data. Or use the 
API Recorder

 to automatically generate your API requests.

api_name: /change_choices
copy
from gradio_client import Client

client = Client("http://localhost:7860/")
result = client.predict(
		api_name="/change_choices"
)
print(result)
Accepts 0 parameters:
Returns 1 element
Literal['使用参考音频', 'jok老师.pt', 'Lei.pt', '叶奈法.pt', '步非烟.pt']

The output value that appears in the "音色列表" Dropdown component.

api_name: /update_prompt_audio
copy
from gradio_client import Client

client = Client("http://localhost:7860/")
result = client.predict(
		api_name="/update_prompt_audio"
)
print(result)
Accepts 0 parameters:
Returns 1 element
api_name: /save_audio
copy
from gradio_client import Client

client = Client("http://localhost:7860/")
result = client.predict(
		name="Hello!!",
		api_name="/save_audio"
)
print(result)
Accepts 1 parameter:
name str Required

The input value that is provided in the "音色名称" Textbox component.

Returns 1 element
api_name: /infer
copy
from gradio_client import Client, handle_file

client = Client("http://localhost:7860/")
result = client.predict(
		name="使用参考音频",
		voice=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		text="Hello!!",
		speed=1,
		api_name="/infer"
)
print(result)
Accepts 4 parameters:
name Literal['使用参考音频', 'jok老师.pt', 'Lei.pt', '叶奈法.pt', '步非烟.pt'] Default: "使用参考音频"

The input value that is provided in the "音色列表" Dropdown component.

voice filepath Required

The input value that is provided in the "请上传参考音频" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

text str Required

The input value that is provided in the "请输入目标文本" Textbox component.

speed float Default: 1

The input value that is provided in the "语速" Slider component.

Returns 1 element
filepath

The output value that appears in the "生成结果" Audio component.