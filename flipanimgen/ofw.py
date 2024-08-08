import os
import shutil
import subprocess
from pathlib import Path
from typing import Union

from rich import print

from flipanimgen.metadata import get_manifest

OFW_DIR = "flipperzero-firmware-release"


def install_ofw(temp_path: Union[Path, str]):
    if not isinstance(temp_path, Path):
        temp_path = Path(temp_path)

    ofw_path = temp_path / OFW_DIR

    if ofw_path.exists():
        print("[yellow]OFW already installed, skipping...[/]")
        return

    print("[yellow]Downloading OFW...[/]")
    subprocess.run(
        [
            "git",
            "clone",
            "https://github.com/flipperdevices/flipperzero-firmware",
            ofw_path,
            "--depth=1",
        ]
    )
    print("[yellow]OFW downloaded![/]")


def copy_anim_to_ofw(new_animation_path: Union[Path, str], temp_path: Union[Path, str]):
    if not isinstance(new_animation_path, Path):
        new_animation_path = Path(new_animation_path)
    if not isinstance(temp_path, Path):
        temp_path = Path(temp_path)

    ofw_path = temp_path / OFW_DIR
    animations_path = ofw_path / "assets" / "dolphin" / "external"

    print("[yellow]Cleaning up old animations...[/]")
    for file in animations_path.iterdir():
        if file.is_file():
            file.unlink()
        elif file.is_dir():
            shutil.rmtree(file)

    print("[yellow]Copying new animation...[/]")
    shutil.copytree(str(new_animation_path), str(animations_path / "animation"))

    print("[yellow]Generating manifest...[/]")
    manifest_path = animations_path / "manifest.txt"
    with manifest_path.open("w") as f:
        f.write(get_manifest())


def compile_animation(temp_path: Union[Path, str], output_path: Union[Path, str]):
    if not isinstance(temp_path, Path):
        temp_path = Path(temp_path)
    if not isinstance(output_path, Path):
        output_path = Path(output_path)

    print("[yellow]Compiling animation...[/]")

    cwd = temp_path / OFW_DIR

    old_dir = os.getcwd()
    os.chdir(cwd)
    command = [
        "fbt.cmd" if os.name == "nt" else "fbt",
        "icons",
        "proto",
        "dolphin_internal",
        "dolphin_ext",
        "resources",
    ]
    subprocess.run(command)
    os.chdir(old_dir)

    ofw_path = temp_path / OFW_DIR
    compiled_animations_path = ofw_path / "build"
    build_name = compiled_animations_path.iterdir().__next__()
    compiled_animations_path = (
        compiled_animations_path
        / build_name
        / "assets"
        / "compiled"
        / "dolphin"
        / "animation"
    )

    shutil.copytree(str(compiled_animations_path), str(output_path), dirs_exist_ok=True)
