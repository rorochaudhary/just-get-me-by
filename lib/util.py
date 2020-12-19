import yaml

def get_target_percentage(target_letter: str, grade_scheme: list) -> float:
    """Returns the percentage required to achieve the target letter grade."""
    for grade in grade_scheme:
        if grade['name'].lower() == target_letter.lower():
            return grade['value'] * 100


def input_to_float(user_input: str) -> float:
    """Returns the input as a float if it makes sense, -1.0 if it doesn't."""
    try:
        float_value = float(user_input)
        if not is_target_valid:
            return -1.0
        return float_value
    except ValueError:
        return -1.0


def is_target_valid(target: float) -> bool:
    """Returns True if target percentage makes sense, False if not."""
    if target < 0.0:
        return False
    if target > 100.0:
        return False
    # Add more checks here if needed.
    return True

def search_token() -> str:
    """looks within config.yaml to see if token is stored and returns token + True. returns prompt + False otherwise"""
    try:
        with open('./config/config.yaml', 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data['token'], True
    except:
        return "Your Token", False

def search_url() -> str:
    """looks within config.yaml to see if school url is stored and returns url + True. returns prompt + False otherwise"""
    try:
        with open('./config/config.yaml', 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data['url'], True
    except:
        return "School URL", False

def config_access(token: str, school_url: str) -> bool:
    """takes token and writes to /config/config.yaml"""
    with open('./config/config.yaml', 'w') as f:
        payload = {
            'token': token,
            'url': school_url
        }
        yaml.dump(payload, f)
    return True
