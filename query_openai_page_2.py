import base64
import requests
import os
import json

#openai.organization = "org-al1yGC2wFQ0b7agTqPVj84L9"
api_key = os.environ.get("OPENAI_API_KEY")

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def go(WCS):
  # Path to your image
  image_path = f"/Users/bizon/Projects/fish_data/RENCI Project/WCS field notes/{WCS}/{WCS}.pdf-1.png"

  # Getting the base64 string
  base64_image = encode_image(image_path)

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }

  payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": """You are an expert at transcribing human handwriting in an ichthyological context. 
            The attached image contains a field note for a wildlife biologist studying fish populations in 
            the Eastern United States. 
            
            This will often be the scientific name of species observed, counts of those species, 
            and some other associated notes.  
            Parse this image into the values of the following JSON Structure:
            {
              "Species observations: [
               { "Transcribed Name": "", 
                 "Scientific Name": "",
                 "Count": "", 
                 "Note" : "",
                 "Transcription Note": ""
               },
               ...
              ],
              "Other Entries": [ {
              "Transcribed Note": "",
              "Transcription Note": ""
              },...
              ]
            }
           
          Be aware of several points: the handwriting is quite poor, so be very careful. To avoid errors, for
          each entry, exactly transcribe the text as found in to the entries marked "Transcribed Name" or "Transcribed Note",
          "Count" and "Note" fields.  The "Note" field is to capture any other information written on the sheet associated
          with the specific species entry.
          
          Then using your knowledge of ichthyology, and the fact that this note was describing populations in the
            Eastern United States, fill in your best guess for "Scientific Name".
          
          There will sometimes be text on the page that is not simply a species entry, and is not associated with a
          specific species entry.  This text should be transcribed into the "Transcribed Note" field of the "Other Entries" array.
          
          For any entry you may enter a "Transcription Note" to indicate any difficulties encountered in the processing of the text,
          or provide other possible interpretations of the text.
          
          Please return only the JSON structure, with no extra commentary or text.
      """

          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}",
              "detail": "high"
            }
          }
        ]
      }
    ],
    "max_tokens": 2000
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  with open(f"page2_outputs1/{WCS}.json", "w") as f:
    json.dump(response.json(),f,indent=4)

if __name__ == "__main__":
  for wcs in ["WCS-3068", "WCS-3033", "WCS-3015", "WCS-3014", "WCS-3013", "WCS-3012", "WCS-3011",
              "WCS-3010", "WCS-2976", "WCS-2969"]:
    print(wcs)
    go(wcs)
