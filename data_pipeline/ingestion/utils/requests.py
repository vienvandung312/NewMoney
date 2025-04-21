import requests 
import uuid
import random

def spoofed_requests(
    url: str,
    data: dict = None,
    method: str = "GET",
    timeout: int = 10,
    ack: bool = True,
) -> requests.Response:
    """
    Send an spoofed HTTP request.

    Args:
        url (str): The URL to send the request to.
        data (dict, optional): Query parameters to include in the request. Defaults to None.
        headers (dict, optional): Headers to include in the request. Defaults to None.
        method (str, optional): HTTP method to use. Defaults to "GET".
        timeout (int, optional): Timeout for the request in seconds. Defaults to 10.

    Returns:
        requests.Response: The response object from the request.
    """

    headers = {
            'Content-Type': 'application/json',
            'X-Mly-Id': str(uuid.uuid4()),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',}

    user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15'
        ]
    
    headers['User-Agent'] = random.choice(user_agents)


    try:
        if method.upper() == "GET":
            if data:
                response = requests.get(url, headers=headers, timeout=timeout)
            else: 
                response = requests.get(url, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=timeout)
        else:
            raise ValueError("Unsupported HTTP method")
        response.raise_for_status()
        
        if ack:
            print(f"Request was successful with status code {str(response.status_code)}.")
        return response
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None