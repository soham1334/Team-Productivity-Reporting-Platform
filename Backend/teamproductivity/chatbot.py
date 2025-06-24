import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_uri = os.getenv("DATABASE_URL")

llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama3-8b-8192")

db = SQLDatabase.from_uri(DB_uri,
                              include_tables=["teamproductivity_issue", "teamproductivity_sprint", "teamproductivity_teams"])

custom_prompt = PromptTemplate(
input_variables=["input"],
template = """
You are an expert in translating natural language questions into SQL queries for a PostgreSQL database.

- teamproductivity_sprint (alias: s)
- teamproductivity_issue (alias: i)
- teamproductivity_teams (alias: t)

Always use **table aliases** (e.g. s.id, i.sprint_id) to avoid ambiguity.
Only output the SQL Result  directly, nothing else.
 Do NOT return SQL syntax or formatting like ```sql or code blocks.



Use the following user question:
{input}
"""

              )

db_chain = SQLDatabaseChain.from_llm(llm,db,custom_prompt, return_intermediate_steps=True,verbose = True)

     

    
    

def query_db_view(query):
    query_res = db_chain.invoke({"query": query})
    # if isinstance(query_res, list) and len(query_res) > 0 and isinstance(query_res[0], tuple):
    #     query_res_text = ", ".join(str(item) for item in query_res[0])
    # else:
    #     query_res_text = str(query_res)
    print("---------------------------------------------")
    print("QUERY_RES:",query_res)
    print("---------------------------------------------")
    result = llm.invoke( f"User asked: '{query}'. SQL result: {query_res['result']}. "
                        "parse the SQL resut before using"
                        "Answer the question using this raw sql result in a human-readable sentence."
                         "Just give clean answers like names or numbers."
                         "Don’t add anything extra, just directly answer."
                         )
    return result.content
    print("output",result)