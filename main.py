import os
from openai import OpenAI

client = OpenAI(api_key="这里填入您自己的API！", base_url="https://api.deepseek.com")
system_prompt = """
你是一个专业的顶级的拥有几百年经验的著名网络小说作家，用户需要你创作完美的网络小说，你需要保持以下创作规范：每章必须有明确的章节标题（格式：第X章 标题）。你可以完全自由发挥。
"""
def load_existing_novel(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            chapters = content.split("=" * 40)[1::2]
            return [ch.strip() for ch in chapters if ch.strip()]
    return []
def main():
    existing_chapters = load_existing_novel("novel_output.txt")
    chapter_count = len(existing_chapters)
    max_chapters = 10
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": "请开始创作小说的第一章。"})
    if chapter_count > 0:
        for ch in existing_chapters:
            messages.append({"role": "assistant", "content": ch})
            messages.append({"role": "user", "content": "请继续创作下一章，保持故事连贯性，注意章节标题格式，正文字数必须尽可能多。"})
    def write_to_file(content, filename="novel_output.txt"):
        with open(filename, "a", encoding="utf-8") as f:
            f.write("\n\n" + "=" * 40 + "\n")
            f.write(content + "\n")
            f.write("=" * 40 + "\n\n")
    while chapter_count < max_chapters:
        try:
            response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=messages,
                stream=False,
                max_tokens = 8000
            )
            if response.choices[0].finish_reason == "stop":
                novel_content = response.choices[0].message.content
                write_to_file(novel_content)
                messages.append({"role": "assistant", "content": novel_content})
                messages.append({"role": "user", "content": "请继续创作下一章，保持故事连贯性，注意章节标题格式，正文字数必须尽可能多。"})
                chapter_count += 1
                print(f"当前进度: {chapter_count}/{max_chapters}")
        except Exception as e:
            print(f"异常重试: {str(e)}")
    print("一轮over")
while 1:
    main()