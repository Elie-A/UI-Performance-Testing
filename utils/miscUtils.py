import screeninfo

def is_list_of_strings_sorted(list_of_elements: 'list[str]', order: str) -> bool:
        size = len(list_of_elements)
        if size == 0 or size == 1:
            return True

        if order == "ASC":
            for i in range(1, size):
                if list_of_elements[i - 1] > list_of_elements[i]:
                    return False
        elif order == "DESC":
            for i in range(1, size):
                if list_of_elements[i - 1] < list_of_elements[i]:
                    return False
        else:
            raise ValueError(f"Order must be 'ASC' or 'DESC'. Given: {order}")

        return True

def is_list_of_numbers_sorted(list_of_elements: 'list[str]', order: str) -> bool:
    size = len(list_of_elements)
    if size == 0 or size == 1:
        return True

    numbers = []
    for element in list_of_elements:
        try:
            # Remove any non-numeric characters like '$' before conversion
            clean_element = element.replace('$', '').replace(',', '').strip()
            number = float(clean_element) if '.' in clean_element else int(clean_element)
            numbers.append(number)
        except ValueError as e:
            raise ValueError(f"Could not convert '{element}' to a number. Error: {e}")

        if order == "ASC":
            return all(numbers[i] <= numbers[i + 1] for i in range(len(numbers) - 1))
        elif order == "DESC":
            return all(numbers[i] >= numbers[i + 1] for i in range(len(numbers) - 1))
        else:
            raise ValueError(f"Order must be 'ASC' or 'DESC'. Given: {order}")

def get_screen_resolution():
    screen = screeninfo.get_monitors()[0]
    return screen.width, screen.height
