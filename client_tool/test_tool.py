# client_tool/test_tool.py
from conway_tool import get_generations_for_word, generate_random_words_and_find_highest_score

print("🧪 Testing: get_generations_for_word('monument')")
result1 = get_generations_for_word("monument")
print(result1)
print()

print("🧪 Testing: generate_random_words_and_find_highest_score()")
result2 = generate_random_words_and_find_highest_score()
print(result2)