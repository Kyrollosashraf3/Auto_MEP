from anthropic import Anthropic
from app.config.settings import settings
from app.core.token_counter import format_usage_response
from app.core.logger import get_logger

logger = get_logger(__name__)

def stream_response_anthropic(model: str, messages: list, max_tokens: int, temperature: float, system: str = None):
    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY, timeout=120.0)
    
    system_content = system if system else ""
    system_parts = []
    filtered_messages = []
    
    for msg in messages:
        role = msg.role if hasattr(msg, "role") else msg.get("role")
        content = msg.content if hasattr(msg, "content") else msg.get("content")
        if role == "system":
            system_parts.append(content)
        else:
            filtered_messages.append({"role": role, "content": content})
    
    if system_parts:
        system_content = "\n\n".join(system_parts) if not system_content else system_content + "\n\n" + "\n\n".join(system_parts)
    
    params = {"model": model, "max_tokens": max_tokens, "temperature": temperature, "messages": filtered_messages}
    if system_content:
        params["system"] = system_content
    
    with client.messages.stream(**params) as stream:
        for event in stream:
            if event.type == "content_block_delta" and hasattr(event.delta, "text"):
                yield event.delta.text

def get_response_anthropic(model: str, messages: list, max_tokens: int, temperature: float, system: str = None):
    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY, timeout=120.0)

    system_content = system if system else ""
    system_parts = []
    filtered_messages = []
    
    for msg in messages:
        role = msg.role if hasattr(msg, "role") else msg.get("role")
        content = msg.content if hasattr(msg, "content") else msg.get("content")
        
        if role == "system":
            system_parts.append(content)
        else:
            filtered_messages.append({"role": role, "content": content})
    
    if system_parts:
        system_content = "\n\n".join(system_parts) if not system_content else system_content + "\n\n" + "\n\n".join(system_parts)

    try:
        params = {"model": model, "max_tokens": max_tokens, "temperature": temperature, "messages": filtered_messages}
        if system_content:
            params["system"] = system_content
        
        response = client.messages.create(**params)
        usage = format_usage_response(input_tokens=response.usage.input_tokens, output_tokens=response.usage.output_tokens)
        
        return {"text": response.content[0].text if response.content else "", "model": model, "usage": usage}
    except Exception as e:
        logger.error(f"[Anthropic] API call failed - {type(e).__name__}: {str(e)}")
        raise
