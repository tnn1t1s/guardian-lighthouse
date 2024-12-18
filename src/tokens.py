import os

def load_auth_token(token_file_path="tokens/auth_token.txt", env_var="AUTH_TOKEN"):
    """
    Loads an authentication token for use in scripts.

    Priority:
    1. Environment Variable (if AUTH_TOKEN or a specified env_var is set).
    2. Direct File Loading (if auth_token.txt or a specified file exists).

    Parameters:
    - token_file_path: str, optional
        Path to the token file. Default is "tokens/auth_token.txt".
    - env_var: str, optional
        Name of the environment variable to check for the token. Default is "AUTH_TOKEN".

    Returns:
    - str: The authentication token.

    Raises:
    - FileNotFoundError: If the token file is not found and the env_var is not set.
    - ValueError: If the token is empty or invalid.
    """
    # Check environment variable
    token = os.getenv(env_var)
    if token:
        return token

    # Check token file
    if os.path.exists(token_file_path):
        with open(token_file_path, 'r') as file:
            token = file.read().strip()
        if token:
            return token
        else:
            raise ValueError(f"Token file {token_file_path} is empty.")

    # Raise error if token not found
    raise FileNotFoundError(
        f"Authentication token not found. Please set the {env_var} environment variable or provide a valid token file at {token_file_path}."
    )

if __name__ == "__main__":
    try:
        # Example usage
        token = load_auth_token()
        print("Authentication token loaded successfully.")
    except Exception as e:
        print(f"Error: {e}")
