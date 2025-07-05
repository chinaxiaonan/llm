from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import logging
import os

# 加载 .env 文件中定义的环境变量
_ = load_dotenv(find_dotenv())

# 初始化 OpenAI 客户端
llm_client = OpenAI(
    api_key=os.getenv("OPENAI_APIBASE"),
    base_url=os.getenv("OPENAI_API_KEY")
) # 默认使用环境变量中的 OPENAI_API_KEY 和 OPENAI_BASE_URL

# 配置基本的日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_openai_connection():
    try:
        # 尝试最简单的API调用
        response = llm_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print("连接成功!")
        return True
    except Exception as e:
        print(f"连接失败: {e}")
        return False

def get_completion(prompt, model="gpt-4o"):
    """
    使用OpenAI API获取对提示的回复
    Args:
        prompt (str): 用户输入提示
        response_format (str): 返回格式，'text'或'json_object'
        model (str): 要使用的OpenAI模型

    Returns:
        str: 模型生成的回复内容
    """
    try:
        messages = [{"role": "user", "content": prompt}]
        response = llm_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"调用OpenAI API时出错: {e}")
        raise

# 先运行测试
# if test_openai_connection():
#     # 继续主要功能
#     pass
# else:
#     print("请检查网络连接和API密钥设置")