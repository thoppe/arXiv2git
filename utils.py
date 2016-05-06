import os

def get_login_params():

    # Verify that there is a token set as an env variable and load it
    shell_token  = "GITHUB_TOKEN"
    try:
        GITHUB_TOKEN = os.environ[shell_token]
    except:
        msg = "Set environment variable $GITHUB_TOKEN"
        raise SyntaxError(msg)

    login_params = {"access_token":GITHUB_TOKEN,}
    return login_params

