from openai import OpenAI

from app.config.settings import settings
from app.core.llm.token_counter import format_usage_response
from app.config.logger import get_logger

logger = get_logger(__name__)

OPENCODE_BASE_URL = "https://opencode.ai/zen/v1"
MIN_MAX_TOKENS = 4096


def _get_client():
    if not settings.OPENCODE_API_KEY:
        raise ValueError("Missing OPENCODE_API_KEY")
    return OpenAI(
        api_key=settings.OPENCODE_API_KEY,
        base_url=OPENCODE_BASE_URL,
        timeout=180.0,
        max_retries=2
    )


def _resolve_max_tokens(max_tokens):
    return max(MIN_MAX_TOKENS, int(max_tokens or MIN_MAX_TOKENS))


def _extract_text(message):
    content = getattr(message, "content", None) or ""
    if isinstance(content, list):
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )
    if content:
        return content
    reasoning = getattr(message, "reasoning_content", None) or getattr(message, "reasoning", None)
    if reasoning:
        return f"[Reasoning output]\n{reasoning}"
    return ""


def _format_messages(messages: list) -> list:
    return [
        {
            "role": msg.role if hasattr(msg, "role") else msg["role"],
            "content": msg.content if hasattr(msg, "content") else msg["content"]
        }
        for msg in messages
    ]


def stream_response_opencode(model: str, messages: list, max_tokens: int = 1024, temperature: float = 1.0, top_p: float = 1.0, thinking: bool = True):
    client = _get_client()
    formatted_messages = _format_messages(messages)

    kwargs = {
        "model": model,
        "messages": formatted_messages,
        "max_tokens": _resolve_max_tokens(max_tokens),
        "temperature": temperature,
        "top_p": top_p,
        "stream": True
    }
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    if not thinking:
        kwargs["extra_body"] = {"thinking": {"type": "disabled"}}

    try:
        response_stream = client.chat.completions.create(**kwargs)
        for chunk in response_stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        logger.error(f"[OpenCode] Stream failed - {type(e).__name__}: {str(e)}")
        raise


def get_response_opencode(model: str, messages: list, max_tokens: int = 1024, temperature: float = 1.0, top_p: float = 1.0, thinking: bool = True):
    client = _get_client()
    formatted_messages = _format_messages(messages)

    kwargs = {
        "model": model,
        "messages": formatted_messages,
        "max_tokens": _resolve_max_tokens(max_tokens),
        "temperature": temperature,
        "top_p": top_p
    }
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    if not thinking:
        kwargs["extra_body"] = {"thinking": {"type": "disabled"}}

    try:
        response = client.chat.completions.create(**kwargs)
        text = _extract_text(response.choices[0].message)

        input_tokens = response.usage.prompt_tokens if response.usage else 0
        output_tokens = response.usage.completion_tokens if response.usage else 0
        usage = format_usage_response(input_tokens, output_tokens)

        return {"text": text, "model": model, "usage": usage}
    except Exception as e:
        logger.error(f"[OpenCode] API call failed - {type(e).__name__}: {str(e)}")
        raise
