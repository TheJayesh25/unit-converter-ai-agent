from typing import TypedDict, List, Union, Annotated, Sequence
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
import os
import requests
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model = 'gpt-4o'
)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
@tool
def convert_temperature(temperature: float, from_unit: str, to_unit: str) -> float:
    """This function converts temperature from one unit to another using Celsius as base"""

    ### HELPER FUNCTION 
    def conversion(value_in_celsius, to_unit):
        if to_unit in ['fahrenheit','f']:
            return (value_in_celsius * 9/5) + 32
    
        if to_unit in ['kelvin','k']:
            return value_in_celsius + 273.15

    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    value_in_celsius = temperature

    if from_unit in ['fahrenheit','f']:
        value_in_celsius = (temperature - 32) * 5/9
    
    if from_unit in ['kelvin','k']:
        value_in_celsius = temperature - 273.15

    converted_value = conversion(value_in_celsius, to_unit)
    return round(converted_value, 6)

@tool
def convert_distance(distance: float, from_unit: str, to_unit: str) -> float:
    """Converts distance from one unit to another using meters as base."""
    unit_aliases = {
        # Metric
        "millimeter": "mm", "millimetre": "mm", "millimeters": "mm", "millimetres": "mm", "mm": "mm",
        "centimeter": "cm", "centimetre": "cm", "centimeters": "cm", "centimetres": "cm", "cm": "cm",
        "meter": "m", "metre": "m", "meters": "m", "metres": "m", "m": "m",
        "kilometer": "km", "kilometre": "km", "kilometers": "km", "kilometres": "km", "km": "km", "kms": "km",

        # Imperial
        "inch": "inch", "inches": "inch", "in": "inch",
        "foot": "foot", "feet": "foot", "ft": "foot",
        "yard": "yard", "yards": "yard", "yd": "yard",
        "mile": "mile", "miles": "mile", "mi": "mile"
    }

    from_unit = unit_aliases.get(from_unit.lower().strip(), from_unit.lower().strip())
    to_unit = unit_aliases.get(to_unit.lower().strip(), to_unit.lower().strip())

    unit_to_meter = {
        "mm": 1e-3,
        "cm": 1e-2,
        "m": 1,
        "km": 1e3,
        "inch": 0.0254,
        "foot": 0.3048,
        "yard": 0.9144,
        "mile": 1609.34
    }

    if from_unit not in unit_to_meter or to_unit not in unit_to_meter:
        return f"Sorry, conversion from {from_unit} to {to_unit} is not supported yet."

    # Convert from source unit to meters
    value_in_meters = distance * unit_to_meter[from_unit]

    # Convert from meters to target unit
    converted_value = value_in_meters / unit_to_meter[to_unit]

    return round(converted_value, 6)  # rounded for neatness

@tool
def convert_currency(value: float, from_unit: str, to_unit: str) -> Union[float, str]:
    """Converts currency from one unit to another using ExchangeRate API."""
    from_unit = from_unit.upper().strip()
    to_unit = to_unit.upper().strip()

    try:
        API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_unit}"
        response = requests.get(url, timeout=5)

        response.raise_for_status()  # Raises HTTPError for bad status codes

        data = response.json()
        conversion_rate = data["conversion_rates"].get(to_unit)

        if conversion_rate is None:
            return f"Sorry, currency code '{to_unit}' not supported."

        return round(value * conversion_rate, 6)

    except requests.exceptions.RequestException as e:
        return f"Network error: {e}"
    except KeyError:
        return "Unexpected response format from currency API."
    except Exception as e:
        return f"Something went wrong: {e}"
    
tools = [convert_temperature, convert_distance, convert_currency]

llm = llm.bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are an intelligent unit conversion assistant. \
    You ONLY respond to valid temperature, distance, or currency conversion queries. \
    If the query doesn't relate to those, respond politely saying it's not within your scope. \
    convert_temperature, convert_distance and convert_currency are the three tools made available to you. \
    You make use of these tools for temperature, distance and currency conversion related tasks.")
  
    response = llm.invoke([system_prompt]+state['messages'])
    return {'messages':[response]}

def should_continue(state:AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls: 
        return "end"
    else:
        return "continue"
    
graph = StateGraph(AgentState)
graph.add_node('Model',model_call)
graph.add_node('Tools',ToolNode(tools))
graph.add_conditional_edges(
    'Model',
    should_continue,
    {
        'continue':'Tools',
        'end': END
    }
)
graph.add_edge('Tools','Model')
graph.add_edge(START,'Model')
app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

def print_conversation(conversation):
    for msg in conversation["messages"]:
        if isinstance(msg, AIMessage) and msg.content.strip():  # Only print non-empty AI responses
            print(f"\n🤖 AI: {msg.content}\n")

user_input = input("🧑 Human: ")
while user_input != "exit":
    response = app.invoke({"messages": [HumanMessage(content=user_input)]})
    print_conversation(response)
    # print_stream(app.stream({"messages": [HumanMessage(content=user_input)]}, stream_mode="values"))
    user_input = input("🧑 Human: ")
    
