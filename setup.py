import subprocess
import os
import argparse


def check_node_version():
    try:
        # Run the node --version command
        result = subprocess.run(
            ["node", "--version"],
            shell=True,
            capture_output=True,
            text=True,
            check=True,
        )
        # If the command was successful, print the Node.js version
        ver = result.stdout.strip()
        ver = ver.split(".")
        ver = float(".".join(ver[:2])[1:])

        if ver < 18.17:
            print(
                "Node.js version is less than 18.17.0. Please update Node.js to version 18.17.0 or later."
            )
            return False

        # print(f"Node.js is installed. Version: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        # If the command failed, Node.js is not installed
        print("Node.js is not installed.")
        return False
    except FileNotFoundError:
        # If the node command is not found, Node.js is not installed
        print("Node.js is not installed.")
        return False


def set_directories():
    parser = argparse.ArgumentParser(
        description="Generate Template Next.js Application"
    )
    parser.add_argument(
        "--dir", metavar="path", required=True, help="Directory to Angular project"
    )
    # Get and Set project directories
    angular_project_dir = parser.parse_args().dir
    angular_project_name = os.path.basename(angular_project_dir)
    react_project_name = f"{angular_project_name}-react"
    react_project_dir = os.path.join(
        os.path.dirname(angular_project_dir), react_project_name
    )
    react_project_dir = react_project_dir.replace("\\", "/")
    
    return angular_project_dir, angular_project_name, react_project_dir, react_project_name

def create_nextjs_project(react_project_dir):
    if os.path.isdir(react_project_dir) == False:
        print(f"Creating {react_project_dir}")

        command = [
            "npx",
            "create-next-app@latest",
            react_project_dir,
            "--ts",
            "--tailwind",
            "--eslint",
            "--app",
            "--src-dir",
            "--import-alias",
            "@/*",
        ]
        process = subprocess.Popen(command, shell=True)
        process.wait()

        # Check if the command was successful
        if process.returncode == 0 and os.path.isdir(react_project_dir) == True:
            print("Next.js application created successfully")
        else:
            print("Failed to create Next.js application")

    else:
        print(f"{react_project_dir} already exists")
