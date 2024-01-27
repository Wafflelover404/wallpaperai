import replicate
import os
import requests
import subprocess

os.environ['REPLICATE_API_TOKEN'] = "r8_CjXQtlXMDaYqUELnifd0NVAQLdn6b3a2OE1Yq"

output = replicate.run(
    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
    input={
        "prompt": "A mesmerizing macOS Big Sur-inspired wallpaper featuring a vibrant wavy gradient in an abstract 2D design, exuding a sense of modernity and elegance.",
        "negative_prompt": "Text, logos, words, low resolution, pixelation, distorted lines, jagged edges, inconsistent colors, visible compression artifacts, watermarks, signatures, trademarks, multiple views, reference sheets, distracting elements, cluttered composition, lack of harmony.",
        "width": 1920,
        "height": 1080,
        "num_outputs": 1
    }
)

try:
    img_url = output[0]
    print(f"Image URL: {img_url}")
    response = requests.get(img_url)

    if response.status_code == 200:
        with open('image.jpg', 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download the image. HTTP status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")

script = '''
var allDesktops = desktops();
for (var i = 0; i < allDesktops.length; i++) {
    var desktop = allDesktops[i];
    desktop.wallpaperPlugin = "org.kde.image";
    desktop.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
    desktop.writeConfig("Image", "image.jpg");
}
'''

command = [
    'qdbus',
    'org.kde.plasmashell',
    '/PlasmaShell',
    'org.kde.PlasmaShell.evaluateScript',
    script
]

subprocess.run(command, check=True)

