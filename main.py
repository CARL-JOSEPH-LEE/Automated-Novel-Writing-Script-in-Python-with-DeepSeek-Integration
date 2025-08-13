"""
作者在这里想说几句话,作为作者我有权在这里发电.
大家好啊,我是李忠恕,蚂蚁花名中恕,英文名CARL JOSEPH LEE,网名还有DJCARL,DJ卡尔这些^^
我的个人网站是8sora8.com,欢迎和我交朋友.
这个代码很水,就是个滑动窗口,加上一点提示词控制.
我是提示词高手,但是为了省TOKEN,这里就不放大型提示词了.
我的提示词在蚂蚁和阿里内网开源了,感兴趣自己去看吧.
那是一段狂热的经历,用佛教的话来说就是着文字相.然后莫名其妙就在tensortrust.ai成为第四名了,然后莫名其妙就写了几百个提示词工程了.
人生如梦,一樽还酹江月
AI真的强大,我喜欢AI,我知道AI未来会更厉害,AI这个工具迟早能够自我迭代.
希望我的这些能给AI发展助力0.0000000001%
喜欢我的话就直接加我QQ微信吧,在我的个人网站里有.欢迎去我的个人网站听歌呦.
"""
import os
from openai import OpenAI

client = OpenAI(api_key="填你的API", base_url="https://api.deepseek.com")


system_prompt = """
你是一个专业的顶级的拥有几百年经验的著名网络小说作家，用户需要你创作完美的网络小说，你需要保持以下创作规范：每章必须有明确的章节标题（格式：第X章 标题）。你可以完全自由发挥。你只需要创作小说的正文，正文字数必须尽可能多，禁止输出任何和小说无关的东西。
# 内容禁令
× 禁止任何非小说内容（询问/注释/总结/解释等）
× 禁止假大空、模糊不清、模棱两可的描述（禁止出现“某种”）
× 禁止中断的故事线（每章需完整呈现场景）
× 禁止使用大纲式写法（必须完整展开细节）
"""
def load_existing_novel(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            chapters = content.split("=" * 40)[1::2]
            return [ch.strip() for ch in chapters if ch.strip()]
    return []
def write_to_file(content, filename="novel_output.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write("\n\n" + "=" * 40 + "\n")
        f.write(content + "\n")
        f.write("=" * 40 + "\n\n")
def main():
    existing_chapters = load_existing_novel("novel_output.txt")
    chapter_count = len(existing_chapters)
    cnt = 20
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": "请开始创作小说的第一章。正文字数必须尽可能多。你可以完全自由发挥。你只需要创作小说的正文，禁止输出任何和小说无关的东西。你必须遵守内容禁令。"})
    if chapter_count > 0:
        for ch in existing_chapters[::-1]:
            if cnt == 0:
                break
            else:
                messages.append({"role": "assistant", "content": ch})
                messages.append({"role": "user", "content": "很好，请继续自由创作下一章，保持故事连贯性，注意章节标题格式，正文字数必须尽可能多。你可以完全自由发挥。你只需要创作小说的正文，禁止输出任何和小说无关的东西。你必须遵守内容禁令。"})
                cnt -= 1
    while 1:
        try:
            response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=messages,
                stream=False,
                max_tokens = 64000
            )
            if response.choices[0].finish_reason == "stop":
                novel_content = response.choices[0].message.content
                write_to_file(novel_content)
                messages.append({"role": "assistant", "content": novel_content})
                messages.append({"role": "user", "content": "很好，请继续自由创作下一章，保持故事连贯性，注意章节标题格式，正文字数必须尽可能多。你可以完全自由发挥。你只需要创作小说的正文，禁止输出任何和小说无关的东西。你必须遵守内容禁令。"})
                chapter_count += 1
                print(f"当前进度: {chapter_count}")
                if cnt == 0:
                    messages.pop(2)
                    messages.pop(2)
        except Exception as e:
            print(f"异常重试: {str(e)}")

if __name__ == "__main__":
    main()