
### llm_openai
写一个调用oepnai及其openai兼容模型的python脚本，实现如下功能：
- 调用OpenAI Python SDK，实现调用openai 其兼容模型
- 输入参数包含：base_url、api_key、prompt、model
- 实现基础流式输出
- 实现同步流式输出
- 需要有错误捕捉和提示
- 需要有注释
- 输入参数从config.toml读取

### llm_gemini

> Gemini 模型需要使用新加坡或美国的代理才能访问。

写一个调用google gemini模型的python脚本，参考[docs\Gemini OpenAI 兼容性设置.md]实现如下功能：
- 调用OpenAI Python SDK，实现调用gemini,完成文本流式响应、多模态输入（文本+图片）、生成图片、音频理解
- 输入参数包含：base_url、api_key、prompt、model
- 实现基础流式输出
- 实现同步流式输出
- 需要有错误捕捉和提示
- 需要有注释
- 输入参数从config.toml读取

- 模型名称可以从官网获取：https://ai.google.dev/gemini-api/docs/models?hl=zh-cn


## openrouter
- base_url = https://openrouter.ai/api/v1
- 模型名称可以从官网搜索（free）获取：https://openrouter.ai/models
- models = ["deepseek/deepseek-chat-v3-0324:free", "qwen/qwq-32b:free"]



[google]
api_key = "google-xxx"
models = ["gemini-pro", "gemini-ultra"]
default_model = "gemini-pro"
temperature = 0.3