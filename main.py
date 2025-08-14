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
import datetime
import time
client = OpenAI(api_key=" ", base_url="https://api.deepseek.com")

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
def check_time():
    """检查当前时间是否在北京时间 00:30 至 08:30 之间"""
    # 获取当前 UTC 时间
    utc_now = datetime.datetime.utcnow()

    # 转换为北京时间（UTC+8）
    beijing_now = utc_now + datetime.timedelta(hours=8)

    # 构造时间范围
    start_time = beijing_now.replace(hour=0, minute=30, second=0, microsecond=0)
    end_time = beijing_now.replace(hour=8, minute=30, second=0, microsecond=0)

    # 检查是否在允许的时间段
    if start_time <= beijing_now <= end_time:
        return True
    else:
        return False

system_prompt = """

"""
chat_prompt = """

"""
start_prompt = """

"""

def main():
    existing_chapters = load_existing_novel("novel_output.txt")
    chapter_count = len(existing_chapters)
    cnt = 12
    tempcnt = cnt
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": start_prompt})
    if chapter_count > 0:
        for ch in existing_chapters[-cnt:]:
            if tempcnt == 0:
                break
            else:
                messages.append({"role": "assistant", "content": ch})
                messages.append({"role": "user", "content": chat_prompt})
                tempcnt -= 1
    while 1:
        if not check_time():
            time.sleep(5)
            continue
        try:
            response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=messages,
                stream=False,
                max_tokens = 64000,
                temperature= 1.5
            )
            if response.choices[0].finish_reason == "stop":
                novel_content = response.choices[0].message.content
                write_to_file(novel_content)
                messages.append({"role": "assistant", "content": novel_content})
                messages.append({"role": "user", "content": chat_prompt})
                chapter_count += 1
                print(f"当前进度: {chapter_count}")
                if chapter_count > cnt:
                    messages.pop(2)
                    messages.pop(2)
        except Exception as e:
            print(f"异常重试: {str(e)}")
            time.sleep(1)




if __name__ == "__main__":
    main()