
import openai
import requests
from PIL import Image
from io import BytesIO
import os


openai.api_key = "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"

#Need a counter function to create unique file names for each image prompt
counter = 1

#print instructions to the user
print ("This is a Codenames image generation tool. You will be able to build your own codenames board by entering as many image ideas as you'd like and then typing `done`. These images will save to your desktop and you can print and play with your friends.")

# Loop to let the user continue entering images until they enter done

while True:
    #prompt user for image and enter done when completed
    prompt = input("Enter an image prompt (or `done` to finish): ")
    if prompt == "done":
        break


    #Set up the request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",

    }

    #Set up the request data
    data = {
        "model": "image-alpha-001",
        "prompt": prompt,
        "num_images": 1,
        "size": "256x256",
    }

    #Make the API request
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=data,
    )

    #Parse the response and extract the generate image
    response_data = response.json()
    image_url = response_data["data"][0]["url"]

    #Do something with the generated image, such as display it
    #print (image_url)

    # Download the generated image from the URL using Pillow
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))


    # Save the downloaded image to the full file path
    file_name = f"generated_image{counter}.png"
    file_path = os.path.join(os.path.expanduser("~/Desktop"), file_name)

    #file_path = (/Users/josephlanders/Desktop/)", file_name)
    #print(file_path)
    image.save(file_path)


    #Increment the counter for the next image

    counter += 1

print("Done generating images. Please go check your Desktop and have fun playing!")

