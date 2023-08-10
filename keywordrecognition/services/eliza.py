# import random
import re
from keywordrecognition.models import (
    Decomp,
    ElizaBot,
    DefaultMessage,
    Keyword,
    PostProcessing,
    Synonym,
    Reasmb,
)
from keywordrecognition.exceptions import ElizaServiceException
from keywordrecognition.enums import ELIZA_SERVICE_EXCEPTION


class ElizaService:
    def __init__(self, bot: ElizaBot):
        self.bot = bot
        self.keyword = None
        self.decomp = None

    def load_initial(self, content: str):
        DefaultMessage.objects.get_or_create(
            bot=self.bot, message=content, message_type=DefaultMessage.INITIAL
        )

    def load_final(self, content: str):
        DefaultMessage.objects.get_or_create(
            bot=self.bot, message=content, message_type=DefaultMessage.FINAL
        )

    def load_fallback(self, content: str):
        DefaultMessage.objects.get_or_create(
            bot=self.bot, message=content, message_type=DefaultMessage.FALLBACK
        )

    def load_synonym(self, content: str):
        patterns = content.split("/")
        patterns = [" ".join(pattern.split()) for pattern in patterns]
        try:
            for i in range(1, len(patterns)):
                Synonym.objects.get_or_create(
                    bot=self.bot, value=patterns[0], word=patterns[i]
                )
        except IndexError:
            pass

    def load_postprocessing(self, content: str):
        patterns = content.split("/")
        patterns = [" ".join(pattern.split()) for pattern in patterns]
        try:
            PostProcessing.objects.get_or_create(
                input_word=patterns[1], output_word=patterns[0]
            )
        except IndexError:
            pass

    def load_keyword(self, content: str):
        patterns = content.split("/")
        word = " ".join(patterns[0].split())
        weight = int(patterns[1]) if len(patterns) > 1 else 1
        self.keyword, created = Keyword.objects.get_or_create(
            bot=self.bot, word=word, weight=weight
        )

    def load_decomp(self, content: str):
        if self.keyword:
            self.decomp, created = Decomp.objects.get_or_create(
                keyword=self.keyword, pattern=content
            )

    def load_reasmb(self, content: str):
        if self.decomp:
            Reasmb.objects.get_or_create(decomp=self.decomp, template=content)

    def load_item(self, tag, content: str):
        if tag == "initial":
            self.load_initial(content)
        elif tag == "final":
            self.load_final(content)
        elif tag == "fallback":
            self.load_fallback(content)
        elif tag == "synon":
            self.load_synonym(content)
        elif tag == "post":
            self.load_postprocessing(content)
        elif tag == "key":
            self.load_keyword(content)
        elif tag == "decomp":
            self.load_decomp(content)
        elif tag == "reasmb":
            self.load_reasmb(content)

    def load_txt(self, data: list):
        for line in data:
            if not line.strip():
                continue
            tag, content = [part.strip() for part in line.split(":=")]
            self.load_item(tag, content)

    def generate_sentence(self, template, decomp_pattern_parts):
        open_bracket = False
        current_position = -1
        result_template = template

        for char in result_template:
            if char == "(":
                open_bracket = True
                current_position = ""
            elif char == ")":
                open_bracket = False
                if current_position:
                    replace_char = f"({current_position})"
                    result_template = result_template.replace(
                        replace_char,
                        decomp_pattern_parts[int(current_position)],
                    )
                    print(result_template)
            elif open_bracket:
                current_position += char
            else:
                pass

        return result_template

    def generate_response(
        self, decomp: Decomp, decomp_pattern_parts: list
    ) -> list[str]:
        response = None
        reasmb = decomp.get_random_reasmb()
        # for i in range(len(decomp_pattern_parts)):
        #     response = reasmb.template.replace(f"({i})", decomp_pattern_parts[i])
        response = self.generate_sentence(reasmb.template, decomp_pattern_parts)
        return response

    def extract_text_by_decomp(self, rule: list, text: str):
        # Construct a regular expression pattern from the given rule
        # This is the regex pattern
        pattern = ""
        for i in range(len(rule)):
            if rule[i] == "*":
                pattern += "(.*?)"
            else:
                pattern += re.escape(rule[i])
        pattern = "^" + pattern + "$"

        # Match the pattern against the text
        print(pattern)
        match = re.search(pattern, text)

        if match:
            # If a match is found, extract the captured groups and return as a list
            groups = match.groups()
            result = []
            j = 0
            for i in range(len(rule)):
                if rule[i] == "*":
                    result.append(groups[j].strip())
                    j += 1
                else:
                    result.append(rule[i])
            return result
        else:
            # If no match is found, return None
            return None

    def match_decomp(self, text: str, decomp: Decomp):
        decomp_pattern_parts = decomp.get_decomp_pattern_parts()
        return self.extract_text_by_decomp(rule=decomp_pattern_parts, text=text)

    def text_preprocess(self, text: str):
        synonyms = Synonym.objects.filter(bot=self.bot)
        words = [w for w in text.split(" ") if w]
        synonyms_list = []

        text_substr_list = []

        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                substr = " ".join(words[i:j])
                text_substr_list.append(substr)
        for substr in text_substr_list:
            for synonym in synonyms:
                if substr == synonym.word:
                    text = text.replace(substr, synonym.value)
                    synonyms_list.append(synonym)
                    break
        return text, synonyms_list

    def match_keyword(self, text: str, keyword: Keyword):
        output = None
        n = len(keyword.word.split())
        words = [w for w in text.split(" ") if w]
        if len(words) >= n:
            for i in range(len(words) - (n - 1)):
                phrase = " ".join(words[i : i + n])
                if keyword.word == phrase:
                    for decomp in keyword.decomp_set.order_by("-weight"):
                        results = self.match_decomp(text=text, decomp=decomp)
                        if not results:
                            continue
                        # postprocessing: subtitute words!
                        # results = [self._sub(words, self.posts) for words in results]
                        output = self.generate_response(
                            decomp=decomp, decomp_pattern_parts=results
                        )
                        if output:
                            return output
                        # if reasmb_template_words[0] == 'goto':
                        #     goto_key = reasmb_template_words[1]
                        #     keywords = Keyword.objects.filter(bot=self.bot).order_by('-weight').values_list('word', flat=True)
                        #     if keywords.exists():
                        #         if goto_key in keywords:
                        #             keyword = Keyword.objects.get(bot=self.bot, word=goto_key)
                        #             return self.match_keyword(words=words, keyword=keyword)
                        #         else:
                        #             raise ElizaServiceException(ELIZA_SERVICE_EXCEPTION.INVALID_GOTO_KEY)
                        # from results and reasmb -> do some cooking to return an ouput
        return output

    def output_postprocess(self, output: str, synonyms_list: list[str]):
        for synonym in synonyms_list:
            output = output.replace(synonym.value, synonym.word)
        return output

    def response(self, text: str):
        if self.bot:
            # punctuation cleanup
            # words = [w for w in text.split(' ') if w]

            keywords = Keyword.objects.filter(bot=self.bot).order_by("-weight")
            output = None
            text, synonyms_list = self.text_preprocess(text=text)
            if not keywords.exists():
                return DefaultMessage.default_message_objects.random_fallback(
                    bot=self.bot
                ).message
            for keyword in keywords:
                output = self.match_keyword(text=text, keyword=keyword)
                if output:
                    output = self.output_postprocess(
                        output=output, synonyms_list=synonyms_list
                    )
                    break
            return (
                output
                if output
                else DefaultMessage.default_message_objects.random_fallback(
                    bot=self.bot
                ).message
            )
        else:
            raise ElizaServiceException(ELIZA_SERVICE_EXCEPTION.BOT_NOT_SET_ERROR)
