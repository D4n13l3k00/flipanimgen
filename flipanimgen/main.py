from pathlib import Path
from shutil import rmtree

import cv2
from rich import print

from flipanimgen.dithering import floyd_steinberg_dither
from flipanimgen.metadata import generate_meta
from flipanimgen.ofw import install_ofw, copy_anim_to_ofw, compile_animation


def main(args):
    input_video_path = Path(args.input)

    if not input_video_path.exists():
        print(f"[bold red]Input video not found:[/] {input_video_path}")
        return

    temp_folder = Path.cwd() / "flipanimgen_temp"
    print(f"[bold cyan]Temp folder:[/] {temp_folder}")
    temp_folder.mkdir(exist_ok=True)

    frames_folder = temp_folder / "animation"
    print(f"[bold cyan]Frames folder:[/] {frames_folder}")
    frames_folder.mkdir(exist_ok=True)

    output_path = Path(args.output)
    if output_path.exists():
        rmtree(output_path, ignore_errors=True)
    print(f"[bold cyan]Output path:[/] {output_path}")
    output_path.mkdir(exist_ok=True)

    cap = cv2.VideoCapture(str(input_video_path))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width, height = (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )
    fps = cap.get(cv2.CAP_PROP_FPS)

    current_frame = 0
    print(f"[bold yellow]Processing frames:[/] {total}")
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if width / height > 2:
                new_width = height * 2
                frame = frame[
                    :,
                    int((width - new_width) / 2) : int((width + new_width) / 2),
                ]
            else:
                new_height = width / 2
                frame = frame[
                    int((height - new_height) / 2) : int((height + new_height) / 2),
                    :,
                ]

            frame = cv2.resize(frame, (128, 64))

            dithered_frame = floyd_steinberg_dither(frame)

            cv2.imwrite(
                str(frames_folder / f"frame_{current_frame}.png"),
                dithered_frame,
            )

            current_frame += 1
            print(f"[bold yellow]Progress:[/] {current_frame}/{total}", end="\r")
        else:
            break

    print()

    cap.release()
    cv2.destroyAllWindows()

    print(f"[bold yellow]Generating meta.txt[/]")
    meta = generate_meta(
        frames_count=current_frame,
        framerate=int(fps),
    )

    with open(frames_folder / "meta.txt", "w") as f:
        f.write(meta)

    install_ofw(temp_folder)
    copy_anim_to_ofw(frames_folder, temp_folder)
    compile_animation(temp_folder, output_path)

    rmtree(frames_folder, ignore_errors=True)
