---
applyTo: 'prompt_maker.py'
description: 'This script generates prompts for various tasks based on user input and predefined templates.'
---

# About

Generate random prompts for pictures with Kirsche.

The promps should always start with "Draw a picture of Kirsche" and then add a random element to the prompt. The random element should be chosen from a predefined list of elements, such as "in a park", "on the beach", "in space", etc. The script should return the generated prompt as a string.

Use Python's built-in `random` library to select a random element from the predefined list and concatenate it with the base prompt "Draw a picture of Kirsche". Finally, return the generated prompt as a string.

Name the file `prompt_maker.py` and place it in the root directory of the project.

# Predefined Elements

Create a list of the of defined elements to be used in the prompts. The elements should be stored in a list variable named `{subject}_elements`. Subjects should be:

- Outfits: attire, clothing, fashion
- Locations: places, settings, environments
- Activities: actions, hobbies, pastimes
- Emotions: feelings, moods, expressions

An example prompt could be "Draw a picture of Kirsche wearing {outfit} in {location}. She is engaged in {activity} and feeling {emotion}."

# Workflow

1. Run the script to generate a prompt with no parameters. The script should randomly select one element from each of the predefined lists and generate a prompt based on the template.
2. Save the generated prompt to a text file named `prompt.txt` in the root directory of the project.