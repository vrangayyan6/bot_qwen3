from langchain_community.tools import DuckDuckGoSearchRun
import concurrent.futures
import time

def do_search(q):
    print(f"Starting search for {q}")
    tool = DuckDuckGoSearchRun()
    res = tool.invoke(q)
    print(f"Finished search for {q}, len: {len(res)}")

queries = ["query 1", "query 2", "query 3"]
start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(do_search, queries)
print(f"Total time: {time.time() - start}")
