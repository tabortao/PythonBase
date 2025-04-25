## index-tts
> IndexTTS是一个基于 GPT 风格的文本转语音 (TTS) 模型，主要基于 XTTS 和 Tortoise 算法。它能够通过拼音纠正汉字发音，并通过标点符号控制任意位置的停顿。我们增强了系统的多个模块，包括改进说话人条件特征表示，并集成 BigVGAN2 以优化音频质量。我们的系统基于数万小时的数据进行训练，达到了最佳性能，超越了目前流行的 TTS 系统，例如 XTTS、CosyVoice2、Fish-Speech 和 F5-TTS。

项目地址：https://github.com/index-tts/index-tts
## 脚本介绍
通过Gradio API 调用 index-tts，克隆自己声音，生成中文语音。
- 每页生成一个音频，命名为《书名》_page_1.wav。
- 最终合并为一个音频《书名》.wav。


