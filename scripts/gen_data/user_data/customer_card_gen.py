import random
from datetime import datetime, timedelta
import os

os.sys.path.append('scripts')
from util.utils import save_to_json

RAW_PATH = r"data\raw"

def generate_unique_numbers(output_length: int):
    numbers = set()
    while len(numbers) < output_length:
        num = random.randint(10**15, 10**16 - 1)
        numbers.add(num)

    return list(numbers)


def transform_numbers(numbers: list[int]) -> list[str]:

    return [' '.join(str(num)[i:i+4] for i in range(0, len(str(num)), 4)) for num in numbers]


def generate_expr_date() -> str:

    expr_date = (datetime.now().date() + timedelta(days=365 * 3)).strftime("%m/%y")

    return expr_date


def generate_cvvs(card_numbers: list[str]) -> list[int]:

    cvvs = []

    for i in range(len(card_numbers)+1):
        cvvs.append(random.randint(100, 999))

    return cvvs


def build_card(card_number: str, expr_date: str, cvv: int) -> dict:

    card = {
        "card_number": card_number,
        "cardholder_name": None,
        "expr_date": expr_date,
        "cvv": cvv
    }

    return card


def generate_cards(output_length: int):
    card_numbers = transform_numbers(generate_unique_numbers(output_length))
    cvvs = generate_cvvs(card_numbers)
    expr_date = generate_expr_date()

    cards = []
    for idx, card_num in enumerate(card_numbers):
        card = build_card(card_num, expr_date, cvvs[idx])
        cards.append(card)


    save_to_json(RAW_PATH, "customer_cards", cards)

generate_cards(50)