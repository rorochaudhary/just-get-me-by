import yaml
import base64

def get_target_percentage(user_input: str, grading_scheme: list) -> float:
    """Returns the percentage required to achieve the target letter grade."""
    if len(grading_scheme) == 0:
        return -1.0
    for grade in grading_scheme:
        if grade['name'].lower() == user_input.lower():
            return grade['value'] * 100
    return -1.0  # if the user_input isn't found in the grading scheme


def input_to_float(user_input: str, grading_scheme: list) -> float:
    """Returns the input as a float if it makes sense, -1.0 if it doesn't."""
    try:
        float_value = float(user_input)
        if not is_target_valid:
            return -1.0
        return float_value
    except ValueError:
        return get_target_percentage(user_input, grading_scheme)


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
            temp = base64.b64decode(data['token'])
            decoded_token = temp.decode('utf_32')
        return decoded_token, True
    except Exception as e:
        print(e)
        return "", False

def search_url() -> str:
    """looks within config.yaml to see if school url is stored and returns url + True. returns prompt + False otherwise"""
    try:
        with open('./config/config.yaml', 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            temp = base64.b64decode(data['url'])
            decoded_url = temp.decode('utf_32')
        return decoded_url, True
    except Exception as e:
        print(e)
        return "", False

def config_access(token: str, school_url: str) -> bool:
    """takes token and writes to /config/config.yaml"""
    with open('./config/config.yaml', 'w') as f:
        token_bytes = bytes(token, 'utf_32')
        url_bytes = bytes(school_url, 'utf_32')
        encoded_token = base64.b64encode(token_bytes)
        encoded_url = base64.b64encode(url_bytes)
        payload = {
            'token': encoded_token,
            'url': encoded_url
        }
        yaml.dump(payload, f)
    return True
