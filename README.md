# MarkanM Python SDK

<div align="center">

[![PyPI version](https://img.shields.io/pypi/v/markanm?color=7c3aed&style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/markanm/)
[![Python](https://img.shields.io/pypi/pyversions/markanm?color=0ea5e9&style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/markanm/)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-MarkanM%20Chat-7c3aed?style=for-the-badge)](https://chat.markanm.com)

**The official Python SDK for building bots, AI agents, and integrations on [MarkanM Chat](https://chat.markanm.com).**

[📖 Documentation](https://chat.markanm.com/developers/docs) · [🚀 Developer Portal](https://chat.markanm.com/developers) · [💬 Chat](https://chat.markanm.com) · [🐛 Issues](https://github.com/markanm/markanm-python-sdk/issues)

</div>

---

## Table of Contents

- [What is MarkanM?](#what-is-markanm)
- [Installation](#installation)
- [Getting Your Bot Token](#getting-your-bot-token)
- [Quick Start — Your First Bot in 60 Seconds](#quick-start)
- [Bot Commands](#bot-commands)
- [Event Listeners](#event-listeners)
- [Receiving User Input](#receiving-user-input)
- [Sending Messages](#sending-messages)
- [CommandContext Reference](#commandcontext-reference)
- [Event Reference](#event-reference)
- [AI Integration](#ai-integration)
  - [Supported AI Providers](#supported-ai-providers)
  - [Sarvam AI (Indian Multilingual)](#sarvam-ai)
  - [Groq (Ultra-Fast, Free)](#groq)
  - [Google Gemini](#google-gemini)
  - [OpenAI GPT](#openai)
  - [Anthropic Claude](#anthropic-claude)
  - [Mistral AI](#mistral-ai)
  - [DeepSeek](#deepseek)
  - [Together AI](#together-ai)
  - [Perplexity AI](#perplexity-ai)
  - [Cohere](#cohere)
  - [HuggingFace Inference API](#huggingface)
  - [Ollama (Local, Free)](#ollama)
  - [OpenRouter (100+ Models)](#openrouter)
  - [Custom HTTP Endpoint](#custom-http-endpoint)
- [Conversation Memory](#conversation-memory)
- [Multi-Turn Chat](#multi-turn-chat)
- [Bot Personas & Custom Training](#bot-personas--custom-training)
- [RAG — Custom Knowledge Base](#rag--custom-knowledge-base)
- [Persistent Memory (Database)](#persistent-memory)
- [Interactive Forms & Multi-Step Flows](#interactive-forms--multi-step-flows)
- [Per-User State Management](#per-user-state-management)
- [Webhooks (Production)](#webhooks-production)
- [Polling (Development)](#polling-development)
- [Error Handling](#error-handling)
- [Complete Bot Examples](#complete-bot-examples)
- [Deploying to Production](#deploying-to-production)
- [API Reference](#api-reference)
- [Changelog](#changelog)

---

## What is MarkanM?

[MarkanM Chat](https://chat.markanm.com) is a real-time chat platform — like WhatsApp or Telegram — where developers can build and publish **bots** that users can interact with directly in chat rooms.

With the `markanm` Python SDK you can:

- 🤖 **Build bots** that respond to commands and messages
- 🧠 **Connect any AI** (Sarvam, Groq, Gemini, OpenAI, Ollama...) to your bot
- 💬 **Receive and process** any text input from users
- 🌐 **Deploy to production** with webhooks or run locally with polling
- 🔐 **Authenticate users** with OAuth 2.0 ("Continue with MarkanM")

---

## Installation

```bash
pip install markanm
```

**Optional: Install `httpx` for async HTTP (recommended)**

```bash
pip install markanm httpx
```

> The SDK automatically falls back to `urllib` if `httpx` is not installed.

**Requirements:** Python 3.8+

---

## Getting Your Bot Token

1. Go to [chat.markanm.com/developers](https://chat.markanm.com/developers)
2. Click **"Developer Portal"**
3. Navigate to the **"Bots"** tab
4. Click **"Create Bot"**
5. Fill in:
   - **Name** — display name (e.g. "My Helper Bot")
   - **Username** — @handle (e.g. `helperbot` → users find it as `@helperbot`)
   - **Description** — what your bot does
   - **Category** — AI Assistant, Utility, Fun, etc.
6. Click **Create** → copy your **Bot Token** (`mkbot_xxxxxxxxxxxxxxxxxx`)

> ⚠️ Keep your bot token secret. Never commit it to Git. Use environment variables.

```bash
# Set as environment variable (recommended)
export MARKANM_BOT_TOKEN="mkbot_xxxxxxxxxxxxxxxxxxxxxxxx"
```

---

## Quick Start

### Your First Bot in 60 Seconds

```python
# hello_bot.py
import os
from markanm import Bot

# Initialize bot with your token
bot = Bot(os.environ["MARKANM_BOT_TOKEN"])

# Respond to /hello command
@bot.command("hello")
async def hello(ctx):
    await ctx.reply("Hello! 👋 I'm alive and running!")

# Respond to /help command
@bot.command("help")
async def help_cmd(ctx):
    await ctx.reply("""🤖 Available Commands:
/hello — Say hello
/help  — Show this help message
/ping  — Check if I'm online
/echo <text> — Repeat your text back""")

# Respond to /ping command
@bot.command("ping")
async def ping(ctx):
    await ctx.reply("Pong! 🏓 Bot is online.")

# Respond to /echo command
@bot.command("echo")
async def echo(ctx):
    text = " ".join(ctx.args)
    if not text:
        await ctx.reply("Usage: /echo <your message>")
        return
    await ctx.reply(f"🔊 {text}")

# Start the bot
bot.run_polling()
```

**Run it:**

```bash
python hello_bot.py
```

**Output:**

```
🤖 MarkanM Bot running in development polling mode (interval: 2.0s)...
⏳ Polling... (20s elapsed, no events yet)
📨 Received 1 event(s)
  ▶ Event: type='command.received' payload={...}
```

Now go to MarkanM, find your bot (`@yourbotusername`), click **Start Bot**, and send `/hello`. Your bot will reply instantly!

---

## Bot Commands

Commands are triggered when users send `/commandname` in chat.

### Basic Command

```python
@bot.command("greet")
async def greet(ctx):
    await ctx.reply("Hello there! 👋")
```

User sends: `/greet` → Bot replies: `Hello there! 👋`

---

### Command with Arguments

Arguments are the words after the command name. They are split by spaces and available as `ctx.args` (a list).

```python
@bot.command("say")
async def say(ctx):
    # ctx.args = ["hello", "world"] for input "/say hello world"
    message = " ".join(ctx.args)

    if not message:
        await ctx.reply("Usage: /say <message>")
        return

    await ctx.reply(f"📢 {message}")
```

```python
# Accessing individual arguments
@bot.command("add")
async def add(ctx):
    if len(ctx.args) < 2:
        await ctx.reply("Usage: /add <number1> <number2>")
        return

    try:
        a = float(ctx.args[0])
        b = float(ctx.args[1])
        await ctx.reply(f"✅ {a} + {b} = {a + b}")
    except ValueError:
        await ctx.reply("❌ Please provide valid numbers.")
```

---

### Command with Named Arguments

Parse structured arguments like `/order --item pizza --qty 2`:

```python
@bot.command("order")
async def order(ctx):
    # Parse --key value pairs from ctx.args
    args = ctx.args
    params = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--") and i + 1 < len(args):
            params[args[i][2:]] = args[i + 1]
            i += 2
        else:
            i += 1

    item = params.get("item", "unknown")
    qty = params.get("qty", "1")
    await ctx.reply(f"🛒 Order placed: {qty}x {item}")
```

---

### Registering Multiple Commands

```python
from markanm import Bot

bot = Bot("mkbot_YOUR_TOKEN")

COMMANDS = {
    "hello":   "hello_handler",
    "help":    "help_handler",
    "ping":    "ping_handler",
}

@bot.command("hello")
async def hello_handler(ctx):
    await ctx.reply("Hello! 👋")

@bot.command("help")
async def help_handler(ctx):
    lines = ["📋 **Commands:**"]
    for cmd in COMMANDS:
        lines.append(f"  /{cmd}")
    await ctx.reply("\n".join(lines))

@bot.command("ping")
async def ping_handler(ctx):
    await ctx.reply("Pong! 🏓")

bot.run_polling()
```

---

### Command with User Info

```python
@bot.command("profile")
async def profile(ctx):
    user = ctx.user
    await ctx.reply(
        f"👤 Your Profile:\n"
        f"Username: @{user.username}\n"
        f"Display Name: {user.display_name}\n"
        f"User ID: {user.id}"
    )
```

---

## Event Listeners

Event listeners respond to **any event** including plain text messages (not just commands).

### Listen to Any Message

```python
@bot.on("command.received")
async def on_any_message(evt):
    text = evt.payload.get("text", "").strip()
    user = evt.payload.get("user", {})
    user_name = user.get("display_name", "there")

    print(f"[{user_name}]: {text}")
```

> **Note:** `command.received` fires for EVERY message sent to your bot — whether it starts with `/` or not.

---

### Separate Slash Commands from Plain Text

```python
@bot.on("command.received")
async def on_message(evt):
    text = evt.payload.get("text", "").strip()

    if text.startswith("/"):
        # This is a slash command — @bot.command() will handle it
        return

    # This is a plain-text message
    await evt.reply(f"You said: {text}")
```

---

### Respond to Keywords

```python
@bot.on("command.received")
async def keyword_handler(evt):
    text = evt.payload.get("text", "").lower().strip()
    user_name = evt.payload.get("user", {}).get("display_name", "friend")

    if text.startswith("/"):
        return  # Skip commands

    if "hello" in text or "hi" in text or "hey" in text:
        await evt.reply(f"Hey {user_name}! 👋 How can I help you?")
    elif "bye" in text or "goodbye" in text:
        await evt.reply(f"Goodbye {user_name}! 👋 Come back soon.")
    elif "thank" in text:
        await evt.reply("You're welcome! 😊")
    elif "?" in text:
        await evt.reply("Good question! Let me think... 🤔")
    else:
        await evt.reply(f"Got your message! Type /help to see what I can do.")
```

---

### Multiple Listeners for Same Event

```python
# Both of these will fire for every "command.received" event
@bot.on("command.received")
async def logger(evt):
    print(f"[LOG] {evt.payload.get('user', {}).get('username')}: {evt.payload.get('text')}")

@bot.on("command.received")
async def responder(evt):
    text = evt.payload.get("text", "")
    if "help" in text.lower():
        await evt.reply("Type /help for commands!")
```

---

## Receiving User Input

### How User Data Arrives

Every event's `payload` contains:

| Field | Type | Description |
|-------|------|-------------|
| `text` | `str` | The full message text (e.g. `/ask who is PM`) |
| `command` | `str` | The command name without `/` (e.g. `ask`) |
| `user.id` | `int` | Sender's user ID |
| `user.username` | `str` | Sender's @username |
| `user.display_name` | `str` | Sender's display name |
| `user.avatar_url` | `str` | Sender's avatar URL |
| `room_id` | `str` | The conversation/room ID |
| `conversation_id` | `str` | Same as room_id |
| `message_id` | `str` | Unique message ID |
| `message.text` | `str` | Message content |
| `args` | `list` | List of words after command (if slash command) |

### Extracting Everything from a Message

```python
@bot.on("command.received")
async def full_example(evt):
    payload = evt.payload

    # Text
    text = payload.get("text", "").strip()

    # User info
    user = payload.get("user", {})
    user_id = user.get("id")
    username = user.get("username", "")
    display_name = user.get("display_name", "")
    avatar_url = user.get("avatar_url", "")

    # Room info
    room_id = payload.get("room_id") or payload.get("conversation_id")

    # Message info
    message = payload.get("message", {})
    message_id = payload.get("message_id")

    # Command-specific (if slash command)
    command = payload.get("command", "")

    print(f"Message from @{username} (ID:{user_id}) in room {room_id}: '{text}'")
    await evt.reply(f"Hi {display_name}! Got your message.")
```

### Accessing User Info in Commands

```python
@bot.command("info")
async def info(ctx):
    # ctx.user — UserContext object
    print(ctx.user.id)
    print(ctx.user.username)
    print(ctx.user.display_name)

    # ctx.room — RoomContext object
    print(ctx.room_id)

    # ctx.args — list of arguments
    print(ctx.args)

    # ctx.text — full raw text after command
    print(ctx.text)

    # ctx.command — command name (without /)
    print(ctx.command)
```

---

## Sending Messages

### Reply to the Current Room

```python
# In a command handler:
await ctx.reply("Hello! 👋")

# In an event listener:
await evt.reply("Got your message!")
```

### Send to a Specific Room

```python
await bot.send_message(room_id="42", text="Hello room 42!")
```

### Send a Message with Formatting

MarkanM supports plain text. Use newlines for structure:

```python
@bot.command("menu")
async def menu(ctx):
    await ctx.reply("""🍔 Today's Menu:

1. Burger       — ₹120
2. Pizza Slice  — ₹80
3. Cold Drink   — ₹40
4. French Fries — ₹60

Type /order <item number> to place your order!""")
```

### Send Long Responses in Parts

```python
@bot.command("report")
async def report(ctx):
    await ctx.reply("📊 Generating report...")

    # Simulate processing
    import asyncio
    await asyncio.sleep(1)

    await ctx.reply("📈 Part 1: Sales Data\n- Jan: ₹50,000\n- Feb: ₹62,000\n- Mar: ₹78,000")
    await ctx.reply("📉 Part 2: Expenses\n- Rent: ₹20,000\n- Salaries: ₹30,000")
    await ctx.reply("✅ Report complete!")
```

---

## CommandContext Reference

When you register a `@bot.command()` handler, it receives a `CommandContext` (called `ctx`):

```python
@bot.command("example")
async def handler(ctx):
    # ── Properties ────────────────────────────────────────
    ctx.command        # str  — command name ("example")
    ctx.text           # str  — full text after command name
    ctx.args           # list — words split from text
    ctx.raw_data       # dict — full raw event payload

    # ── Nested Objects ────────────────────────────────────
    ctx.user           # UserContext
    ctx.user.id        # int
    ctx.user.username  # str
    ctx.user.display_name  # str
    ctx.user.avatar_url    # str

    ctx.room           # RoomContext
    ctx.room_id        # str — shortcut for ctx.room.id
    ctx.room.id        # str
    ctx.room.name      # str

    ctx.message        # MessageContext
    ctx.message.id     # str
    ctx.message.text   # str
    ctx.message.type   # str ("text", "card", etc.)

    # ── Methods ───────────────────────────────────────────
    await ctx.reply("text")          # Send message to room
    await bot.send_message(room_id, "text")  # Send to any room
```

---

## Event Reference

When you register a `@bot.on()` handler, it receives an `Event`:

```python
@bot.on("command.received")
async def handler(evt):
    # ── Properties ────────────────────────────────────────
    evt.id          # str — unique event ID
    evt.type        # str — event type ("command.received")
    evt.timestamp   # str — when event was created
    evt.payload     # dict — full payload (see table above)
    evt.raw_data    # dict — raw event data from server
    evt.room_id     # str — extracted from payload

    # ── Aliases ───────────────────────────────────────────
    evt.event_id    # same as evt.id
    evt.event_type  # same as evt.type
    evt.created_at  # same as evt.timestamp

    # ── Methods ───────────────────────────────────────────
    await evt.reply("text")   # Send message to this event's room
```

---

## AI Integration

The `markanm.ai` module lets you connect **any AI provider** to your bot with a single import. No lock-in — bring your own API key.

### Basic Pattern

```python
from markanm import Bot
from markanm.ai import AI

bot = Bot("mkbot_YOUR_TOKEN")
ai = AI(provider="PROVIDER_NAME", api_key="YOUR_API_KEY")

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args)
    if not question:
        await ctx.reply("Usage: /ask <your question>")
        return

    answer = await ai.generate(question)
    await ctx.reply(answer)

bot.run_polling()
```

Just change `provider=` and `api_key=` to switch between services.

---

## Supported AI Providers

| Provider | `provider=` value | Default Model | Best For | Cost |
|----------|------------------|---------------|----------|------|
| Sarvam AI | `"sarvam"` | `sarvam-105b` | Indian languages (Hindi, Tamil…) | Paid |
| Groq | `"groq"` | `llama3-8b-8192` | Fastest responses | Free tier |
| Google Gemini | `"gemini"` | `gemini-1.5-flash` | Multimodal, web context | Free tier |
| OpenAI | `"openai"` | `gpt-3.5-turbo` | Most capable | Paid |
| Anthropic Claude | `"anthropic"` | `claude-3-haiku-20240307` | Precise, safe | Paid |
| Mistral AI | `"mistral"` | `mistral-small-latest` | EU-hosted, private | Paid |
| DeepSeek | `"deepseek"` | `deepseek-chat` | Affordable, smart | Paid |
| Together AI | `"together"` | `mistralai/Mistral-7B-Instruct-v0.1` | 100s of open models | Free tier |
| Perplexity | `"perplexity"` | `llama-3.1-sonar-small-128k-online` | Live web search | Paid |
| Cohere | `"cohere"` | `command-r` | Business NLP | Free tier |
| HuggingFace | `"huggingface"` | `mistralai/Mistral-7B-Instruct-v0.1` | Open source models | Free |
| Ollama | `"ollama"` | `llama3` | Local/private, no cost | **FREE** |
| OpenRouter | `"openrouter"` | `meta-llama/llama-3-8b-instruct:free` | 100+ models, free tier | Free tier |
| Custom API | `"custom"` | your choice | Your own server | — |

---

## Sarvam AI

**Sarvam AI** is an Indian-built AI that understands Hindi, Tamil, Telugu, Bengali, Marathi, Kannada, Malayalam, Odia, Punjabi, and Gujarati natively.

**Get API Key:** [api.sarvam.ai](https://api.sarvam.ai) → Sign up → Create API Key

**Available Models:**
- `sarvam-105b` — General-purpose (recommended for Q&A)
- `sarvam-105b-conversations` — Optimized for multi-turn chat

```python
from markanm import Bot
from markanm.ai import AI

bot = Bot("mkbot_YOUR_TOKEN")

ai = AI(
    provider="sarvam",
    api_key="sk_YOUR_SARVAM_KEY",
    model="sarvam-105b",
    system_prompt=(
        "You are a helpful assistant. "
        "If the user writes in Hindi or any Indian language, always respond in the same language."
    )
)

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args)
    if not question:
        await ctx.reply("कुछ पूछिए! 🙏\nUsage: /ask <your question>")
        return
    answer = await ai.generate(question)
    await ctx.reply(answer)

@bot.on("command.received")
async def on_message(evt):
    text = evt.payload.get("text", "").strip()
    if not text or text.startswith("/"):
        return
    reply = await ai.generate(text)
    await evt.reply(reply)

bot.run_polling()
```

**Example usage:**

| User sends | Bot replies |
|------------|-------------|
| `/ask भारत का PM कौन है?` | `भारत के प्रधानमंत्री नरेंद्र मोदी हैं।` |
| `/ask who is the president of India?` | `The President of India is Droupadi Murmu.` |
| `நமஸ்காரம்` | `நமஸ்காரம்! நான் உங்களுக்கு எப்படி உதவ முடியும்?` |

---

## Groq

**Groq** is the fastest AI inference platform — responses arrive in under 1 second. It runs open-source models like LLaMA 3.

**Get Free API Key:** [console.groq.com](https://console.groq.com) → Sign up → API Keys → Create

**Available Models:**
- `llama3-8b-8192` — Fast, free, good quality
- `llama3-70b-8192` — Smarter but slower
- `mixtral-8x7b-32768` — Long context (32k tokens)
- `gemma2-9b-it` — Google's Gemma 2
- `llama-3.1-8b-instant` — Even faster

```python
from markanm import Bot
from markanm.ai import AI

bot = Bot("mkbot_YOUR_TOKEN")

ai = AI(
    provider="groq",
    api_key="gsk_YOUR_GROQ_API_KEY",
    model="llama3-8b-8192",  # Free, fast model
    system_prompt="You are a helpful, friendly assistant. Keep answers concise.",
    timeout=30.0
)

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args)
    if not question:
        await ctx.reply("Usage: /ask <question>")
        return
    answer = await ai.generate(question)
    await ctx.reply(answer)

@bot.command("explain")
async def explain(ctx):
    topic = " ".join(ctx.args)
    if not topic:
        await ctx.reply("Usage: /explain <topic>")
        return
    answer = await ai.generate(
        f"Explain {topic} in simple terms, like I'm 12 years old."
    )
    await ctx.reply(answer)

@bot.command("code")
async def code(ctx):
    task = " ".join(ctx.args)
    if not task:
        await ctx.reply("Usage: /code <what you want to build>")
        return
    answer = await ai.generate(
        f"Write Python code for: {task}\nProvide clean, working code with brief comments."
    )
    await ctx.reply(answer)

bot.run_polling()
```

---

## Google Gemini

**Google Gemini** — powerful, multimodal AI with a generous free tier.

**Get Free API Key:** [aistudio.google.com](https://aistudio.google.com) → Sign in → Get API key

**Available Models:**
- `gemini-1.5-flash` — Fast, free (recommended)
- `gemini-1.5-pro` — More capable, higher limits
- `gemini-1.0-pro` — Stable older version
- `gemini-2.0-flash-exp` — Experimental, cutting-edge

```python
from markanm import Bot
from markanm.ai import AI

bot = Bot("mkbot_YOUR_TOKEN")

ai = AI(
    provider="gemini",
    api_key="AIzaSy_YOUR_GOOGLE_API_KEY",
    model="gemini-1.5-flash",
    system_prompt="You are a smart assistant. Provide accurate, helpful answers."
)

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args)
    if not question:
        await ctx.reply("Usage: /ask <question>")
        return
    answer = await ai.generate(question)
    await ctx.reply(answer)

@bot.command("summarize")
async def summarize(ctx):
    text = " ".join(ctx.args)
    if not text:
        await ctx.reply("Usage: /summarize <long text>")
        return
    summary = await ai.generate(f"Summarize this in 3 bullet points:\n\n{text}")
    await ctx.reply(summary)

@bot.command("translate")
async def translate(ctx):
    if len(ctx.args) < 2:
        await ctx.reply("Usage: /translate <language> <text>\nExample: /translate Hindi Hello world")
        return
    lang = ctx.args[0]
    text = " ".join(ctx.args[1:])
    result = await ai.generate(f"Translate this to {lang}: {text}")
    await ctx.reply(result)

bot.run_polling()
```

---

## OpenAI

**OpenAI** — the creators of GPT. Most capable but requires a paid account.

**Get API Key:** [platform.openai.com](https://platform.openai.com) → API Keys → Create new secret key

**Available Models:**
- `gpt-3.5-turbo` — Fast, cheap (recommended for bots)
- `gpt-4o` — Most capable
- `gpt-4o-mini` — Affordable, smarter than 3.5
- `gpt-4-turbo` — Large context window

```python
from markanm import Bot
from markanm.ai import AI

bot = Bot("mkbot_YOUR_TOKEN")

ai = AI(
    provider="openai",
    api_key="sk-YOUR_OPENAI_KEY",
    model="gpt-3.5-turbo",  # or "gpt-4o-mini" for better quality
    system_prompt="You are a helpful assistant."
)

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args)
    if not question:
        await ctx.reply("Usage: /ask <question>")
        return
    answer = await ai.generate(question)
    await ctx.reply(answer)

bot.run_polling()
```

---

## Anthropic Claude

**Anthropic Claude** — known for being safe, precise, and great at reasoning.

**Get API Key:** [console.anthropic.com](https://console.anthropic.com) → API Keys

**Available Models:**
- `claude-3-haiku-20240307` — Fastest, cheapest
- `claude-3-sonnet-20240229` — Balanced
- `claude-3-opus-20240229` — Most capable
- `claude-3-5-sonnet-20241022` — Latest, best quality

```python
from markanm import Bot
from markanm.ai import AI

bot = Bot("mkbot_YOUR_TOKEN")

ai = AI(
    provider="anthropic",
    api_key="sk-ant-YOUR_ANTHROPIC_KEY",
    model="claude-3-haiku-20240307",
    system_prompt="You are a helpful, harmless, and honest assistant."
)

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args)
    if not question:
        await ctx.reply("Usage: /ask <question>")
        return
    answer = await ai.generate(question)
    await ctx.reply(answer)

bot.run_polling()
```

---

## Mistral AI

**Mistral AI** — European AI company, GDPR-compliant, strong models.

**Get API Key:** [console.mistral.ai](https://console.mistral.ai) → API Keys

**Available Models:**
- `mistral-small-latest` — Fast, affordable
- `mistral-medium-latest` — Balanced
- `mistral-large-latest` — Most capable
- `open-mistral-7b` — Open source, cheaper
- `open-mixtral-8x7b` — Mixture of experts

```python
from markanm import Bot
from markanm.ai import AI

bot = Bot("mkbot_YOUR_TOKEN")

ai = AI(
    provider="mistral",
    api_key="YOUR_MISTRAL_API_KEY",
    model="mistral-small-latest"
)

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args)
    answer = await ai.generate(question)
    await ctx.reply(answer)

bot.run_polling()
```

---

## DeepSeek

**DeepSeek** — powerful Chinese AI models, very affordable pricing.

**Get API Key:** [platform.deepseek.com](https://platform.deepseek.com) → API Keys

**Available Models:**
- `deepseek-chat` — General purpose
- `deepseek-coder` — Specialized for code

```python
from markanm.ai import AI

ai = AI(
    provider="deepseek",
    api_key="sk-YOUR_DEEPSEEK_KEY",
    model="deepseek-chat"
)

# For coding bots:
ai_coder = AI(
    provider="deepseek",
    api_key="sk-YOUR_DEEPSEEK_KEY",
    model="deepseek-coder",
    system_prompt="You are an expert programmer. Provide clean, working code with explanations."
)
```

---

## Together AI

**Together AI** — run hundreds of open-source models with one API.

**Get API Key:** [api.together.xyz](https://api.together.xyz) → Sign up → API Keys

**Popular Models:**
- `mistralai/Mistral-7B-Instruct-v0.1`
- `meta-llama/Llama-2-70b-chat-hf`
- `NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO`

```python
from markanm.ai import AI

ai = AI(
    provider="together",
    api_key="YOUR_TOGETHER_API_KEY",
    model="mistralai/Mistral-7B-Instruct-v0.1"
)
```

---

## Perplexity AI

**Perplexity** — AI with live internet access. Perfect for real-time news/facts bots.

**Get API Key:** [www.perplexity.ai](https://www.perplexity.ai) → Settings → API

**Available Models:**
- `llama-3.1-sonar-small-128k-online` — Fast + web search
- `llama-3.1-sonar-large-128k-online` — Smarter + web search
- `llama-3.1-sonar-huge-128k-online` — Most capable + web

```python
from markanm import Bot
from markanm.ai import AI

bot = Bot("mkbot_YOUR_TOKEN")

# Real-time facts bot with live internet access!
ai = AI(
    provider="perplexity",
    api_key="pplx-YOUR_PERPLEXITY_KEY",
    model="llama-3.1-sonar-small-128k-online",
    system_prompt="You are a news bot. Answer based on current, real-time information."
)

@bot.command("news")
async def news(ctx):
    topic = " ".join(ctx.args)
    if not topic:
        await ctx.reply("Usage: /news <topic>\nExample: /news cricket score India")
        return
    answer = await ai.generate(f"What is the latest news about: {topic}")
    await ctx.reply(answer)

@bot.command("price")
async def price(ctx):
    item = " ".join(ctx.args)
    if not item:
        await ctx.reply("Usage: /price <item>\nExample: /price Bitcoin")
        return
    answer = await ai.generate(f"What is the current price of {item}?")
    await ctx.reply(answer)

bot.run_polling()
```

---

## Cohere

**Cohere** — enterprise-grade NLP models, good free tier.

**Get API Key:** [dashboard.cohere.com](https://dashboard.cohere.com) → API Keys

```python
from markanm.ai import AI

ai = AI(
    provider="cohere",
    api_key="YOUR_COHERE_API_KEY",
    model="command-r"
)
```

---

## HuggingFace

**HuggingFace Inference API** — access thousands of open-source models for free.

**Get Free API Key:** [huggingface.co](https://huggingface.co) → Settings → Access Tokens

```python
from markanm.ai import AI

ai = AI(
    provider="huggingface",
    api_key="hf_YOUR_HUGGINGFACE_TOKEN",
    model="mistralai/Mistral-7B-Instruct-v0.1"
)

# Other popular HuggingFace models:
# "google/flan-t5-xxl"
# "facebook/blenderbot-400M-distill"
# "tiiuae/falcon-7b-instruct"
# "HuggingFaceH4/zephyr-7b-beta"
```

---

## Ollama

**Ollama** — run AI models **100% locally** on your own computer. No API key, no cost, fully private.

**Setup:**

```bash
# 1. Install Ollama (Linux/macOS)
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Pull a model (choose one)
ollama pull llama3          # Meta LLaMA 3 (recommended)
ollama pull mistral         # Mistral 7B
ollama pull gemma2          # Google Gemma 2
ollama pull phi3            # Microsoft Phi-3 (small but smart)
ollama pull qwen2           # Alibaba Qwen 2
ollama pull codellama       # Code-specialized

# 3. Verify it's running
ollama list
```

```python
from markanm import Bot
from markanm.ai import AI

bot = Bot("mkbot_YOUR_TOKEN")

# No API key needed!
ai = AI(
    provider="ollama",
    model="llama3",  # must match a model you've pulled
    system_prompt="You are a helpful assistant.",
    # base_url="http://localhost:11434/api"  # default
)

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args)
    if not question:
        await ctx.reply("Usage: /ask <question>")
        return
    await ctx.reply("🤔 Thinking (running locally)...")
    answer = await ai.generate(question)
    await ctx.reply(answer)

bot.run_polling()
```

> ✅ Works completely offline. Your data never leaves your computer.

---

## OpenRouter

**OpenRouter** — one API key, 100+ models, many completely free.

**Get Free API Key:** [openrouter.ai](https://openrouter.ai) → Sign up → Keys

**Free Models (no cost):**
- `meta-llama/llama-3-8b-instruct:free`
- `mistralai/mistral-7b-instruct:free`
- `google/gemma-2-9b-it:free`
- `qwen/qwen-2-7b-instruct:free`

```python
from markanm import Bot
from markanm.ai import AI

bot = Bot("mkbot_YOUR_TOKEN")

ai = AI(
    provider="openrouter",
    api_key="sk-or-v1-YOUR_OPENROUTER_KEY",
    model="meta-llama/llama-3-8b-instruct:free",  # 100% FREE
    system_prompt="You are a helpful assistant."
)

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args)
    if not question:
        await ctx.reply("Usage: /ask <question>")
        return
    answer = await ai.generate(question)
    await ctx.reply(answer)

bot.run_polling()
```

---

## Custom HTTP Endpoint

You can connect to **any AI service** — including your own server — by using `provider="custom"`.

**Your server must:**
- Accept `POST` requests with JSON body: `{"prompt": "...", "system": "...", "history": [...], "model": "..."}`
- Return JSON with one of: `text`, `content`, `response`, `output`, `result`, or `answer`

```python
from markanm.ai import AI

# Connect to your own AI server
ai = AI(
    provider="custom",
    base_url="https://my-ai-server.com/api/generate",
    api_key="my-secret-key",   # optional — sent as Bearer token
    model="my-model-v1",
)

# Example server that accepts this format (Python/FastAPI):
# @app.post("/api/generate")
# async def generate(req: Request):
#     body = await req.json()
#     prompt = body["prompt"]
#     response = my_model.generate(prompt)
#     return {"text": response}  ← must return "text" key
```

**Connect to a local AI service:**

```python
# If you're running a local AI service on port 5000:
ai = AI(
    provider="custom",
    base_url="http://localhost:5000/predict",
    model="my-local-model"
)
```

---

## Conversation Memory

By default, `ai.generate()` is **stateless** — it doesn't remember previous messages. Use `ai.chat()` for memory.

### `generate()` — Stateless (no memory)

```python
# Each call is independent — AI doesn't remember past messages
answer1 = await ai.generate("What is Python?")
answer2 = await ai.generate("What is it used for?")  # AI doesn't know "it" refers to Python
```

### `chat()` — Stateful (remembers conversation)

```python
# Each call remembers the entire previous conversation
answer1 = await ai.chat("What is Python?")
answer2 = await ai.chat("What is it used for?")  # AI knows "it" = Python ✅
answer3 = await ai.chat("Give me a simple example")  # Full context retained ✅
```

### Reset Memory

```python
ai.reset()  # Clears all conversation history
```

---

## Multi-Turn Chat

The most common pattern: each user gets their own AI instance with independent memory.

```python
import os
from markanm import Bot
from markanm.ai import AI

bot = Bot(os.environ["MARKANM_BOT_TOKEN"])

# Dictionary to store one AI instance per user
user_sessions = {}  # user_id → AI instance

def get_session(user_id: int) -> AI:
    """Get or create an AI session for a user."""
    if user_id not in user_sessions:
        user_sessions[user_id] = AI(
            provider="groq",
            api_key=os.environ["GROQ_API_KEY"],
            model="llama3-8b-8192",
            system_prompt=(
                "You are a friendly and helpful assistant named Aria. "
                "Remember what the user tells you throughout the conversation."
            )
        )
    return user_sessions[user_id]

@bot.on("command.received")
async def chat_handler(evt):
    text = evt.payload.get("text", "").strip()
    user_id = evt.payload.get("user", {}).get("id")

    if not text or text.startswith("/") or not user_id:
        return

    ai = get_session(user_id)
    reply = await ai.chat(text)  # ← remembers all previous messages
    await evt.reply(reply)

@bot.command("reset")
async def reset_cmd(ctx):
    """User can clear their chat history."""
    user_id = ctx.user.id
    if user_id in user_sessions:
        user_sessions[user_id].reset()
    await ctx.reply("🧹 Chat history cleared! Starting fresh.")

@bot.command("history")
async def history_cmd(ctx):
    """Show how many messages are in memory."""
    user_id = ctx.user.id
    if user_id in user_sessions:
        count = len(user_sessions[user_id]._history)
        await ctx.reply(f"🧠 I remember {count} messages in our conversation.")
    else:
        await ctx.reply("No conversation history yet. Start chatting!")

bot.run_polling()
```

---

## Bot Personas & Custom Training

You don't need fine-tuning to make your bot behave a specific way. The **system prompt** is your training tool.

### Customer Support Bot

```python
ai = AI(
    provider="groq",
    api_key="gsk_...",
    system_prompt="""You are Riya, the official support agent for ShopIndia.

RULES (follow strictly):
1. Only answer questions related to ShopIndia orders, products, and policies.
2. If asked about anything else, say: "I can only help with ShopIndia-related questions."
3. Always be polite, professional, and empathetic.
4. Never make up order details — ask the user to provide their Order ID.
5. If you cannot resolve an issue, say: "I'll escalate this to our team."

POLICIES:
- Shipping: Free above ₹500, ₹49 for orders below.
- Returns: 7-day no-questions-asked return policy.
- Refunds: Processed within 5–7 business days.
- Support hours: Mon–Sat, 9am–6pm IST.

FORMAT: Keep replies under 3 sentences unless listing policies."""
)
```

### Educational Tutor Bot

```python
ai = AI(
    provider="gemini",
    api_key="AIza...",
    system_prompt="""You are a patient, encouraging tutor for Class 10 students.

TEACHING STYLE:
1. Always explain in simple, clear language.
2. Use real-world examples and analogies.
3. Break complex topics into small steps.
4. After explaining, ask: "Does this make sense? Shall I give an example?"
5. When a student is wrong, gently correct them.
6. Use emojis occasionally to keep it friendly 😊

SUBJECTS: Math, Science, English, Social Studies, Hindi."""
)
```

### Fitness Coach Bot

```python
ai = AI(
    provider="openai",
    api_key="sk-...",
    model="gpt-4o-mini",
    system_prompt="""You are FitBot, a certified fitness coach.

CAPABILITIES:
- Create personalized workout plans based on user's goals
- Give nutrition advice
- Track progress when users share updates
- Motivate users with encouragement

IMPORTANT:
- Always recommend consulting a doctor before starting new exercise routines
- Do not recommend specific medications or supplements
- Keep workout advice safe and beginner-friendly unless user specifies advanced level

FORMAT: Use bullet points for exercises. Always specify: sets, reps, and rest time."""
)
```

### Hindi/Regional Language Bot

```python
ai = AI(
    provider="sarvam",
    api_key="sk_...",
    model="sarvam-105b",
    system_prompt="""आप एक सहायक बॉट हैं। 

नियम:
1. अगर उपयोगकर्ता हिंदी में लिखे, तो हिंदी में उत्तर दें।
2. अगर English में लिखे, तो English में उत्तर दें।
3. सरल और स्पष्ट भाषा का उपयोग करें।
4. हमेशा विनम्र और सहायक रहें।"""
)
```

---

## RAG — Custom Knowledge Base

RAG (Retrieval Augmented Generation) = inject your own knowledge into AI prompts.

### Simple Keyword-Based RAG

```python
from markanm import Bot
from markanm.ai import AI

bot = Bot("mkbot_YOUR_TOKEN")
ai = AI(provider="groq", api_key="gsk_...",
        system_prompt="You are a helpful support agent. Only answer using the provided context.")

# Your custom knowledge base
KNOWLEDGE = {
    "price": "Our plans: Free (5GB storage), Pro ₹299/month (50GB), Business ₹999/month (unlimited).",
    "refund": "We offer a 30-day money-back guarantee. Refunds process in 5–7 business days.",
    "support": "Email: help@myapp.com | WhatsApp: +91-9999999999 | Hours: Mon–Fri, 10am–6pm IST.",
    "features": "MyApp features: cloud storage, file sharing, team collaboration, version history.",
    "install": "Download the app from myapp.com/download. Supports Windows, Mac, Linux, Android, iOS.",
    "login": "Visit myapp.com and click 'Login'. Use your email and password, or 'Continue with Google'.",
    "password": "To reset your password, click 'Forgot Password' on the login page. Check your email.",
    "upgrade": "To upgrade, go to Settings → Billing → Choose Plan → Pay securely via Razorpay/Stripe.",
}

def find_relevant_facts(question: str) -> str:
    """Find knowledge base entries relevant to the question."""
    q = question.lower()
    relevant = []

    keyword_map = {
        "price": ["price", "cost", "plan", "subscription", "how much", "fee", "pay"],
        "refund": ["refund", "money back", "cancel", "return"],
        "support": ["support", "contact", "help", "email", "call", "reach"],
        "features": ["feature", "what can", "what does", "capability", "function"],
        "install": ["install", "download", "setup", "how to get"],
        "login": ["login", "log in", "sign in", "access"],
        "password": ["password", "forgot", "reset", "can't login"],
        "upgrade": ["upgrade", "change plan", "switch plan", "premium"],
    }

    for key, keywords in keyword_map.items():
        if any(kw in q for kw in keywords):
            relevant.append(KNOWLEDGE[key])

    return "\n".join(relevant)

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args).strip()
    if not question:
        await ctx.reply("Usage: /ask <question>\nExample: /ask what is the price?")
        return

    # Find relevant knowledge
    context = find_relevant_facts(question)

    if context:
        prompt = f"Context:\n{context}\n\nUser question: {question}\n\nAnswer based only on the context above."
    else:
        prompt = f"{question}\n\nNote: Answer helpfully but mention this may be outside your knowledge base."

    answer = await ai.generate(prompt)
    await ctx.reply(answer)

bot.run_polling()
```

---

## Persistent Memory

Save conversation history to a file or database so the bot remembers users across restarts.

### Save to JSON File

```python
import json
import os
from markanm import Bot
from markanm.ai import AI

bot = Bot("mkbot_YOUR_TOKEN")

MEMORY_FILE = "bot_memory.json"
MAX_HISTORY = 20  # Keep last 20 messages per user

def load_all_memories() -> dict:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_all_memories(data: dict):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user_history(user_id: str) -> list:
    return load_all_memories().get(user_id, [])

def save_user_history(user_id: str, history: list):
    data = load_all_memories()
    data[user_id] = history[-MAX_HISTORY:]  # Trim to limit
    save_all_memories(data)

@bot.on("command.received")
async def persistent_chat(evt):
    text = evt.payload.get("text", "").strip()
    user_id = str(evt.payload.get("user", {}).get("id", ""))

    if not text or not user_id or text.startswith("/"):
        return

    # Load this user's history from file
    ai = AI(provider="groq", api_key=os.environ["GROQ_API_KEY"])
    ai._history = get_user_history(user_id)

    # Chat (uses history)
    reply = await ai.chat(text)

    # Save updated history back to file
    save_user_history(user_id, ai._history)

    await evt.reply(reply)

@bot.command("reset")
async def reset(ctx):
    user_id = str(ctx.user.id)
    data = load_all_memories()
    if user_id in data:
        del data[user_id]
        save_all_memories(data)
    await ctx.reply("🧹 Memory cleared!")

bot.run_polling()
```

---

## Interactive Forms & Multi-Step Flows

Collect structured data from users step-by-step, like a form or wizard.

```python
import os
from markanm import Bot
from markanm.ai import AI

bot = Bot("mkbot_YOUR_TOKEN")

# State storage: user_id → {"step": "...", "data": {...}}
user_states = {}

def set_state(user_id, step, data=None):
    user_states[user_id] = {"step": step, "data": data or {}}

def get_state(user_id):
    return user_states.get(user_id)

def clear_state(user_id):
    user_states.pop(user_id, None)

# ── Step 1: Start the form ─────────────────────────────────────
@bot.command("register")
async def register_start(ctx):
    set_state(ctx.user.id, "ask_name")
    await ctx.reply("📝 Registration Form (Step 1/4)\n\nWhat is your full name?")

# ── Steps 2–4: Handle form input ──────────────────────────────
@bot.on("command.received")
async def handle_form(evt):
    text = evt.payload.get("text", "").strip()
    user_id = evt.payload.get("user", {}).get("id")

    if not user_id or not text or text.startswith("/"):
        return

    state = get_state(user_id)
    if not state:
        return  # User isn't in a form flow

    step = state["step"]
    data = state["data"]

    if step == "ask_name":
        if len(text) < 2:
            await evt.reply("❌ Please enter a valid name.")
            return
        data["name"] = text
        set_state(user_id, "ask_email", data)
        await evt.reply(f"✅ Name: {text}\n\n📝 Step 2/4 — What is your email address?")

    elif step == "ask_email":
        if "@" not in text or "." not in text:
            await evt.reply("❌ Please enter a valid email address (e.g. name@example.com).")
            return
        data["email"] = text
        set_state(user_id, "ask_phone", data)
        await evt.reply(f"✅ Email: {text}\n\n📝 Step 3/4 — What is your phone number?")

    elif step == "ask_phone":
        if not text.isdigit() or len(text) < 10:
            await evt.reply("❌ Please enter a valid 10-digit phone number.")
            return
        data["phone"] = text
        set_state(user_id, "confirm", data)
        await evt.reply(
            f"📋 Step 4/4 — Please confirm your details:\n\n"
            f"👤 Name:  {data['name']}\n"
            f"📧 Email: {data['email']}\n"
            f"📞 Phone: {data['phone']}\n\n"
            f"Type YES to confirm or NO to cancel."
        )

    elif step == "confirm":
        if text.upper() == "YES":
            # Process the registration
            clear_state(user_id)
            await evt.reply(
                f"🎉 Registration successful!\n\n"
                f"Welcome, {data['name']}!\n"
                f"We'll send details to {data['email']}."
            )
            # Here you would save to a database
        elif text.upper() == "NO":
            clear_state(user_id)
            await evt.reply("❌ Registration cancelled. Type /register to start again.")
        else:
            await evt.reply("Please type YES to confirm or NO to cancel.")

@bot.command("cancel")
async def cancel_form(ctx):
    clear_state(ctx.user.id)
    await ctx.reply("❌ Form cancelled.")

bot.run_polling()
```

---

## Per-User State Management

A reusable pattern for tracking different states per user:

```python
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

class UserStep(Enum):
    IDLE = auto()
    WAITING_NAME = auto()
    WAITING_CHOICE = auto()
    WAITING_CONFIRM = auto()

@dataclass
class UserState:
    step: UserStep = UserStep.IDLE
    data: Dict[str, Any] = field(default_factory=dict)

class StateManager:
    def __init__(self):
        self._states: Dict[int, UserState] = {}

    def get(self, user_id: int) -> UserState:
        if user_id not in self._states:
            self._states[user_id] = UserState()
        return self._states[user_id]

    def set_step(self, user_id: int, step: UserStep, **data):
        state = self.get(user_id)
        state.step = step
        state.data.update(data)

    def reset(self, user_id: int):
        self._states[user_id] = UserState()

    def is_idle(self, user_id: int) -> bool:
        return self.get(user_id).step == UserStep.IDLE

states = StateManager()

@bot.command("start")
async def start_flow(ctx):
    states.set_step(ctx.user.id, UserStep.WAITING_NAME)
    await ctx.reply("What's your name?")

@bot.on("command.received")
async def flow_handler(evt):
    text = evt.payload.get("text", "").strip()
    user_id = evt.payload.get("user", {}).get("id")
    if not user_id or not text or text.startswith("/"):
        return

    state = states.get(user_id)

    if state.step == UserStep.IDLE:
        return

    if state.step == UserStep.WAITING_NAME:
        states.set_step(user_id, UserStep.WAITING_CHOICE, name=text)
        await evt.reply(f"Hi {text}! Choose: 1) Option A or 2) Option B")

    elif state.step == UserStep.WAITING_CHOICE:
        if text not in ["1", "2", "Option A", "Option B"]:
            await evt.reply("Please choose 1 or 2.")
            return
        states.set_step(user_id, UserStep.IDLE)
        name = state.data.get("name", "friend")
        await evt.reply(f"✅ {name} chose {text}. Done!")
        states.reset(user_id)
```

---

## Webhooks (Production)

**Webhooks** are for deploying your bot to a **real server**. Instead of polling, MarkanM pushes events to your server instantly.

### Requirements

- A public HTTPS URL (e.g. `https://mybot.railway.app/webhook`)
- A server framework (FastAPI, Flask, Django, etc.)

### FastAPI Webhook Server

```python
# webhook_bot.py
import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from markanm import Bot
from markanm.ai import AI

app = FastAPI(title="My MarkanM Bot")

# Initialize bot with webhook_secret for signature verification
bot = Bot(
    token=os.environ["MARKANM_BOT_TOKEN"],
    webhook_secret=os.environ["MARKANM_WEBHOOK_SECRET"]  # from Developer Portal
)

ai = AI(
    provider="groq",
    api_key=os.environ["GROQ_API_KEY"],
    model="llama3-8b-8192"
)

# ── Register your handlers ─────────────────────────────────────

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args)
    if not question:
        await ctx.reply("Usage: /ask <question>")
        return
    answer = await ai.generate(question)
    await ctx.reply(answer)

@bot.on("command.received")
async def on_message(evt):
    text = evt.payload.get("text", "").strip()
    if not text or text.startswith("/"):
        return
    reply = await ai.generate(text)
    await evt.reply(reply)

# ── Webhook endpoint ───────────────────────────────────────────

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-MarkanM-Signature", "")

    try:
        # Verify signature & dispatch to handlers
        event = await bot.handle_webhook(body.decode("utf-8"), signature)
        return {"ok": True, "event_id": event.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "bot": "running"}

# ── Run ────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
```

**Deploy:**

```bash
# Install deps
pip install markanm httpx fastapi uvicorn

# Set environment variables
export MARKANM_BOT_TOKEN="mkbot_..."
export MARKANM_WEBHOOK_SECRET="whsec_..."
export GROQ_API_KEY="gsk_..."

# Run
python webhook_bot.py
```

### Flask Webhook Server

```python
import os
from flask import Flask, request, jsonify
from markanm import Bot
from markanm.ai import AI
import asyncio

app = Flask(__name__)

bot = Bot(
    token=os.environ["MARKANM_BOT_TOKEN"],
    webhook_secret=os.environ["MARKANM_WEBHOOK_SECRET"]
)
ai = AI(provider="groq", api_key=os.environ["GROQ_API_KEY"])

@bot.command("ask")
async def ask(ctx):
    answer = await ai.generate(" ".join(ctx.args))
    await ctx.reply(answer)

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_data(as_text=True)
    signature = request.headers.get("X-MarkanM-Signature", "")

    async def process():
        await bot.handle_webhook(body, signature)

    asyncio.run(process())
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## Polling (Development)

Polling is for **local development** — no server needed.

```python
bot.run_polling()                    # Default: polls every 2 seconds
bot.run_polling(interval=1.0)        # Poll every 1 second (faster)
bot.run_polling(interval=5.0)        # Poll every 5 seconds (lighter)
bot.run(mode="polling", interval=2)  # Alternative syntax
```

**How it works:**

1. Every `interval` seconds, your bot calls `POST /api/bot/v1/polling`
2. The server returns any pending events
3. Your handlers are called for each event
4. The cycle repeats

> ✅ Use polling for local development.
> 🚀 Switch to webhooks for production.

---

## Error Handling

### Handle AI Errors Gracefully

```python
from markanm.exceptions import MarkanMError, MarkanMAPIError, MarkanMAuthError

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args)
    if not question:
        await ctx.reply("Usage: /ask <question>")
        return

    try:
        answer = await ai.generate(question)
        await ctx.reply(answer)

    except MarkanMAuthError:
        await ctx.reply("❌ AI authentication failed. Check your API key.")

    except MarkanMAPIError as e:
        await ctx.reply(f"❌ AI service error: {e}")

    except MarkanMError as e:
        await ctx.reply(f"❌ Error: {e.message}")

    except Exception as e:
        await ctx.reply("❌ An unexpected error occurred. Please try again.")
        print(f"Unexpected error: {e}")
```

### Retry on Failure

```python
import asyncio

async def generate_with_retry(ai, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await ai.generate(prompt)
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                await asyncio.sleep(wait)
            else:
                raise e

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args)
    try:
        answer = await generate_with_retry(ai, question)
        await ctx.reply(answer)
    except Exception:
        await ctx.reply("❌ Failed after 3 attempts. Please try again later.")
```

### Validate User Input

```python
@bot.command("calculate")
async def calculate(ctx):
    if not ctx.args:
        await ctx.reply("❌ Please provide an expression.\nUsage: /calculate 2 + 3")
        return

    expression = " ".join(ctx.args)

    # Only allow safe characters
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        await ctx.reply("❌ Invalid characters. Only use numbers and + - * / ( )")
        return

    try:
        result = eval(expression)  # Safe since we validated input
        await ctx.reply(f"🧮 {expression} = **{result}**")
    except ZeroDivisionError:
        await ctx.reply("❌ Cannot divide by zero!")
    except Exception:
        await ctx.reply("❌ Invalid expression.")
```

---

## Complete Bot Examples

### Example 1: Full AI Assistant Bot

```python
# ai_assistant.py — A complete, production-ready AI bot
import os
from markanm import Bot
from markanm.ai import AI

bot = Bot(os.environ["MARKANM_BOT_TOKEN"])

user_sessions = {}  # user_id → AI instance

def get_ai(user_id: int) -> AI:
    if user_id not in user_sessions:
        user_sessions[user_id] = AI(
            provider="groq",
            api_key=os.environ["GROQ_API_KEY"],
            model="llama3-8b-8192",
            system_prompt="You are Aria, a friendly and intelligent assistant."
        )
    return user_sessions[user_id]

@bot.command("start")
async def start(ctx):
    await ctx.reply(
        f"👋 Hello {ctx.user.display_name}!\n\n"
        "I'm Aria, your AI assistant powered by LLaMA 3.\n\n"
        "Commands:\n"
        "/ask <question> — Ask me anything\n"
        "/chat — Start a conversation (I'll remember context!)\n"
        "/reset — Clear conversation history\n"
        "/help — Show this message"
    )

@bot.command("ask")
async def ask(ctx):
    question = " ".join(ctx.args).strip()
    if not question:
        await ctx.reply("Usage: /ask <question>\nExample: /ask what is machine learning?")
        return
    await ctx.reply("🤔 Thinking...")
    ai = AI(provider="groq", api_key=os.environ["GROQ_API_KEY"], model="llama3-8b-8192")
    answer = await ai.generate(question)
    await ctx.reply(f"💡 {answer}")

@bot.command("reset")
async def reset(ctx):
    user_id = ctx.user.id
    if user_id in user_sessions:
        user_sessions[user_id].reset()
    await ctx.reply("🧹 Conversation history cleared!")

@bot.command("help")
async def help_cmd(ctx):
    await ctx.reply(
        "🤖 **Aria AI Bot — Commands:**\n\n"
        "/start — Welcome message\n"
        "/ask <q> — One-shot question (no memory)\n"
        "/reset  — Clear my memory of you\n"
        "/help   — Show this message\n\n"
        "💬 Or just send any message to chat with me!"
    )

@bot.on("command.received")
async def chat(evt):
    text = evt.payload.get("text", "").strip()
    user_id = evt.payload.get("user", {}).get("id")
    if not text or not user_id or text.startswith("/"):
        return
    ai = get_ai(user_id)
    reply = await ai.chat(text)
    await evt.reply(reply)

bot.run_polling()
```

---

### Example 2: Customer Support Bot

```python
# support_bot.py
import os
from markanm import Bot
from markanm.ai import AI

bot = Bot(os.environ["MARKANM_BOT_TOKEN"])

ai = AI(
    provider="sarvam",
    api_key=os.environ["SARVAM_API_KEY"],
    model="sarvam-105b",
    system_prompt="""You are a customer support agent for MyShop India.
Answer only about: orders, products, shipping, returns, and payments.
If asked anything else: "I can only help with MyShop queries. Please contact us at help@myshop.in"
Language: Respond in the same language the customer uses (Hindi/English/etc.)
Tone: Professional, empathetic, helpful.

Policies:
- Shipping: Free above ₹499, ₹49 below. 2-5 business days.
- Returns: 7-day return. Initiate via /return command.
- Refunds: 5-7 business days after return received.
- COD available on orders below ₹10,000."""
)

@bot.command("start")
async def start(ctx):
    await ctx.reply(
        f"🛍️ Welcome to MyShop Support!\n\n"
        f"Hi {ctx.user.display_name}! I'm here to help.\n\n"
        "How can I assist you today?\n\n"
        "Commands:\n"
        "/order <ID> — Track your order\n"
        "/return — Start a return\n"
        "/help — See all options"
    )

@bot.command("order")
async def track_order(ctx):
    if not ctx.args:
        await ctx.reply("Please provide your Order ID.\nUsage: /order ORD123456")
        return
    order_id = ctx.args[0].upper()
    # In a real bot, query your database here
    await ctx.reply(
        f"📦 Order Status: {order_id}\n\n"
        "Status: In Transit 🚚\n"
        "Expected: 2–3 business days\n\n"
        "For more details, email orders@myshop.in"
    )

@bot.command("return")
async def start_return(ctx):
    await ctx.reply(
        "📦 Return Policy:\n\n"
        "✅ 7-day return window\n"
        "✅ Free pick-up for defective items\n"
        "✅ Refund in 5–7 business days\n\n"
        "To initiate: Email returns@myshop.in with:\n"
        "- Order ID\n- Reason for return\n- Photos (if damaged)"
    )

@bot.on("command.received")
async def support_chat(evt):
    text = evt.payload.get("text", "").strip()
    if not text or text.startswith("/"):
        return
    reply = await ai.generate(text)
    await evt.reply(reply)

bot.run_polling()
```

---

### Example 3: Quiz Bot

```python
# quiz_bot.py
import os, random
from markanm import Bot

bot = Bot(os.environ["MARKANM_BOT_TOKEN"])

QUESTIONS = [
    {"q": "What is the capital of India?",         "a": "new delhi", "hint": "It's in the north."},
    {"q": "Who invented the telephone?",            "a": "alexander graham bell", "hint": "Scottish-American inventor."},
    {"q": "What is 15 × 15?",                      "a": "225", "hint": "It's between 200 and 250."},
    {"q": "What is the largest planet in our solar system?", "a": "jupiter", "hint": "It's a gas giant."},
    {"q": "Who wrote the Mahabharata?",             "a": "ved vyasa", "hint": "Ancient Indian sage."},
    {"q": "What is the chemical symbol for water?", "a": "h2o", "hint": "Hydrogen and Oxygen."},
    {"q": "In what year did India gain independence?", "a": "1947", "hint": "After World War II."},
    {"q": "Who is known as the Father of the Nation in India?", "a": "mahatma gandhi", "hint": "Led the freedom movement."},
]

quiz_state = {}  # user_id → {"question": ..., "attempts": 0, "score": 0}

@bot.command("quiz")
async def start_quiz(ctx):
    user_id = ctx.user.id
    q = random.choice(QUESTIONS)
    quiz_state[user_id] = {"question": q, "attempts": 0, "score": quiz_state.get(user_id, {}).get("score", 0)}
    await ctx.reply(f"🎯 Question:\n\n{q['q']}\n\nType your answer! (or /hint for a clue, /skip to skip)")

@bot.command("hint")
async def hint(ctx):
    user_id = ctx.user.id
    state = quiz_state.get(user_id)
    if not state:
        await ctx.reply("Start a quiz first with /quiz")
        return
    await ctx.reply(f"💡 Hint: {state['question']['hint']}")

@bot.command("skip")
async def skip(ctx):
    user_id = ctx.user.id
    state = quiz_state.get(user_id)
    if not state:
        await ctx.reply("Start a quiz first with /quiz")
        return
    ans = state['question']['a'].title()
    await ctx.reply(f"⏭️ Skipped!\nThe answer was: **{ans}**\n\nType /quiz for next question!")
    del quiz_state[user_id]

@bot.command("score")
async def score(ctx):
    state = quiz_state.get(ctx.user.id, {})
    score = state.get("score", 0)
    await ctx.reply(f"🏆 Your score: {score} points!")

@bot.on("command.received")
async def check_answer(evt):
    text = evt.payload.get("text", "").strip().lower()
    user_id = evt.payload.get("user", {}).get("id")
    if not user_id or not text or text.startswith("/"):
        return

    state = quiz_state.get(user_id)
    if not state:
        return

    state["attempts"] += 1
    correct = state["question"]["a"].lower()

    if text == correct or correct in text:
        pts = max(10 - state["attempts"] * 2, 1)
        state["score"] = state.get("score", 0) + pts
        await evt.reply(f"🎉 Correct! +{pts} points\n\n🏆 Total score: {state['score']}\n\nType /quiz for next question!")
        del quiz_state[user_id]
    elif state["attempts"] >= 3:
        ans = state["question"]["a"].title()
        await evt.reply(f"❌ Out of attempts!\nThe answer was: **{ans}**\n\nType /quiz to try another!")
        del quiz_state[user_id]
    else:
        remaining = 3 - state["attempts"]
        await evt.reply(f"❌ Wrong! {remaining} attempt(s) remaining.\nTry again or type /hint for a clue.")

bot.run_polling()
```

---

## Deploying to Production

### Option 1: Railway.app (Recommended — Free Tier)

```bash
# 1. Create a Railway account at railway.app
# 2. New Project → Deploy from GitHub

# Create requirements.txt
cat > requirements.txt << EOF
markanm>=0.1.0
httpx>=0.24.0
fastapi>=0.104.0
uvicorn>=0.24.0
EOF

# Create Procfile
echo "web: uvicorn webhook_bot:app --host 0.0.0.0 --port \$PORT" > Procfile

# Set environment variables in Railway dashboard:
# MARKANM_BOT_TOKEN = mkbot_...
# MARKANM_WEBHOOK_SECRET = whsec_...
# GROQ_API_KEY = gsk_...
```

### Option 2: Render.com (Free Tier)

```yaml
# render.yaml
services:
  - type: web
    name: my-markanm-bot
    env: python
    startCommand: uvicorn webhook_bot:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: MARKANM_BOT_TOKEN
        sync: false
      - key: GROQ_API_KEY
        sync: false
```

### Option 3: VPS / DigitalOcean

```bash
# On your server:
git clone https://github.com/your-username/my-bot.git
cd my-bot
pip install -r requirements.txt

# Run with systemd (auto-restart on crash)
cat > /etc/systemd/system/markanm-bot.service << EOF
[Unit]
Description=MarkanM Bot
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/my-bot
Environment=MARKANM_BOT_TOKEN=mkbot_...
Environment=GROQ_API_KEY=gsk_...
ExecStart=/usr/bin/python3 webhook_bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl enable markanm-bot
systemctl start markanm-bot
systemctl status markanm-bot
```

### Option 4: Keep Polling Running 24/7 (no server needed)

```bash
# Install screen or tmux to keep it running after you disconnect
sudo apt install screen
screen -S mybot
python main.py
# Press Ctrl+A, then D to detach
# Bot keeps running in background!

# To re-attach later:
screen -r mybot
```

---

## API Reference

### `Bot` class

```python
Bot(
    token: str,                         # Required. Bot token from Developer Portal.
    base_url: str = "https://chat.markanm.com/api/bot/v1",
    timeout: float = 30.0,              # HTTP request timeout in seconds.
    webhook_secret: Optional[str] = None # Required for webhook verification.
)
```

| Method | Description |
|--------|-------------|
| `@bot.command(name)` | Register a slash command handler |
| `@bot.on(event_type)` | Register an event listener |
| `bot.run_polling(interval=2.0)` | Start development polling loop |
| `bot.run(mode="polling")` | Alias for run_polling |
| `await bot.send_message(room_id, text)` | Send message to a room |
| `await bot.get_room(room_id)` | Fetch room details |
| `await bot.get_room_members(room_id)` | Fetch room members |
| `await bot.react(message_id, emoji)` | React to a message |
| `await bot.delete_message(message_id)` | Delete a message |
| `await bot.handle_webhook(body, signature)` | Verify + process webhook |

---

### `AI` class

```python
AI(
    provider: str = "openai",          # AI provider name
    api_key: str = "",                 # API key (or list with one key)
    model: Optional[str] = None,       # Model name (uses provider default if not set)
    base_url: Optional[str] = None,    # Override API base URL
    system_prompt: str = "...",        # Bot's personality/instructions
    timeout: float = 60.0,            # Request timeout in seconds
)
```

| Method | Description |
|--------|-------------|
| `await ai.generate(prompt, system_prompt=None)` | Stateless generation (no memory) |
| `await ai.chat(user_message)` | Multi-turn chat with memory |
| `ai.reset()` | Clear conversation history |
| `ai._history` | Access/set raw conversation history |

---

### Exception Types

| Exception | When it's raised |
|-----------|-----------------|
| `MarkanMError` | Base error class |
| `MarkanMAPIError` | Non-2xx HTTP response from API |
| `MarkanMAuthError` | 401 — Invalid bot token or API key |
| `MarkanMPermissionError` | 403 — Bot lacks permission |
| `MarkanMNotFoundError` | 404 — Resource not found |
| `MarkanMRateLimitError` | 429 — Too many requests |
| `MarkanMWebhookError` | Invalid webhook signature |

```python
from markanm.exceptions import (
    MarkanMError,
    MarkanMAPIError,
    MarkanMAuthError,
    MarkanMPermissionError,
    MarkanMNotFoundError,
    MarkanMRateLimitError,
)
```

---

## Changelog

### v0.1.0a1 (current)
- ✅ Core `Bot` class with command and event routing
- ✅ Long-polling development mode
- ✅ Webhook support with HMAC-SHA256 signature verification
- ✅ `AI` class with 13 provider integrations
- ✅ Multi-turn `chat()` with automatic conversation memory
- ✅ `CommandContext` and `Event` with `.reply()` method
- ✅ Async/sync handler support
- ✅ Automatic `httpx`/`urllib` fallback

### Roadmap
- 📋 v0.2.0 — Message reactions, room management, file uploads
- 📋 v0.3.0 — Interactive card messages (buttons, menus)
- 📋 v1.0.0 — Stable API with full test coverage

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ by the [MarkanM Team](https://chat.markanm.com)**

[🌐 Website](https://chat.markanm.com) · [👨‍💻 Developer Portal](https://chat.markanm.com/developers) · [📖 Docs](https://chat.markanm.com/developers/docs)

</div>
