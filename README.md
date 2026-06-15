# Vexa



# ✨ Vexa — Your Agent. Your Voice.

> Build your own AI agent with a unique personality, expertise, and soul.

## 🎯 What is Vexa?

Vexa is a creative AI application that lets users design and bring to life 

their own personalized AI agents. Each agent has a unique name, personality, 

expertise, communication style, and backstory — then comes alive as an 

intelligent conversational partner.

## 🏆 Hackathon Track

**Agents League Hackathon 2026 — Creative Apps Track**

Built with GitHub Copilot and Microsoft Foundry IQ

## ✨ Features

- 🎭 **Agent Creator** — Design agents with unique personalities

- 🧠 **Dual Model Routing** — Smart routing between LLaMA 8B and 70B

- 🛡️ **Guardrails** — Input validation and output quality checks

- 💰 **Cost Optimization** — Automatic model selection saves up to 90%

- 🧠 **Memory** — Agents remember conversation context

- ⚡ **Fast Inference** — Powered by Groq LPU engine

## 🏗️ Architecture

User Input  
↓  
🛡️ Input Guardrails (prompt injection, safety)  
↓  
🧭 Router Agent (complexity scoring)  
├── Simple → LLaMA 3.1 8B (fast, free)  
└── Complex → LLaMA 3.3 70B (powerful)  
↓  
🎭 Character Agent (persona + memory)  
↓  
🛡️ Output Guardrails (quality check)  
↓  
💬 Response to User



## 💰 Cost Optimization Strategy

- **Model Routing** — cheap model for simple queries

- **Response Caching** — repeated queries cost $0

- **Token Optimization** — trimmed prompts reduce cost

- **Result** — up to 90% cost reduction vs single model

## 🛡️ Guardrails Implementation

**Input Guardrails:**

- Prompt injection detection

- Message length validation

- Harmful content filtering

**Output Guardrails:**

- Response quality check

- Minimum length validation

- Character consistency

## 🤖 GitHub Copilot Usage

GitHub Copilot was used throughout development for:

- Generating the guardrails validation logic

- Autocompleting Groq API integration

- Suggesting memory management structure

- Debugging Streamlit session state

- Writing the router agent complexity scoring

## 🧠 Microsoft IQ Integration

**Foundry IQ** — Used for grounding agent responses in the 

knowledge base `knowledge/base_knowledge.md`), ensuring 

agents provide cited, accurate information about their 

expertise domains.

## 🚀 Tech Stack

| Component | Technology |

|---|---|

| UI | Streamlit |

| Fast LLM | LLaMA 3.1 8B via Groq |

| Smart LLM | LLaMA 3.3 70B via Groq |

| Guardrails | Custom Python validators |

| Memory | Streamlit Session State |

| Inference | Groq LPU Engine |

## ⚙️ Setup

### Prerequisites

- Python 3.10+

- Groq API key (free at [console.groq.com](http://console.groq.com))

### Installation

```bash

git clone [https://github.com/Sahita9/Vexa.git](https://github.com/Sahita9/Vexa.git)

cd Vexa

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

```

### Configuration

```bash

cp .env.example .env

# Add your GROQ_API_KEY to .env

```

### Run

```bash

python -m streamlit run [app.py](http://app.py)

```

## 📁 Project Structure

vexa/  
├── [app.py](http://app.py) ← Main Streamlit app  
├── agents/  
│ ├── [router.py](http://router.py) ← Model selection  
│ ├── [character.py](http://character.py) ← Personality engine  
│ └── [memory.py](http://memory.py) ← Conversation memory  
├── guardrails/  
│ ├── input_[guard.py](http://guard.py) ← Input validation  
│ └── output_[guard.py](http://guard.py) ← Output quality  
├── models/  
│ └── llama_[client.py](http://client.py) ← Groq integration  
├── knowledge/  
│ └── base_[knowledge.md](http://knowledge.md) ← Foundry IQ knowledge base  
└── requirements.txt





