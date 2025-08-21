import os
import platform
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langchain.schema import SystemMessage


class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def run_command(cmd: str, file_content: str = None):
    """
    Executes shell commands in Windows PowerShell or Unix.
    If `file_content` is provided, writes it to the file `cmd`.
    """
    system_os = platform.system()

    # If file_content is given, write to file safely
    if file_content:
        os.makedirs(os.path.dirname(cmd), exist_ok=True)
        with open(cmd, "w", encoding="utf-8") as f:
            f.write(file_content)
        return f"File {cmd} created with content."

    # Otherwise, execute shell command
    if system_os == "Windows":
        ps_command = f"powershell -Command \"{cmd}\""
        return os.system(ps_command)
    else:
        return os.system(cmd)


# Initialize LLM
llm = init_chat_model(model_provider="openai", model="gpt-4.1")
llm_with_tool = llm.bind_tools(tools=[run_command])


def chatbot(state: State):
    system_prompt = SystemMessage(content="""
        You are an AI Coding assistant.
        - All code must be human-readable line by line, without enclosing lines in strings.
        - All files should be saved inside 'chat_gpt/'.
        - On Windows, use PowerShell-compatible commands.
        - Never generate Unix-style commands like `touch` or `mkdir -p`.
        - If you need to create a file, you can just specify the file path and content,
          and the run_command tool will write it safely.
          
        Example:
        User: "Create a Python file selection_sort.py and write selection sort."
        AI should call:
        run_command(cmd="chat_gpt/selection_sort.py", file_content="<python code here>")
        user: create a react app 
        Ai should call 
        run command tool :and do npm create vite@latest my-app
                                  
    """)

    message = llm_with_tool.invoke([system_prompt] + state["messages"])
    # assert len(message.tool_calls) <= 1
    return {"messages": [message]}


tool_node = ToolNode(tools=[run_command])

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()


def create_chat_graph(checkpointer=None):
    return graph_builder.compile(checkpointer=checkpointer)
