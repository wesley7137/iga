# Take in code, and execute it with Modal
import tempfile
import subprocess
import os

source_code = """
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

mean = np.mean(arr)
print("Mean of given array is", mean)
"""


def run_code(source_code):
    # Add tabs to source code
    source_code = "\n".join(["    " + line for line in source_code.split("\n")])

    # Wrap function in a Modal decorator
    code = f"@stub.function()\ndef main():\n{source_code}"

    # Create a stub
    code = "stub = modal.Stub()\n" + code

    # Import Modal
    code = "import modal\n" + code

    # Create a temporary file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, dir=f"{os.getcwd()}/tmp"
    ) as f:
        f.write(code)
        f.close()

        # Run the file using Modal
        res = subprocess.run(
            [f"modal run {f.name}"],
            executable="/bin/bash",
            shell=True,
            capture_output=True,
        )

        return (res.stdout.decode("utf-8"))

    # Delete the temporary file
    # os.remove(f.name)


if __name__ == "__main__":
    print(run_code(source_code))