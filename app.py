import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        clue = request.form["clue"]
        avoid = request.form["avoid words"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful boardgame partner playing codenames with me. You give me suggestions for clues I can give our teammate and you explain how your clue links to each target word and avoids each unwanted word."},
{"role": "user", "content": "We are playing a game of Codenames. Our goal is to think of a one-word clue that relates to some of our target words. You also say one number, which tells your teammtes how many target words are related to your clue. For example a clue should be in the format CLUE NUMBER, e.g. TRAVEL 3. This means there are 3 target words that relate to the word travel. While you are allowed to give a clue for only one target word, it's better to give two or more, so always aim to give clues that relate to 2 target words. We are also trying make our word avoid associations with any unwanted words. One rule you MUST follow is that the clues your provide CANNOT be any of the target words or the unwanted words. I am going to give you some examples of how to answer clues which you should follow. Make sure when you answer to give at least two candidates for good clues."},
{"role": "user", "content": "Here is the first example: Give me some clues that relate the following target words, but avoids the unwanted words. Target words: tree, page, book. Unwanted words: material."},
{"role": "assistant", "content": "Here are some clues I would give. 1.  'LEAF 3'. Leaf relates to tree as some trees have leaves on their branches. Leaf also relates to page and book as a read can leaf through the pages of a book. The clue LEAF avoids relation to the word material, as even though leaves can be used as a type of material the clue more strongly relates to the target words tree, page and book. I avoided suggesting a word like PAPER as that would relate to the concept of material. 2. 'READ 2'. Read refers to page and book as one can read both a page and a book. It avoids association with the word material."},
{"role": "user", "content": " Here is the second example: Give me some clues that relate the following target words, but avoids the unwanted words. Target words: bat, platypus, horse. Unwanted words: dwarf."},
{"role": "assistant", "content": "Consider some of these clues. 1. 'ANIMAL 3''. Animal relates to horse, platypus and bat as these are all examples of animals. The clue ANIMAL avoids relation to the word dwarf as dwarves are usually considered sentient creatures and hence not animals. I avoided suggesting a word like LIVING, CREATURE, or ALIVE as that would also relate to dwarf as a dwarf is a something that can be considered a creature, alive or living. 2. 'FUR 3'. Each of the target words are things that have fur, whereas the unwanted word (dwarf) does no have fur."},
{"role": "user", "content": " Here is the third example: Give me some clues that relate the following target words, but avoids the unwanted words. Target words: berlin, bond. Unwanted words: box."},
{"role": "assistant", "content": "Here are some clues I would suggest. 1.  'SPY 2''. Spy relates to Bond, as James Bond is a popular character who is a spy. Spy also relates to Berlin as many spys were used in Berlin during the cold war. The clue SPY also has no obvious relation to the word box, hence there is no risk of association with the unwanted word. 2. 'UNITE 2'. Unite relates to bond in the sense that bond means 'to tie together' which unite can also mean. Unite also relates to Berlin as east and west Berlin eventually united. Unite has no strong association with the word box."},
{"role": "user", "content": generate_prompt_target(clue, avoid)}],
            temperature=1,
        )
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    print(result)
    return render_template("index.html", result=result)


def generate_prompt_target(clue, avoid = ""):
    return """ Give me some clues that relates the following target words, but avoids the unwanted words. Target words: {0} Unwanted words: {1}.           
                       """.format(clue.capitalize(), avoid.capitalize())

