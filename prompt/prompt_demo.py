"""
调用openai的demo，包括prompt写在代码中和文件中两种方式；还报错单次对话和多轮对话
"""
# 导入依赖库
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# 加载 .env 文件中定义的环境变量
_ = load_dotenv(find_dotenv())

# 初始化 OpenAI 客户端
client = OpenAI() # 默认使用环境变量中的 OPENAI_API_KEY 和 OPENAI_BASE_URL

# 获取openai结果的方法
def get_completion(prompt, response_format="text", model="gpt-4o-mini"):
    messages = [{"role": "user", "content": prompt}]    # 将 prompt 作为用户输入
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,                                  # 模型输出的随机性，0 表示随机性最小
        # 返回消息的格式，text 或 json_object
        response_format={"type": response_format},
    )
    return response.choices[0].message.content # 返回模型生成的文本

# 1. 在代码中构建prompt--begin
# 构建prompt，包括角色定义，任务描述，例子，定义输出格式,用户输入
# 任务描述
instruction = """
你的任务是识别用户对手机流量套餐产品的选择条件。
每种流量套餐产品包含三个属性：名称，月费价格，月流量。
根据用户输入，识别用户在上述三种属性上的需求是什么。
"""

# 用户输入
input_text = """
办个100G的套餐。
"""
# 输出格式增加了各种定义、约束
output_format = """
以JSON格式输出。
1. name字段的取值为string类型，取值必须为以下之一：经济套餐、畅游套餐、无限套餐、校园套餐 或 null；

2. price字段的取值为一个结构体 或 null，包含两个字段：
(1) operator, string类型，取值范围：'<='（小于等于）, '>=' (大于等于), '=='（等于）
(2) value, int类型

3. data字段的取值为取值为一个结构体 或 null，包含两个字段：
(1) operator, string类型，取值范围：'<='（小于等于）, '>=' (大于等于), '=='（等于）
(2) value, int类型或string类型，string类型只能是'无上限'

4. 用户的意图可以包含按price或data排序，以sort字段标识，取值为一个结构体：
(1) 结构体中以"ordering"="descend"表示按降序排序，以"value"字段存储待排序的字段
(2) 结构体中以"ordering"="ascend"表示按升序排序，以"value"字段存储待排序的字段

输出中只包含用户提及的字段，不要猜测任何用户未直接提及的字段，不输出值为null的字段。
"""
# 1. 在代码中构建prompt
# prompt 模版。instruction 和 input_text 会被替换为上面的内容
# prompt = f"""
# # 目标
# {instruction}
#
# # 输出格式
# {output_format}
#
# # 用户输入
# {input_text}
# """


# 2. 从文件中读取模板构建prompt 在demo_simple.txt中定义了prompt的简单格式，包括目标，输出格式，用户输入
with open('../prompt_templates/simple_demo.txt', 'r', encoding='utf-8') as file:
    prompt_template = file.read()
prompt = prompt_template.replace("{instruction}", instruction).replace("{input_text}", input_text)  # 使用.replace()方法，适用于简单替换

print("==== Prompt ====")
print(prompt)
print("================")

# 调用大模型，指定用 JSON mode 输出
response = get_completion(prompt)
print(response)