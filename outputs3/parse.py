import json
import os

# loop through all the WCS-*.json files.  Read each as a json, extract the response, and write it to a new json
# json file with the same name as the input file but with the extension changed to .output.json. The original file
# stays the same.
files = os.listdir(".")
for file in files:
    if file.startswith("WCS-") and file.endswith(".json") and not file.endswith(".output.json"):
        with open(file) as inf:
            data = json.load(inf)
        with open(file.replace(".json", ".output.json"), "w") as outf:
            c = data["choices"][0]["message"]["content"]
            #The content looks like:
            # ```json
            # { ... a json document ... }
            # ```
            # Blah Blah comments

            # We want to extract the json document
            # First, find the first ```
            start = c.find("```")
            # Then find the next ```
            end = c.find("```", start+3)
            # Then extract the json document and take out the word json
            outf.write(c[start+8:end])