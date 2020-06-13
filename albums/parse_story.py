import re

MALE = "male"
FEMALE = "female"


# Syntax
STATE_TAG = "@"
FIGURE_TAG = f"{STATE_TAG}Figure"
DESCRIPTION_TAG = f"{STATE_TAG}Description"
TEXT_TAG = f"{STATE_TAG}Texte"
TAG_SEPARATOR = ":"
GENDER_TAG = {
    FEMALE: "$",
    MALE: "&"
}
CONDITIONAL_RE = r'\$\((\w+)\)(\w+)=(\w+)'

PENDING = 0
FIGURE_MODE = 1
TEXT_MODE = 2


def conditional_replace(match_object, gender_dict):
    assert match_object.group(2) in gender_dict
    gender = gender_dict[match_object.group(2)]
    if match_object.group(3)==gender:
        return match_object.group(1)
    else:
        return ""


def detect_new_state(line):
    if line.startswith(STATE_TAG):
        tag = line.split(" ")[0]
        assert tag in [FIGURE_TAG, DESCRIPTION_TAG, TEXT_TAG]
        if tag == FIGURE_TAG:
            return FIGURE_MODE
        elif tag == TEXT_TAG:
            return TEXT_MODE
        else:
            return False
    else:
        return False


def create_new_part(parsed_story, line):
    figure_name = line.split(TAG_SEPARATOR)[1]
    figure_name = figure_name.strip()
    parsed_story[figure_name] = []
    return parsed_story, figure_name


def add_text_line(parsed_story, figure_name, line):
    assert figure_name in parsed_story
    parsed_story[figure_name].append(line)
    return parsed_story


def parse_line(line, custom_dict, gender_dict):
    line = line % custom_dict  # replace by custom variable
    gender_replace = lambda x: conditional_replace(x, gender_dict)
    line = re.sub(CONDITIONAL_RE, gender_replace, line)
    return line


def parse_story(story_file, custom_dict, gender_dict):
    state = PENDING
    parsed_story = {}
    figure_name = None
    with open(story_file) as f:
        for line in f:
            assert state in [PENDING, FIGURE_MODE, TEXT_MODE]
            new_state = detect_new_state(line)
            # Detect first figure
            if state == PENDING:
                if new_state == FIGURE_MODE:
                    parsed_story, figure_name = create_new_part(parsed_story, line)
                    state = new_state
                else:
                    pass

            # Figure mode
            elif state == FIGURE_MODE:
                if new_state == TEXT_MODE:
                    state = new_state
                elif new_state == FIGURE_MODE:
                    parsed_story, figure_name = create_new_part(parsed_story, line)
                else:
                    pass

            # Text mode
            elif state == TEXT_MODE:
                if new_state == FIGURE_MODE:
                    parsed_story, figure_name = create_new_part(parsed_story, line)
                    state = new_state
                else:
                    line = parse_line(line, custom_dict, gender_dict)
                    parsed_story = add_text_line(parsed_story, figure_name, line)
    return parsed_story




custom_dict = {
    "location": "Dinant",
    "nickname": "Léa",
    "friend": "Didier",
    "dog": "Patmolle",
    "cake": "glace"
}

gender_dict = {
    "nickname": FEMALE,
    "friend": MALE,
    "cake": FEMALE,
}

parsed_story = parse_story("histoire.txt", custom_dict, gender_dict)
print(parsed_story)
