# MarkanM Python SDK

Python SDK for the MarkanM bot API: bot identity, room messages, command/event dispatch, polling, signed webhooks, and an OpenAI-compatible AI helper. The server currently exposes `GET /me`, `POST /rooms/{roomId}/messages`, and `POST /polling` under `/api/bot/v1`; methods for other platform features are not advertised until the backend supports them.

## Requirements and install

- Python 3.9 or newer (the SDK uses `asyncio.to_thread`).
- `httpx` is installed with the package; it provides async HTTP and TLS handling.

```bash
python -m pip install markanm
```

On Kali Linux and other Debian based distributions, system Python may be externally managed (PEP 668). Do not use `sudo pip` or force `--break-system-packages`. Create a virtual environment:

```bash
sudo apt update
sudo apt install python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install markanm
```

If `venv` reports that `ensurepip` is unavailable, install the matching `python3-venv` package for your Kali Python version, then recreate the environment. Activate `.venv` in each new shell before running the bot. Use the system package manager for OS packages; avoid `sudo pip`.

## Quick start: polling bot

Create a bot and copy its token from the MarkanM developer portal. Keep the token in an environment variable:

```bash
export MARKANM_BOT_TOKEN="mkbot_..."
```

```python
import os
from markanm import Bot

bot = Bot(os.environ["MARKANM_BOT_TOKEN"])

@bot.command("hello")
async def hello(ctx):
    await ctx.reply(f"Hello, {ctx.user.display_name or 'there'}!")

@bot.on("command.received")
async def log_command(event):
    print(event.id, event.type)

bot.run_polling(interval=2.0)
```

Run `python bot.py`. Polling is intended for local development and simple deployments. Since the server marks fetched events as delivered before your handlers finish, keep handlers fast and make side effects safe to repeat. For hosted production bots, configure a webhook.

## API methods

```python
profile = await bot.get_me()
result = await bot.send_message(room_id="123", text="Hi")
await bot.poll_once()  # fetch one batch and dispatch it
bot.stop()             # request run_polling() to stop
```

`send_message` accepts an optional `card` dictionary. The current backend stores card content as a formatted text message; it does not yet expose interactive button callbacks. `CommandContext` provides `command`, `text`, `args`, `user`, `room`, `room_id`, `message`, and `await ctx.reply(text)`.

`@bot.on("event.type")` registers event listeners. Handlers may be synchronous or `async def`. Handler errors are logged and do not stop polling. `Event` exposes `id`, `type`, `timestamp`, `payload`, and `raw_data`.

## Webhooks

The webhook signature is `X-MarkanM-Signature: t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`, computed over `timestamp + "." + exact_raw_body` with the bot webhook secret. Preserve the raw request bytes before JSON parsing and pass the exact body to the SDK:

```python
event = await bot.handle_webhook(raw_body, request.headers["X-MarkanM-Signature"])
```

The default accepted timestamp drift is five minutes. Webhook event formats follow the same `Event` model as polling.

## AI helper

The `AI` helper currently supports OpenAI chat completions (or an OpenAI compatible endpoint), not the 13 providers claimed in older README text:

```python
from markanm import AI

ai = AI(api_key=os.environ["OPENAI_API_KEY"], model="gpt-4o-mini")
answer = await ai.chat("Suggest a greeting")  # keeps in-memory conversation history
ai.reset()
```

AI calls use your provider credentials directly and are billed by that provider. Do not put provider keys in client side code.

## Errors and network troubleshooting

All SDK exceptions derive from `MarkanMError`. API errors include `status_code`, `error_code`, and optional `request_id`; rate limit errors also expose `retry_after`. TLS certificate verification remains enabled. On Kali, install/update the OS CA bundle (`sudo apt install ca-certificates && sudo update-ca-certificates`) instead of disabling certificate checks. Check system time, DNS, outbound HTTPS access, token validity, API base URL, and that the bot is active. For a self-hosted endpoint, pass `base_url="https://host.example/api/bot/v1"`.

```python
from markanm import MarkanMAPIError, MarkanMRateLimitError

try:
    await bot.send_message("123", "Hello")
except MarkanMRateLimitError as exc:
    print("Retry after", exc.retry_after)
except MarkanMAPIError as exc:
    print(exc.status_code, exc.error_code, exc.request_id)
```

## Publishing

From this directory, build with `python -m build`, inspect the wheel and sdist in `dist/`, then upload with `python -m twine upload dist/*`. Use a PyPI token or trusted publishing in CI; do not commit credentials. Version numbers must be unique on PyPI.

## License

MIT. See [LICENSE](LICENSE).
