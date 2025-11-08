import math
from typing import Tuple
from escpos.printer import Usb
from PIL import Image, ImageDraw, ImageFont

WIDTH = 501
HEIGHT = 960
LINE_SPACING = 4


def text_to_image(
    text: str,
    font_filepath: str,
    font_size: int,
    color: Tuple[int, int, int, int],
):
    font = ImageFont.truetype(font_filepath, size=font_size)
    img = Image.new("RGBA", (0, 0), "white")

    draw = ImageDraw.Draw(img)
    draw_point = (0, 0)

    multilineTextData = []
    currentLineLength = 0
    totalHeight = 0
    for word in text.split(" "):
        wordBox = draw.textbbox((0, 0), word, font=font)
        wordLength = wordBox[2] - wordBox[0]
        if wordLength > WIDTH:
            raise ValueError(
                f"Word '{word}' is too long to fit in the image width of {WIDTH} pixels."
            )
        if math.ceil(currentLineLength + wordLength) > WIDTH:
            multilineTextData.append("\n")
            currentLineLength = 0
        multilineTextData.append(word)
        multilineTextData.append(" ")
        currentLineLength += wordLength + draw.textlength(" ", font=font)

    multiLineText = "".join(multilineTextData).strip() + "\n"
    multilineBox = draw.multiline_textbbox(
        (0, 0), multiLineText, font=font, spacing=LINE_SPACING)
    totalHeight = multilineBox[3] - multilineBox[1] + LINE_SPACING * 3

    img = Image.new("RGBA", (WIDTH, math.ceil(totalHeight)), "white")
    draw = ImageDraw.Draw(img)

    draw.multiline_text(draw_point, multiLineText, font=font,
                        fill=color, spacing=LINE_SPACING)

    return img


def getTaskImage(message: dict):

    titleImg = Image.new("RGBA", (0, 0), "white")
    if 'Title' in message:
        titleImg = text_to_image(
            message['Title'],
            "./font.ttf",
            36,
            (0, 0, 0, 255),
        )
    # draw a line under the title
    draw = ImageDraw.Draw(titleImg)
    draw.line((0, titleImg.height - 2, WIDTH, titleImg.height - 2),
              fill=(0, 0, 0, 255), width=4)

    bodyImg = text_to_image(
        message["Body"],
        "./font.ttf",
        30,
        (0, 0, 0, 255),
    )

    dueDateImg = Image.new("RGBA", (0, 0), "white")
    if 'DueDate' in message:
        dueDateImg = text_to_image(
            f"Due Date: {message['DueDate']}",
            "./font.ttf",
            40,
            (0, 0, 0, 255),
        )

    createdDateImg = Image.new("RGBA", (0, 0), "white")
    if 'CreatedDate' in message:
        createdDateImg = text_to_image(
            f"Created Date: {message['CreatedDate']}",
            "./font.ttf",
            18,
            (0, 0, 0, 255),
        )

    height = titleImg.height + bodyImg.height + \
        dueDateImg.height + createdDateImg.height

    img = Image.new("RGBA", (WIDTH, height), "white")
    img.paste(titleImg, (0, 0))
    img.paste(bodyImg, (0, titleImg.height))
    img.paste(dueDateImg, (0, titleImg.height + bodyImg.height))
    img.paste(createdDateImg, (0, titleImg.height +
              bodyImg.height + dueDateImg.height))

    return img


def main():
    task = {
        "Body": "This is a test task to print. It has multiple lines of text to see how the text wrapping works. Let's add some more text to make sure it wraps correctly across several lines. This should be enough text to test the functionality.",
        "Title": "Test Task Title",
        "Priority": "High",
        "DueDate": "2024-12-31",
        "CreatedDate": "2024-06-15",
    }

    im = getTaskImage(task)
    im.show()

    # p = Usb(0x0fe6, 0x811e, 0, profile="RP326")
    # p.image(im, impl="bitImageColumn")
    # p.text("\n"*4)
    # p.cut()


if __name__ == "__main__":
    main()
