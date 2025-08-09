from flask import Flask, render_template, request, send_file
import replicate
import os
import time

app = Flask(__name__)

# قراءة مفتاح Replicate من متغير البيئة
replicate.Client(api_token=os.environ.get("REPLICATE_API_TOKEN"))

MODEL_NAME = "stability-ai/stable-diffusion-2-1"

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    nsfw_enabled = False
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        nsfw_enabled = request.form.get("nsfw") == "on"

        # إضافة فلتر NSFW إذا كان مغلق
        if not nsfw_enabled:
            prompt += " ,safe content, no nudity"

        # تشغيل الموديل
        output = replicate.run(
            f"{MODEL_NAME}:latest",
            input={
                "prompt": prompt
            }
        )
        image_url = output[0]

    return render_template("index.html", image_url=image_url, nsfw_enabled=nsfw_enabled)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
