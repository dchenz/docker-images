import argparse
import fcntl
import io
import json
import os
import subprocess
import sys


def getArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir")
    parser.add_argument("--push", action="store_true")
    return parser.parse_args()


def setNonBlocking(fd: int) -> None:
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)


def runCommand(command: list[str]) -> str:
    stdoutText = io.StringIO()

    with subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
    ) as process:
        stdout = process.stdout
        stderr = process.stderr
        assert stdout
        assert stderr
        setNonBlocking(stdout.fileno())
        setNonBlocking(stderr.fileno())

        try:
            while True:
                c1 = stdout.read(1)
                if c1:
                    sys.stdout.write(c1)
                    stdoutText.write(c1)

                c2 = stderr.read(1)
                if c2:
                    sys.stderr.write(c2)
                    stdoutText.write(c2)

                if process.poll() is not None and not (c1 or c2):
                    break

            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command)

        except KeyboardInterrupt:
            pass

    return stdoutText.getvalue()


def getDockerImageName(spec: dict) -> str:
    repository = spec.get("repository")
    if not repository:
        raise Exception("Missing repository")
    gitHash = runCommand(["git", "rev-parse", "--short", "HEAD"]).strip()
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
