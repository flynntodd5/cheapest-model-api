from dataclasses import dataclass
from typing import Optional

@dataclass
class Price:
    model: str
    provider: str
    input_per_1m: float
    output_per_1m: float
    kind: str = 'official'

PRICES = [
    Price('gpt-4o-mini', 'provider-a', 0.15, 0.60, 'official'),
    Price('gpt-4o-mini', 'relay-b', 0.10, 0.45, 'relay'),
    Price('deepseek-chat', 'provider-c', 0.14, 0.28, 'official'),
    Price('deepseek-chat', 'relay-d', 0.08, 0.20, 'relay'),
    Price('llama-3.1-70b', 'host-e', 0.59, 0.79, 'inference'),
]

def estimate_cost(p: Price, input_tokens: int, output_tokens: int) -> float:
    return p.input_per_1m * input_tokens / 1_000_000 + p.output_per_1m * output_tokens / 1_000_000

def cheapest(model: str, input_tokens: int = 1000, output_tokens: int = 500) -> Optional[Price]:
    candidates = [p for p in PRICES if p.model == model]
    if not candidates:
        return None
    return min(candidates, key=lambda p: estimate_cost(p, input_tokens, output_tokens))

def main() -> None:
    models = sorted({p.model for p in PRICES})
    print('Available models:', ', '.join(models))
    model = input('Model: ').strip()
    p = cheapest(model)
    if p is None:
        print(f'No listed price for {model}')
        return
    cost = estimate_cost(p, 1000, 500)
    print(f'Cheapest: {p.provider} ({p.kind})')
    print(f'Input: ${p.input_per_1m}/1M, Output: ${p.output_per_1m}/1M')
    print(f'Estimated cost for 1k input + 500 output: ${cost:.6f}')

if __name__ == '__main__':
    main()
