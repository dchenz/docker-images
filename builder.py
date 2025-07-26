import argparse
import json
import os
import subprocess


def getArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir")
    parser.add_argument("--push", action="store_true")
    return parser.parse_args()


def runCommand(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True)
    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()
    if stdout:
        print("STDOUT:", stdout)
    if stderr:
        print("STDERR:", stderr)
    if result.returncode:
        raise Exception(f"Docker build failed with {result.returncode}")
    return stdout


def getDockerImageName(spec: dict) -> str:
    repository = spec.get("repository")
    if not repository:
        raise Exception("Missing repository")
    gitHash = runCommand(["git", "rev-parse", "--short", "HEAD"])
    return f"{spec['repository']}:{gitHash}"


def runDockerBuild(spec: dict) -> None:
    context = spec.get("context", ".")
    dockerfile = spec.get("dockerfile", "./Dockerfile")
    imageName = getDockerImageName(spec)
    command = [
        "docker",
        "build",
        context,
        "-f",
        dockerfile,
        "-t",
        imageName,
    ]
    for name, value in spec.get("build_args", {}).items():
        command.append("--build-arg")
        command.append(f"{name}={value}")
    runCommand(command)


def runDockerPush(spec: dict) -> None:
    imageName = getDockerImageName(spec)
    input(f"Press any key to push {imageName}...")
    runCommand(["docker", "push", imageName])


if __name__ == "__main__":
    args = getArgs()
    os.chdir(args.project_dir)
    with open("spec.json") as f:
        spec = json.load(f)
    runDockerBuild(spec)
    if args.push:
        runDockerPush(spec)
