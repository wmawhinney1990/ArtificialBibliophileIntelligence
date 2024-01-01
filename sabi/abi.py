# Artificial Bibliophile Intelligence

import together
import colorama

from sabi import utils

class ABI:

    def __init__(self, together_api_key):
        together.api_key = together_api_key
        self.history_pairs = []
        colorama.init()

    @property
    def models(self):
        return together.Models.list()

    def prompt_mixtral(self, prompt: str):
        model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        return together.Complete.create(
                 prompt = prompt, model = model, 
                 max_tokens = 8000, temperature = 0.7,
                 top_k = 50, # 0 means no filtering
                 top_p = 0.7, repetition_penalty = 1,
                 stop = ["</s>"] # add any sequence you want to stop generating at. 
               )

    def build_prompt(self, history_pairs, user_input):
        prompt = "<s>"
        for pair in history_pairs:
            prompt += " [INST] "+pair[0]+" [/INST] "+pair[1]+"</s> "
        prompt += " [INST] "+user_input+" [/INST]"
        return prompt

    def input(self, user_input):
        prompt = self.build_prompt(self.history_pairs, user_input)

        print()
        print(colorama.Fore.RED+prompt+colorama.Fore.RESET)
        print()

        output = self.prompt_mixtral(prompt)

        self.t = output
        model_out = output['output']['choices'][0]['text']

        print(colorama.Fore.CYAN+model_out+colorama.Fore.RESET)
        print()

        self.history_pairs.append((user_input, model_out))

    def npl_is_chapter(self, text: str) -> bool:
        instructions = "*Instructions: Only answer True or False, as if you were a python method designed to return a boolean."
        prompt = f"<s> [INST] {instructions} Does this text appear to be a book chapter? *Text: {text} [INST]"
        result = self.prompt_mixtral(prompt)
        return utils.parse_output(result['output']['choices'][0]['text'])

    @classmethod
    def use_together_api(cls, together_api_key):
        return cls(together_api_key)