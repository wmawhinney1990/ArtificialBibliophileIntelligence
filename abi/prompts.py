# This is the collection of prompts used in the ABI project


is_chapter = """### Question:
Can this text be considered a chapter in a book? Introduction and Prefaces are not chapters.
### Text:
{text}
### Instructions:
Respond to the Question given the Text with either "True" or "False" and nothing else. Introduction and Prefaces are not chapters.
"""

read_chunks = """You are reading a book called {title}.
You have some notes about your progress so far in the book.
Your goal is to take notes in context to what is happening.
### Instructions
Given your notes, read the chunks and append to your notes.
### Notes
{notes}
### Chunks
{chunks}
"""