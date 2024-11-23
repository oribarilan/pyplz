from enum import Enum
from plz.plz import plz


class Coffee(Enum):
    """Coffee enum"""

    ESPRESSO = "espresso"
    DOUBLE_ESPRESSO = "double espresso"


@plz.task()
def drink_coffee(type: Coffee = Coffee.ESPRESSO):
    """Brew coffee"""
    plz.print(f"Drinking {type.value}")


# @plz.task(requires=[(drink_coffee, (Coffee.DOUBLE_ESPRESSO,))])
# def check_emails():
#     """Check emails"""
#     plz.print("Checking emails")


# @plz.task()
# def take_a_nap(minutes: int = 10):
#     """Take a nap"""
#     plz.print(f"Taking a nap for {minutes} minutes")


# @plz.task(requires=[check_emails, (take_a_nap, (5,))])
# def write_report():
#     """Write report"""
#     plz.print("Writing report")
