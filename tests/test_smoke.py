import asyncio

async def run_curl(command):
    """Run a curl command asynchronously."""
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

