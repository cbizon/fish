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
  image_path = f"/Users/bizon/Projects/fish_data/RENCI Project/WCS field notes/{WCS}/{WCS}.pdf-0.png"

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
            "text": """You are an expert at transcribing human handwriting. The attached image contains a field note for a wildlife biologist studying fish populations in nature. Please transcribe the handwritten portions into the following json structure. You will note that the keys in the json correspond to the entry locations on the form. You are to transcribe the written text into the corresponding values.

  Be aware of several points: the handwriting is quite poor, so be very careful especially on the dates and times. 
  Also, the text corresponding to a particular form element may be on the line, above the line, or sometimes continue below the line or to the side. 
  Sometimes the person filing out the form will use a line or caret to indicate the continuation of the response. 
  Often text will be crossed or scribbled out - please ignore this text.
  Many fields will be left blank if the question is not applicable.
  
  Some field specific notes:  For DATE the format given is almost always DD MMM YYYY. (Numeric Date, Abbreviated Month Name, Four Digit Year).
  TIME: is always a range given in four digit 24 hour time.  For instance 0830-1100. The total time is usually about two hours.  Sometimes there will
  be two time intervals given, often above and below the line.
  FIELD#: should be in the form WCS-**** where **** indicates a four digit number.
  LOCALITY: This response covers two lines, be sure to get the text from both.  The locality frequently contains the
  distance (in air miles) and direction to a local city or town.  For instance "6.2 air mi WNW of Raleigh"
  LAT and LONG are usually given with 5 decimal places of precision. Both LAT and LONG often have two values, indicating the beginning
  and ending coordinates of the survey.
  METHOD CAPTURE sometimes has text both above and below the line.  Common values include "seine" (often with a measurement), 
  "electrofishing boat", "backback electrofisher", and "angling"
  STREAM WIDTH: The text is often raised above the line
  MAX DEPTH: The text is often raised above the line
  SALINITY does not usually include numbers or units, but only a qualitative description such as "slight"
  CURRENT: Common values include "fast", "moderate", and "sluggish", often abbreviated.
  
  Most, but not all, measurements of depth or width will be listed in meters, usually abbreviated as "m" or "mt"

  Note also that there is a key at the end of the JSON document called Transcription Notes that does not correspond to a form element. 
  Please fill this value with any difficulties encountered in the processing of the text. 
  For instance if you are unsure of a result, or you found handwritten text but were unable to associate it with a particular form element. 
  If you have no difficulties, you can leave this element blank.

  { "NORTH CAROLINA STATE MUSEUM OF NATURAL SCIENCES AQUATIC/MARINE FIELD DATA SHEET": 
    { "DATE": "", 
    "TIME": "", 
    "FIELD#": "", 
    "REGIONAL DATA": { 
      "FOR FRESHWATER ONLY": { 
        "CONTINENT": "", 
        "PRINCIPAL DRAINAGE BASIN": "", 
        "RIVER SUBBASINS": "", 
        "COUNTRY": "", 
        "ST/PROV.": "" }, 
      "FOR MARINE ONLY": { 
        "OCEAN": "", 
        "OCEAN SUBBASIN": "", 
        "COUNTRY (if coastal collection)": "", 
        "ST/PROV.": "" 
        } 
      }, 
    "LOCALE DATA/COLLECTING INFORMATION": { 
      "COUNTIES": "", 
      "MAP SHEET": "", 
      "LOCALITY": "", 
      "LAT": "", 
      "LONG": "", 
      "OTHER COORDS": "", 
      "VESSEL": "", 
      "CRUISE": "", 
      "STA#": "", 
      "PERMIT": "", 
      "COLLECTORS": "", 
      "METHOD CAPTURE": "", 
      "DEPTH CAPTURE": "", 
      "PRESERVATIVE": "" 
      }, 
    "ECOLOGICAL DATA": { 
      "GENERAL HABITAT": "", 
      "ELEV.": "", 
      "STREAM WIDTH": "", 
      "MAX DEPTH": "", 
      "CURRENT": "", 
      "COLOR": "", 
      "TEMP": "", 
      "SALINITY": "", 
      "TIDE": "", 
      "BOTTOM TYPE": "", 
      "VEGETATION": "", 
      "SHORE TYPE": "" 
      }, 
      "ACC.#": "", 
      "ADD. NOTES/SPECIES LISTS ETC. on back": "" 
      } 
      "TRANSCRIPTION NOTES": "" }"""
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
    "max_tokens": 900
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  with open(f"outputs3/{WCS}.json", "w") as f:
    json.dump(response.json(),f,indent=4)

if __name__ == "__main__":
  for wcs in ["WCS-3068", "WCS-3033", "WCS-3015", "WCS-3014", "WCS-3013", "WCS-3012", "WCS-3011",
              "WCS-3010", "WCS-2976", "WCS-2969"]:
    print(wcs)
    go(wcs)
