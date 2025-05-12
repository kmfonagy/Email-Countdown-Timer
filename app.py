from flask import Flask, request, send_file
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw, ImageFont
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/timer")
def timer():
    target_str = request.args.get("target")
    if not target_str:
        return "Missing target parameter", 400

    try:
        target = datetime.fromisoformat(target_str).replace(tzinfo=timezone.utc)
    except Exception:
        return "Invalid target datetime format", 400

    now = datetime.now(timezone.utc)
    width, height = 263, 63
    frame_count = 60  # 60 seconds of animation
    number_color = "#d2232a"
    label_color = "#000000"
    separator_color = "#ced9e1"
    bg_color = "#ffffff"

    # Load fonts
    orbitron = ImageFont.truetype("fonts/Orbitron-Regular.ttf", 22)
    raleway = ImageFont.truetype("fonts/Raleway-Regular.ttf", 10)

    frames = []

    for i in range(frame_count):
        current = now + timedelta(seconds=i)
        remaining = target - current

        if remaining.total_seconds() < 0:
            days = hours = minutes = seconds = 0
        else:
            total = int(remaining.total_seconds())
            days, rem = divmod(total, 86400)
            hours, rem = divmod(rem, 3600)
            minutes, seconds = divmod(rem, 60)

        # Create frame
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        # EVENLY SPACED COUNTDOWN BLOCKS
        values = [f"{days:02}", f"{hours:02}", f"{minutes:02}", f"{seconds:02}"]
        labels = ["Days", "Hours", "Minutes", "Seconds"]
        colon = ":"

        y_val = 5
        y_label = 38

        column_width = 263 // 4  # ~65px per block
        digit_width = orbitron.getlength("88")
        colon_width = orbitron.getlength(":")

        for idx in range(4):
            center_x = column_width * idx + column_width // 2

            # Draw the number (centered)
            num_x = center_x - digit_width // 2
            draw.text((num_x, y_val), values[idx], font=orbitron, fill=number_color)

            # Draw the label below (centered)
            label_width = raleway.getlength(labels[idx])
            label_x = center_x - label_width // 2
            draw.text((label_x, y_label), labels[idx], font=raleway, fill=label_color)

            # Draw colons after Hours and Minutes
            if idx in [1, 2]:
                colon_x = column_width * idx + column_width - colon_width // 2
                draw.text((colon_x, y_val), colon, font=orbitron, fill=number_color)

            # Draw vertical line after Days
            if idx == 0:
                line_x = column_width - 2
                draw.line([(line_x, y_val + 7), (line_x, y_val + 21)], fill=separator_color, width=1)

        frames.append(img)

    # Save GIF
    img_io = io.BytesIO()
    frames[0].save(
        img_io,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=1000,
        disposal=2
    )
    img_io.seek(0)
    return send_file(img_io, mimetype="image/gif")
