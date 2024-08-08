def generate_meta(frames_count: int, framerate: int) -> str:
    duration = int(frames_count / framerate * 1000)
    frames_order = " ".join(map(str, range(0, frames_count)))

    return """
    Filetype: Flipper Animation
    Version: 1
    
    Width: 128
    Height: 64
    Passive frames: {frames_count}
    Active frames: 0
    Frames order: {frames_order}
    Active cycles: 0
    Frame rate: {framerate}
    Duration: {duration}
    Active cooldown: 0
    Bubble slots: 0
    """.format(
        frames_count=frames_count,
        duration=duration,
        frames_order=frames_order,
        framerate=framerate,
    ).strip()


def get_manifest() -> str:
    return """
    Filetype: Flipper Animation Manifest
    Version: 1
    
    Name: animation
    Min butthurt: 0
    Max butthurt: 14
    Min level: 1
    Max level: 3
    Weight: 8
    """.strip()
