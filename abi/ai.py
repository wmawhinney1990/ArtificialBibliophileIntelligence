# Artificial Bibliophile Intelligence

import together

from abi import utils, prompts

class AI:

    def __init__(self, together_api_key, verbose=False):
        together.api_key = together_api_key
        self.verbose = verbose

    @property
    def model(self):
        return "mistralai/Mixtral-8x7B-Instruct-v0.1"

    @property
    def info(self):
        return together.models.Models.info(self.model)

    @property
    def context_window(self):
        return self.info["context_length"]

    def prompt_mixtral(self, prompt: str):
        prompt = f"<s> [INST] {prompt} [INST]"
        return together.Complete.create(
                 prompt = prompt, model = self.model, 
                 max_tokens = 8000, temperature = 0.7,
                 top_k = 50, # 0 means no filtering
                 top_p = 0.7, repetition_penalty = 1,
                 stop = ["</s>"] # add any sequence you want to stop generating at. 
               )

    def find_chapter(self, chapters: list) -> int:
        for i, chapter in enumerate(chapters):
            if len(chapter) > 500: chapter = chapter[:500]

            if self.verbose: utils.inline_print(f"Looking for a chapter ... | {i} / {len(chapters)}")

            results = self.prompt_mixtral(prompts.is_chapter.format(text=chapter))
            result = utils.parse_output(results['output']['choices'][0]['text'])

            if utils.str_to_bool(result[0]):
                # LOGGIGN NEEDS TO BE ESTABLISHED HERE
                if self.verbose: utils.inline_print(result[-1], end="\n\n")
                return i

    def read_section(self, title, notes, section) -> str:
        prompt = prompts.read_section.format(title=title, notes=notes, section=section)
        results = self.prompt_mixtral(prompt)
        return results['output']['choices'][0]['text']

    @classmethod
    def together_backend(cls, together_api_key, **kwargs):
        return cls(together_api_key, **kwargs)