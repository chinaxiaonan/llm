from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import json


_ = load_dotenv(find_dotenv())
client = OpenAI()

def print_json(data):
    """
    打印参数。如果参数是有结构的（如字典或列表），则以格式化的 JSON 形式打印；
    否则，直接打印该值。
    """
    if hasattr(data, 'model_dump_json'):
        data = json.loads(data.model_dump_json())

    if (isinstance(data, (list))):
        for item in data:
            print_json(item)
    elif (isinstance(data, (dict))):
        print(json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ))
    else:
        print(data)

# 调用本地函数例子，用tools
def get_completion(messages, model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        tools=[{  # 用 JSON 描述函数。可以定义多个。由大模型决定调用谁。也可能都不调用
            "type": "function",
            "function": {
                "name": "sum",
                "description": "加法器，计算一组数的和",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {
                                "type": "number"
                            }
                        }
                    }
                }
            }
        }],
    )
    return response.choices[0].message

# prompt = "Tell me the sum of 1, 2, 3, 4, 5, 6, 7, 8, 9, 10."
# prompt = "桌上有 2 个苹果，四个桃子和 3 本书，还有 3 个番茄，以及三个傻瓜，一共有几个水果？"
# #prompt = "1+2+3...+99+100"
# #prompt = "1024 乘以 1024 是多少？"   # Tools 里没有定义乘法，会怎样？
# #prompt = "太阳从哪边升起？"            不需要算加法，会怎样？
#
# messages = [
#     {"role": "system", "content": "你是一个数学家"},
#     {"role": "user", "content": prompt}
# ]
# response = get_completion(messages)
#
# # 把大模型的回复加入到对话历史中。必须有
# messages.append(response)
#
# # 如果返回的是函数调用结果，则打印出来
# if (response.tool_calls is not None):
#     # 是否要调用 sum
#     tool_call = response.tool_calls[0]
#     if (tool_call.function.name == "sum"):
#         # 调用 sum
#         args = json.loads(tool_call.function.arguments)
#         result = sum(args["numbers"])
#
#         # 把函数调用结果加入到对话历史中
#         messages.append(
#             {
#                 "tool_call_id": tool_call.id,  # 用于标识函数调用的 ID
#                 "role": "tool",
#                 "name": "sum",
#                 "content": str(result)  # 数值 result 必须转成字符串
#             }
#         )
#
#         # 再次调用大模型
#         response = get_completion(messages)
#         messages.append(response)
#         print("=====最终 GPT 回复=====")
#         print(response.content)
#
# print("=====对话历史=====")
# print_json(messages)

# 多function调用
# def get_completion(messages, model="gpt-4o"):
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=0,
#         seed=1024,      # 随机种子保持不变，temperature 和 prompt 不变的情况下，输出就会不变
#         tool_choice="auto",  # 默认值，由 GPT 自主决定返回 function call 还是返回文字回复。也可以强制要求必须调用指定的函数，详见官方文档
#         tools=[{
#             "type": "function",
#             "function": {
#                 "name": "get_location_coordinate",
#                 "description": "根据POI名称，获得POI的经纬度坐标",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "location": {
#                             "type": "string",
#                             "description": "POI名称，必须是中文",
#                         },
#                         "city": {
#                             "type": "string",
#                             "description": "POI所在的城市名，必须是中文",
#                         }
#                     },
#                     "required": ["location", "city"],
#                 }
#             }
#         },
#             {
#             "type": "function",
#             "function": {
#                 "name": "search_nearby_pois",
#                 "description": "搜索给定坐标附近的poi",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "longitude": {
#                             "type": "string",
#                             "description": "中心点的经度",
#                         },
#                         "latitude": {
#                             "type": "string",
#                             "description": "中心点的纬度",
#                         },
#                         "keyword": {
#                             "type": "string",
#                             "description": "目标poi的关键字",
#                         }
#                     },
#                     "required": ["longitude", "latitude", "keyword"],
#                 }
#             }
#         }],
#     )
#     return response.choices[0].message
#
# import requests
# import os
#
# amap_key = os.getenv("AMAP_KEY")
# amap_base_url = os.getenv("AMAP_URL") # 默认是 https://restapi.amap.com/v5
#
#
# def get_location_coordinate(location, city):
#     url = f"{amap_base_url}/place/text?key={amap_key}&keywords={location}&region={city}"
#     r = requests.get(url)
#     result = r.json()
#     if "pois" in result and result["pois"]:
#         return result["pois"][0]
#     return None
#
#
# def search_nearby_pois(longitude, latitude, keyword):
#     url = f"{amap_base_url}/place/around?key={amap_key}&keywords={keyword}&location={longitude},{latitude}"
#     r = requests.get(url)
#     result = r.json()
#     ans = ""
#     if "pois" in result and result["pois"]:
#         for i in range(min(3, len(result["pois"]))):
#             name = result["pois"][i]["name"]
#             address = result["pois"][i]["address"]
#             distance = result["pois"][i]["distance"]
#             ans += f"{name}\n{address}\n距离：{distance}米\n\n"
#     return ans

# 通过 Function Calling 查询数据库
#  描述数据库表结构
database_schema_string = """
CREATE TABLE orders (
    id INT PRIMARY KEY NOT NULL, -- 主键，不允许为空
    customer_id INT NOT NULL, -- 客户ID，不允许为空
    product_id STR NOT NULL, -- 产品ID，不允许为空
    price DECIMAL(10,2) NOT NULL, -- 价格，不允许为空
    status INT NOT NULL, -- 订单状态，整数类型，不允许为空。0代表待支付，1代表已支付，2代表已退款
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 创建时间，默认为当前时间
    pay_time TIMESTAMP -- 支付时间，可以为空
);
"""
def get_sql_completion(messages, model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        tools=[{  # 摘自 OpenAI 官方示例 https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb
            "type": "function",
            "function": {
                "name": "ask_database",
                "description": "Use this function to answer user questions about business. \
                            Output should be a fully formed SQL query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": f"""
                            SQL query extracting info to answer the user's question.
                            SQL should be written using this database schema:
                            {database_schema_string}
                            The query should be returned in plain text, not in JSON.
                            The query should only contain grammars supported by SQLite.
                            """,
                        }
                    },
                    "required": ["query"],
                }
            }
        }],
    )
    return response.choices[0].message