import os
import subprocess

#tools
WORKSPACE="workspace"
def read_file(path) -> str:
    path = os.path.join(WORKSPACE, path)
    with open(path, "r") as file:
        text = file.read()

    return text

def write_file(path, code) -> None:
    path = os.path.join(WORKSPACE, path)
    with open(path, "w") as file:
        file.write(code)


def list_files(path=".") -> list:
    path = os.path.join(WORKSPACE,path)
    return os.listdir(path)


def run_command(command) -> dict:
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        cwd=WORKSPACE
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }


if __name__=="__main__":
    print(read_file("example.py"))
    write_file("example.py","print('hello world')")
    print(run_command("python example.py"))
    