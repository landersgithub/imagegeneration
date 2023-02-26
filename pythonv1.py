
import openai
import requests
from PIL import Image
from io import BytesIO
import os


openai.api_key = "INSERT OPENAI API KEY HERE"

#print instructions to the user
print ("There is nothing worse than running out of squares in Codenames. This is a Codenames image generation tool powered by text completion endpoint. Each time this script is ran, it will generate 10 more random images for you to print and use when playing codenames.")

#Generate 10 random images
data = {
    "model": "text-davinci-002",
    "prompt": "Generate random words, not numbers, and make sure no words are the same:",
    "temperature": 0.5,
    "max_tokens": 30,
    "n": 10,
    "stop": "."

}


response = openai.Completion.create(engine="text-davinci-002", prompt=data['prompt'], max_tokens=data['max_tokens'], temperature=data['temperature'], n=data['n'], stop=data['stop'])
prompts = response.choices
prompts = [prompt.text.strip() for prompt in prompts]



# Loop through the generated prompts and generate and save the corresponding images

for i, prompt in enumerate(prompts):
    
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


    
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))


    # Save the downloaded image to the full file path
    file_name = f"generated_image{i+1}.png"
    file_path = os.path.join(os.path.expanduser("~/Desktop"), file_name)
    image.save(file_path)
    

print("Done generating images. Please go check your Desktop and have fun playing!")

