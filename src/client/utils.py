def cast_money_string_to_float(text: str):
    if not text.replace('.', '').isdigit() or text.find('.') > 1:
        raise TypeError
    if len(text.split('.')) == 2 and len(text.split('.')[0]) > 2:
        raise TypeError
    return float(text)
