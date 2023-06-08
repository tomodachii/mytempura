# import re


# def rule_to_regex(rule):
#     # Remove whitespace from the rule
#     rule = ''.join(rule.split())
#     # Replace * placeholders with a regex pattern that matches any non-space characters
#     regex_pattern = rule.replace('*', r'[^ ]+')
#     return regex_pattern


# def split_string(s):
#     pattern = r'(\*|\b\w+\b)'
#     return re.findall(pattern, s)


# rule = '* i dont know * sad *'
# a = split_string('* i dont * sad *')


# def parse_decomp(pattern):
#     pattern_words = pattern.split(' ')
#     output = []
#     phrase = ''
#     for word in pattern_words:
#         if word == '*':
#             if phrase:
#                 output.append(phrase.strip())
#                 phrase = ''
#             output.append(word)
#         else:
#             phrase = ' '.join([phrase, word])
#     if phrase:
#         output.append(phrase.strip())
#     return output


# a = parse_decomp(rule)
# print(a)


import re


def extract_matched_pattern(rule, text):
    # Construct a regular expression pattern from the given rule
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


rule = ["*", "I want to", "*"]
text = "last night I want to go to the garden"
output = extract_matched_pattern(rule, text)
print(output)
