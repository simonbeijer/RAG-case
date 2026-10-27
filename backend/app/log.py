from rich.console import Console
from rich.markup import escape
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage

def calc_cost(input_tokens:int, output_tokens: int, config: dict) -> float:
    """ Calculate token cost in $ """
    input_cost = input_tokens * config["input_price_per_m"] / 1_000_000
    output_cost = output_tokens * config["output_price_per_m"] / 1_000_000
    return input_cost + output_cost

def log_usage(input_tokens: int, output_tokens: int, seconds: float, config: dict) -> None:
    """ Print log row with rich package"""
    cost = calc_cost(input_tokens, output_tokens, config)
    Console().print(
        f"[dim]in: {input_tokens} | ut: {output_tokens} | ${cost:.6f} | {seconds:.2f} s[/dim]"
    )

def log_hits(hits: list[dict]) -> None:
    """Print url and score for every hit with rich package"""
    console = Console()
    for hit in hits:
        console.print(f"[dim]    {hit['url']} | {hit['score']:.3f}[/dim]")
        
        
def log_messages(messages: list[BaseMessage], seconds: float, config: dict) -> None:
    """Log last hit, message and summed tokens"""
    input_tokens = 0
    output_tokens = 0
    # Only messages after the latest question
    last_human = max(i for i, m in enumerate(messages) if isinstance(m, HumanMessage))
    for message in messages[last_human + 1:]:
        if isinstance(message, ToolMessage):
            log_hits(message.artifact)
        elif isinstance(message, AIMessage):
            for tool_call in message.tool_calls:
                Console().print(f"[dim]    sökfråga: {escape(tool_call['args']['query'])}[/dim]")
            input_tokens += message.usage_metadata["input_tokens"]
            output_tokens += message.usage_metadata["output_tokens"]
    if messages[-1].response_metadata.get("finish_reason") == "length":
        Console().print("[yellow]Varning: svaret klipptes av vid max_tokens[/yellow]")
    log_usage(input_tokens, output_tokens, seconds, config)