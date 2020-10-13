import decimal
from decimal import localcontext
from typing import Union


def to_absolute_amount(number: Union[float, str], decimals: int) -> int:
    if isinstance(number, str):
        d_number = decimal.Decimal(value=number)
    elif isinstance(number, float):
        d_number = decimal.Decimal(value=str(number))
    else:
        raise TypeError("Unsupported type.  Must be one of integer, float, or string")

    s_number = str(number)
    unit_value = decimal.Decimal(10 ** decimals)

    if d_number == decimal.Decimal(0):
        return 0

    if d_number < 1 and "." in s_number:
        with localcontext() as ctx:
            multiplier = len(s_number) - s_number.index(".") - 1

            ctx.prec = multiplier
            d_number = decimal.Decimal(value=number, context=ctx) * 10 ** multiplier
        unit_value /= 10 ** multiplier

    with localcontext() as ctx:
        ctx.prec = 999
        result_value = decimal.Decimal(value=d_number, context=ctx) * unit_value

    if result_value < 0 or result_value > 2 ** 256 - 1:
        raise ValueError("Resulting token value must be between 1 and 2**256 - 1")

    return int(result_value)
