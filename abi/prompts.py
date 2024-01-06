# This is the collection of prompts used in the ABI project


is_chapter = """### Question:
Can this text be considered a chapter in a book? Introduction and Prefaces are not chapters.
### Text:
{text}
### Instructions:
Respond to the Question given the Text with either "True" or "False" and nothing else. Introduction and Prefaces are not chapters.
"""

read_section = """You are reading a book called {title}.
Your goal is to take notes in context to what is happening.
### Instructions
Given your notes, read the section and respond with synopsis of the events and characters in context of the section.
You must respond also with notes specific to the section on what happened and what is learned.
Give a high resolution of the sequence of events along with the characters involved
#### Example
##### Summary
This is the explanation of the section and the details of events and characters in the section
##### Notes
- Here there are bullet points
- About the relevant details
- Of the section
### Notes
{notes}
### Section
{section}
### Instructions
Only focus on this section.
"""