# This is the collection of prompts used in the ABI project

import re
import string

summarize = """Your job is to summarize information.
You will be given sets of related information for a book.
Your goal is to combine the infomation while retaining all relevent information.

### Information
{info}

### Instructions
Summarize all the information.

### Summary

"""

is_chapter = """### Question:
Can this text be considered a chapter in a book? Introduction and Prefaces are not chapters.
### Text:
{text}
### Instructions:
Respond to the Question given the Text with either "True" or "False" and nothing else. Introduction and Prefaces are not chapters.
"""

basic_notes = """You are reading a book called {title}.
Your goal is to take notes in context to what is happening.
## Instructions
Given your notes, read the section and respond with synopsis of the events and characters in context of the section.
You must respond also with notes specific to the section on what happened and what is learned.
Give a high resolution of the sequence of events along with the characters involved.
Then, in JSON format, provide a question to answer set. Be detailed and accurate in the question answer information.

## Example
##### Summary
This is the explanation of the section and the details of events and characters in the section. Your goal is to be detailed in the events and interactions.
##### Notes
- Here there are bullet points
- About the relevant details
- Of the section
- Includes details of events
- Include details of interactions
- Provide more details
- Provide more details
##### JSON
[
"What is 2+2?" : "4" ,
"What details are relivent to the story?" : "All of them" ,
"How detailed should the questions and answers be?" : "The questions and answers should be as detailed as possible." ,
"How many JSON question/answers should be captured?" : "There should be a lot of question/answer details." ,
"Why is the sky blue?" : "Because of a process called Rayleigh scattering, sunlight is scattered by the atmosephere. Blue light is scattered more which renders the blue sky we see." ,
"Why do we brush our teeth?" : "We brush our teeth to remove food and plaque, prevent tooth decay and gum disease, and maintain overall oral health."
]

## Notes
{summary}
## Section
{section}
## Instructions
Only focus on this section.

# Response
"""

class Template:
    def __init__(self, template: str):
        """Initialize with a template string."""
        self.template = template
        self.kwargs = {}

    def __call__(self, **kwargs) -> None:
        """Store incoming kwargs into kwargs dict"""
        for key in self.keys:
            if key in kwargs:
                self.kwargs[key] = kwargs[key]

    class CustomFormatter(string.Formatter):
        def get_value(self, key, args, kwargs):
            if isinstance(key, int):
                return args[key]
            else:
                return kwargs.get(key, '{' + key + '}')

    def __str__(self):  
          formatter = self.CustomFormatter()
          return formatter.format(self.template, **self.kwargs)

    @property
    def is_full(self):
        return all(item in self.kwargs for item in self.keys)
    
    @property
    def keys(self):
        return re.findall(r'\{(\w+)\}', self.template)
    
    @property
    def prompt(self) -> str:
        """Return prompt self.kwargs contain all format keys in self.template"""
        if not isinstance(self.template, str):
            raise TypeError("Inputs must be numbers")
         
        if not self.is_full:
            raise KeyError(f"Template keys issue! Necessary keys: {', '.join(self.keys)}. Current keys: {', '.join(list(self.kwargs.keys()))}.")

        return self.template.format(**self.kwargs)