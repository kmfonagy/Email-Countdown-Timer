from flask import Flask, request, send_file
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw, ImageFont
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/timer": {"origins": "*"}})  # allow all origins (good for local dev)

@app.route("/timer/<timestamp>")
def timer(timestamp):
    
    try:
        # Example format: 20250621T035900Z
        target = datetime.strptime(timestamp, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return "Invalid timestamp format", 400

    now = datetime.now(timezone.utc)
    width, height = 263, 67
    frame_count = 60  # 60 seconds of animation
    number_color = "#d2232a"
    label_color = "#000000"
    separator_color = "#ced9e1"
    bg_color = "#ffffff"

    # Load fonts
    orbitron = ImageFont.truetype("fonts/Orbitron-SemiBold.ttf", 28)
    raleway = ImageFont.truetype("fonts/Raleway-Medium.ttf", 10)

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
        y_label = 44

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

# ✅ This is the key part to run Flask manually on port 5050:
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)