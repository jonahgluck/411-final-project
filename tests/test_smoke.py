""" 
This model demonstrates how to perform asynchrynous account management tasks using curl commands
and a REST API. 

The operations include:
1. Creating a new account
2. Logging into the account
3. Updating the account password
Asynchronous execution is implemented using the 'asyncio' library.
"""

import asyncio


async def run_curl(command):
    """Run a curl command asynchronously.
       Args: 
           command (str): The curl command to be executed
        Returns:
            None: Prints the success or failure of the command, along with its output or error.
    """
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode == 0:
        print(f"Command succeeded: {command}")
        print(f"Response:\n{stdout.decode()}")
    else:
        print(f"Command failed: {command}")
        print(f"Error:\n{stderr.decode()}")

async def main():
    """Run a sequence of curl commands for managing an account via a REST API.
        The sequence performs the following steps:
        1. Creates an account
        2. Logs into the created account
        3. Updates the account password
        Returns:
            None: Outputs the results of each operation to the console.
    """
    # Step 1: Create Account
    create_account_cmd = (
        'curl -X POST http://127.0.0.1:5000/create-account '
        '-H "Content-Type: application/json" '
        '-d \'{"username": "accountN1", "password": "CS411"}\''
    )
    await run_curl(create_account_cmd)

    # Step 2: Log In
    login_cmd = (
        'curl -X POST http://127.0.0.1:5000/login '
        '-H "Content-Type: application/json" '
        '-d \'{"username": "accountN1", "password": "CS411"}\''
    )
    await run_curl(login_cmd)

    # Step 3: Update Password
    update_password_cmd = (
        'curl -X PUT http://127.0.0.1:5000/update-password '
        '-H "Content-Type: application/json" '
        '-d \'{"username": "accountN1", "old_password": "CS411", "new_password": "ILOVECS411"}\''
    )
    await run_curl(update_password_cmd)

# Run the main coroutine
if __name__ == "__main__":
    asyncio.run(main())

