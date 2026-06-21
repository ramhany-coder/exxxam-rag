from agents import *
from models import State
from langgraph.graph import StateGraph, START, END

class WorkFlow:
    def __init__(self):
        self.rewrite_query = rewritter_agent
        self.reponse_agent = responser_agent
        self.retriever_agent = retrival_agent

    def build_graph(self):
        graph = StateGraph(State)

        graph.add_node("rewrite_query", self.rewrite_query)
        graph.add_node("reponse_agent", self.reponse_agent)
        graph.add_node("retriever", self.retriever_agent)

        graph.add_edge(START, "rewrite_query")
        graph.add_edge("rewrite_query", "retriever")
    
        graph.add_edge("retriever", "reponse_agent")
        graph.add_edge("reponse_agent", END)

        return graph.compile()
    
    def run(self, initial_state: State):
        graph = self.build_graph()
        results = graph.invoke(initial_state)
        return results
    
workflow = WorkFlow

client = workflow()

test = client.run({
    "query": "how to make pivote tble in numpy?",  
})
print(test.get("rewritten_query"))
print(test.get("response"))