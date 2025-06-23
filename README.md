# 🔁 Unit Converter Agent (LangGraph + LangChain Tools)

This is a LangGraph-based intelligent agent designed to handle **temperature**, **distance**, and **currency** conversions through natural language queries. It uses `LangGraph`, `LangChain`, and `OpenAI GPT-4o` with custom tools for performing unit conversion tasks.

---

## 🧠 What It Does

The agent understands natural language queries like:

- `Convert 100 Fahrenheit to Celsius`
- `How many kilometers are in 50 miles?`
- `Convert 100 USD to INR`

It uses structured tools under-the-hood for:

- 🌡️ **Temperature Conversion** (`Celsius`, `Fahrenheit`, `Kelvin`)
- 📏 **Distance Conversion** (metric & imperial: `mm`, `cm`, `m`, `km`, `inch`, `foot`, `yard`, `mile`)
- 💱 **Currency Conversion** (real-time via ExchangeRate API)

---

## 🔍 Why Use a Multi-Tool AI Agent?

Unlike standalone language models that only "guess" answers from training data, this agent is **enhanced with real tools** to provide precise, reliable, and up-to-date results.

### ✅ Advantages Over Plain LLM Agents

| Feature                        | Plain LLM Agent         | Multi-Tool AI Agent (This Project)     |
|-------------------------------|-------------------------|----------------------------------------|
| 🌡️ Accurate Unit Conversion   | May hallucinate          | Uses hard-coded, tested logic          |
| 💱 Currency Exchange Rates    | Outdated or hallucinated | Uses real-time API via ExchangeRate    |
| 📏 Distance Calculations      | May miscalculate units   | Converts using base metric logic       |
| 🔁 Contextual Reuse           | Limited memory in loop   | Retains state across tool calls        |
| 🧠 Modular Design             | One-shot response        | Modular graph with reusable tools      |
| 🔐 Safety and Control         | Unpredictable            | Deterministic tool output              |

### 🧠 How It Helps

- Combines **language understanding** (LLM) with **functional execution** (tools)
- Can **route intelligently** between different tools based on user intent
- Ensures **precision** in logic-heavy tasks like conversions, which pure LLMs are not designed for
- Easily extensible — add more tools like date conversion, BMI calculators, tax estimators, etc.

---

> 🤖 This is not just an LLM — it's an **intelligent agent** that knows when to "think" and when to "act".

---

## ⚙️ How It Works

### 🧩 Tools

Three tools are defined and made available to the LLM:

- `convert_temperature(temperature, from_unit, to_unit)`
- `convert_distance(distance, from_unit, to_unit)`
- `convert_currency(value, from_unit, to_unit)`

### 🔄 LangGraph Flow

```text
START → Model Node → (ToolNode if needed) → Model Node → … → END
```
- The Model node interprets user input and decides whether to call a tool.
- The ToolNode executes the requested tool.
- The loop continues until the conversation ends.

### 🗂️ Project Structure

```
unit-converter-agent/
│
├── agent.py                # Main logic for the LangGraph agent
├── .env                    # Contains API key for ExchangeRate API
├── requirements.txt        # Python dependencies
└── README.md               # You're here!
```

### 📦 Installation

```
# 1. Clone the repo
git clone https://github.com/your-username/unit-converter-ai-agent.git
cd unit-converter-ai-agent

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your ExchangeRate API key to a .env file
echo "EXCHANGE_RATE_API_KEY=your_api_key_here" > .env
```

### 🚀 Usage

```python agent.py```

Then interact with the agent via terminal:
🧑 Human: Convert 100 USD to INR
🤖 AI: 100 USD is approximately 8300 INR.

Type exit to stop the program.

### 🔐 API Key
You’ll need an API key from [ExchangeRate](https://app.exchangerate-api.com/) API and place it in your .env file

### ✅ Features
- ✅ Natural language support via GPT-4o
- ✅ Custom tool calls with LangChain
- ✅ Multi-turn conversion conversations
- ✅ Currency rates via external API
- ✅ Gracefully handles invalid or unsupported units

### 🧪 Example Queries

| Query                             | Intent                 |
| --------------------------------- | ---------------------- |
| `Convert 212 F to C`              | Temperature conversion |
| `How many kilometers is 3 miles?` | Distance conversion    |
| `Convert 500 EUR to JPY`          | Currency conversion    |

### 📌 Requirements

- Python 3.9+
- OpenAI API Key (via langchain_openai)
- ExchangeRate API Key

### 🛠️ Built With
- LangGraph
- LangChain
- OpenAI GPT-4o
- ExchangeRate API

### 🧑‍💻 Author
Jayesh Suryawanshi
- 🧠 Python Developer | 💡 AI Tools Builder | 🌍 Data & Engineering Enthusiast
- 📫 [LinkedIn](https://www.linkedin.com/in/jayesh-suryawanshi-858bb21aa/)

### 📄 License
MIT License

