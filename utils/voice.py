import os
import uuid
from gtts import gTTS


def text_to_speech(
    text: str,
    output_dir: str = "data/audio"
) -> str:

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    filename = f"feynman_voice_{uuid.uuid4()}.mp3"

    file_path = os.path.join(
        output_dir,
        filename
    )

    clean_text = text.replace(
        "#",
        ""
    ).replace(
        "*",
        ""
    )

    tts = gTTS(
        text=clean_text[:3000],
        lang="en"
    )

    tts.save(file_path)

    return file_path