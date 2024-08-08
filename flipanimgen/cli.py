import argparse

from flipanimgen.main import main


def cli():
    parser = argparse.ArgumentParser(
        description="FlipAnimGen - Dithering animation generator from video files for Flipper Zero written in Python"
    )
    parser.add_argument(
        "--input", "-i", help="Input video path", type=str, required=True
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output folder path for animation",
        type=str,
        default="flipanimgen-output",
        required=False,
    )
    parsed_args = parser.parse_args()
    if not parsed_args.input.endswith(".mp4"):
        print("[red]Error:[/red] Input file must be .mp4")
        exit(1)
    main(parsed_args)
