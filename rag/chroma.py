import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import ssl
from util.llm_util import llm_client, get_completion

ssl._create_default_https_context = ssl._create_unverified_context
# 创建持久化客户端，数据将保存在 "chromadb/" 目录中
client = chromadb.PersistentClient(path="C:/chromadb/")

# 将文本数据添加到集合中，ChromaDB 会自动将文本转换为向量嵌入并存储
student_info = """
Alexandra Thompson, a 19-year-old computer science sophomore with a 3.7 GPA,
is a member of the programming and chess clubs who enjoys pizza, swimming, and hiking
in her free time in hopes of working at a tech company after graduating from the University of Washington.
"""

club_info = """
The university chess club provides an outlet for students to come together and enjoy playing
the classic strategy game of chess. Members of all skill levels are welcome, from beginners learning
the rules to experienced tournament players. The club typically meets a few times per week to play casual games,
participate in tournaments, analyze famous chess matches, and improve members' skills.
"""

university_info = """
The University of Washington, founded in 1861 in Seattle, is a public research university
with over 45,000 students across three campuses in Seattle, Tacoma, and Bothell.
As the flagship institution of the six public universities in Washington state,
UW encompasses over 500 buildings and 20 million square feet of space,
including one of the largest library systems in the world.
"""

# 使用默认的embedding模型 -- begin
# 创建集合，集合类似于数据库中的表，用于存储相关的向量数据
collection = client.get_or_create_collection(name="Students")
# 使用默认的embedding模型 -- end

# 不使用默认的embedding模型创建集合，需要配置环境变量中的key和url
# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#     # model_name="text-embedding-ada-002"
#     model_name="text-embedding-async-v1"
# )
# # 使用text-embedding-ada-002
# students_embeddings = openai_ef([student_info, club_info, university_info])
#
# collection = client.create_collection(
#     name="Students",
#     embedding_function=openai_ef
# )

# 添加数据到集合，使用默认的all-MiniLM-L6-v2
collection.add(
    #下面三个参数的赋值是一一对应关系
    documents=[student_info, club_info, university_info],#存储在向量数据库中的实际文本内容的列表
    #包含与每个文档相关联的额外信息（元数据）。每个元数据是一个字典，可以包含任何你想要的键值对
    metadatas=[{"source": "student info", "date_added": "2023-06-01"},
               {"source": "club info"},
               {"source": "university info"}],
    ids=["id1", "id2", "id3"]#每个文档提供唯一标识符
)

# 查询结果
results = collection.query(
    query_texts=["What is the student name?"],
    n_results=2
)
print("完整查询结果:")
print(results)
#将结果给大模型，给出回答
# 获取包含学生信息的文档
student_doc = results['documents'][0][0]

prompt = "从以下文本中提取学生姓名，只返回姓名:\n" + student_doc
response = get_completion(prompt)

print("学生姓名:", response)

# 更新数据
# collection.update(
#     ids=["id1"],
#     documents=["Kristiane Carina, a 19-year-old computer science sophomore with a 3.7 GPA"],
#     metadatas=[{"source": "student info"}]
# )
#
# # 删除数据
# collection.delete(ids=["id1"])
# # 查询以验证删除
# results = collection.query(
#     query_texts=["What is the student name?"],
#     n_results=2
# )
#
# print(results)
#
# # 获取集合列表
# collections = client.list_collections()
# print(collections)
#
# # 获取集合中的数据
# collection = client.get_collection(name="Students")
# data = collection.peek()  # 获取集合中的前10条数据
# print(data)
#
# # 条件查询
# results = collection.query(
#     query_texts=["What is the student name?"],
#     n_results=2,
#     where={"source": "student info"},
#     where_document={"$contains": "computer science"}
# )
# print(results)
#
# # 删除集合
# client.delete_collection(name="Students")








