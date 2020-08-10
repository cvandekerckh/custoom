from cover import create_cover
from parse_story import parse_story

FEMALE = "female"
MALE = "male"

output_filename = "albums/test_cover"
albums_path = "albums/cover"
custom_dict = {
    "location": "Jambes",
    "nickname": "Léa",
    "friend": "Alexandre",
    "dog": "Eva",
    "cake": "mousse au chocolat",
    "nickname_gender": FEMALE,
    "friend_gender": MALE,
    "cake_gender": FEMALE,
}
parsed_list = parse_story(custom_dict, story_file="albums/resume.txt")
create_cover(parsed_list, "Léâ", output_filename)
