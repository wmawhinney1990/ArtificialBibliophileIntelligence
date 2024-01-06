# Artificial Bibliophile Intelligence

import together

from abi import utils, prompts

class AI:

    def __init__(self, together_api_key, verbose=False):
        together.api_key = together_api_key
        self.verbose = verbose

    @property
    def models(self):
        return together.Models.list()

    def prompt_mixtral(self, prompt: str):
        model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        prompt = f"<s> [INST] {prompt} [INST]"
        return together.Complete.create(
                 prompt = prompt, model = model, 
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
            #print(f"\n\n{results['output']['choices'][0]['text']}\n\n")
            result = utils.parse_output(results['output']['choices'][0]['text'])

            if utils.str_to_bool(result[0]):
                # LOGGIGN NEEDS TO BE ESTABLISHED HERE
                if self.verbose: utils.inline_print(result[-1], end="\n\n")
                return i

    @classmethod
    def together_backend(cls, together_api_key, **kwargs):
        return cls(together_api_key, **kwargs)