"""Import "Selecting the Correct Sentences" (Objective General English, ch. 18)
into data/english/pronoun.json and schedule the quizzes from Day 35.

The chapter holds five revision exercises of 20 questions; the answer keys are
printed on the last two pages. Exercise B Q3 is skipped because the book prints
its options B and C with identical text, and the quiz UI tracks the selected
option by its text, so a duplicate would highlight two choices at once.

Existing questions and existing day plans are never modified: the bank is only
appended to, and only days that have no grammarQuizzes entry are given one.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "data" / "english" / "pronoun.json"
SCHEDULE = ROOT / "data" / "schedule-75.json"

EXPECTED_BANK_SIZE = 887  # pronoun_887 is the last question before this import
PROMPT = "Select the most suitable sentence in respect of meaning and grammatical correctness."

SKIP = {("B", 3)}  # book misprint: options B and C are identical

ANSWERS = {
    "A": "DDCDBBABAB ABABCDAABC",
    "B": "CADBABBCDC AADCDABDCD",
    "C": "CBDCDBCBAC DCCCABDDDC",
    "D": "CDDCDDDDAA CDCBCBCCBB",
    "E": "DDCBCABCDD BCCADBDCDD",
}

EXERCISES = {}

EXERCISES["A"] = [
    ["To be intelligent is more essential than being hard working.",
     "Being intelligent is more important than to be hard working.",
     "For one to be intelligent is more important than being hard working.",
     "Being intelligent is more essential than being hard working."],
    ["If he wins the prize I would be very happy.",
     "If he were to win the prize I'll be very happy.",
     "If he was to win the prize I would be very happy.",
     "If he were to win the prize I would be very happy."],
    ["Our school had won the match if only we have concentrated.",
     "Our school would have won the match if only we would have concentrated.",
     "Our school would have won the match if only we had concentrated.",
     "Our school had won the match if only we would have concentrated."],
    ["My sister had left for America last week.",
     "My sister has been left for America last week.",
     "My sister has left for America last week.",
     "My sister left for America last week."],
    ["It is high time he will start earning.",
     "It is high time he started earning.",
     "It is high time he starts earning.",
     "It is high time he has started earning."],
    ["It is a pleasure to see an alligator basking in the sunshine on a river bank as long as ninety feet.",
     "It is a pleasure to see an alligator as long as ninety feet basking in the sunshine on a river bank.",
     "It is a pleasure to see an alligator basking in the sunshine as long as ninety feet on a river bank.",
     "It is a pleasure to see an alligator basking as long as ninety feet in the sunshine on a river bank."],
    ["The villagers were enjoying winter evening around the fire.",
     "The villagers were enjoying winter evening around a fire.",
     "The villagers were enjoying winter evening around fire.",
     "The villagers were enjoying winter evening round fire."],
    ["When he had lost the book he searched it everywhere.",
     "When he lost the book he searched for it everywhere.",
     "When he lost the book he had searched for it everywhere.",
     "When he lost the book he searched it up everywhere."],
    ["This was the ideal book available in the market.",
     "This was most ideal book available in the market.",
     "This was a most ideal book available in the market.",
     "This was the most ideal book available in the market."],
    ["An one-eyed person was seen roaming about the streets.",
     "A one-eyed person was seen roaming about the streets.",
     "The one-eyed person was seen roaming about the streets.",
     "One-eyed person was seen roaming about the streets."],
    ["It is the duty of a house-wife to wait on the guest.",
     "It is the duty of a house-wife to wait for the guest.",
     "It is the duty of a house-wife to wait the guest.",
     "It is the duty of a house-wife to await the guest."],
    ["You are not working hard so your success is out of a question.",
     "You are not working hard so your success is out of the question.",
     "You are not working hard so your success is out of question.",
     "You are not working hard so your success is not out of the question."],
    ["You cannot win my confidence without ever believing me.",
     "You cannot win my confidence without never believing me.",
     "You cannot win my confidence without not believing me.",
     "You cannot win my confidence with ever believing me."],
    ["It is strange that you don't know swimming.",
     "It is strange that you don't know how to swim.",
     "It is strange that you don't know how to swimming.",
     "It is strange that you don't know to swim."],
    ["The receptionist must answer courteously the questions what are asked by the callers.",
     "The receptionist must answer courteously the questions of all the callers.",
     "The receptionist should answer courteously the questions of all the callers.",
     "The receptionist courteously should answer the question of callers."],
    ["As he was sick, he was quite enthusiastic.",
     "Since he was sick, he was quite enthusiastic.",
     "As sick he was, he was quite enthusiastic.",
     "Sick as he was, he was quite enthusiastic."],
    ["Both my brother and my sister love me but I should say that she loves me more than he.",
     "Both my brother and my sister love me but I should say that she loves more than him.",
     "Both my brother and my sister love me but I should say that she loves me more than him.",
     "Both my brother and my sister love me but I should say that she loves I more than he."],
    ["I am an optimist and therefore I generally differ with you.",
     "I am an optimist and therefore I generally differ from you.",
     "I am an optimist and therefore I generally differ in you.",
     "I am an optimist and therefore I generally differ you."],
    ["Neena can do it alone and no body else can do it.",
     "Neena can do it and nobody else can do it.",
     "Neena alone can do it and nobody else can do it.",
     "Alone Neena can do it and no body else can do it."],
    ["Due to want of rain the wells have gone dry.",
     "Because of want of rain the wells have gone dry.",
     "For want of rain the wells have gone dry.",
     "Owing to want of rain the wells have gone dry."],
]

EXERCISES["B"] = [
    ["As the train which was my usual was missing I had to travel.",
     "Having missed the train which I usually catch and had to travel.",
     "I missed the train which I usually catch and had to travel by the next.",
     "I missed not only the train which I usually catch but had to travel on the next."],
    ["He may be poor now but he appears to have been rich in his youth.",
     "He may be poor now but he appears to be rich in his youth.",
     "He may be poor now but he appears being rich in his youth.",
     "He may be poor now but he appears to rich in his youth."],
    ["By June next year Ajay will be twenty years working in the office.",
     "Till June next year Ajay will work in the office for twenty years.",
     "Till June next year Ajay will work in the office for twenty years.",
     "By June next year Ajay will have been working in the office for twenty years."],
    ["He went to the wholesale market and bought the cheap rations.",
     "He went to the wholesale market and bought the rations cheap.",
     "He went to the wholesale market and bought rations cheaply.",
     "He went to the wholesale market and cheaply bought rations."],
    ["I went yesterday to the bank to collect the pass book.",
     "I went to the bank to collect the pass book.",
     "Yesterday to collect the pass book I went to the bank.",
     "To collect the pass book yesterday I went to the bank."],
    ["The principal appointed him as a peon in the college.",
     "The principal appointed him a peon in the college.",
     "As a peon the Principal appointed him in the college.",
     "The principal as a peon appointed him in the college."],
    ["The team is confident to win the match.",
     "The team is confident of winning the match.",
     "The team is confident of win the match.",
     "The team is confident for winning the match."],
    ["He is one of the best policeman who has ever lived.",
     "He is one of the best policeman who have ever lived.",
     "He is one of the best policemen that have ever lived.",
     "He is one of the best policeman that has ever lived."],
    ["My sister is the poet and the philosopher.",
     "My sister is a poet and the philosopher.",
     "My sister is a poet and a philosopher.",
     "My sister is a poet and philosopher."],
    ["Meena seldom or ever refuses an invitation.",
     "Meena seldom or always refuses an invitation.",
     "Meena seldom or never refuses an invitation.",
     "Meena seldom if never refuses an invitation."],
    ["There is no meaning in what you say.",
     "There is no meaning in that you say.",
     "There is no meaning as to what you say.",
     "There is no meaning that you say."],
    ["I hope you will excuse my leaving early.",
     "I hope you will excuse me leaving early.",
     "I hope you will excuse mine leaving early.",
     "I hope you will excuse leaving early."],
    ["I am ready to say this at her face.",
     "I am ready to say this on her face.",
     "I am ready to say this in her face.",
     "I am ready to say this to her face."],
    ["On account of shortage of time both of them cannot finish their work.",
     "On account of shortage of time none of them can finish their work.",
     "On account of shortage of time neither of them can finish his work.",
     "On account of shortage of time neither of them cannot finish his work."],
    ["Many problems are staring at my face.",
     "Many problems are staring in my face.",
     "Many problems are staring me into my face.",
     "Many problems are staring me in my face."],
    ["The cow does not eat anything else. It lives on grass and leaves.",
     "The cow does not eat anything else. It lives at grass and leaves.",
     "The cow does not eat anything else. It lives in grass and leaves.",
     "The cow does not eat anything else. It lives for grass and leaves."],
    ["As one of his arms was amputated on account of an accident, the company will compensate the loss to him.",
     "As one of his arms was amputated on account of an accident, the company will compensate him for the loss.",
     "As one of his arms was amputated on account of an accident, the company will compensate him in the loss.",
     "As one of his arms was amputated on account of an accident, the company will compensate his loss."],
    ["Now I have cancelled my meeting though I was to go there.",
     "Now I have cancelled my meeting though I have to go there.",
     "Now I have cancelled my meeting though I am to go there.",
     "Now I have cancelled my meeting though I was to have gone there."],
    ["She insisted on me to stay there.",
     "She insisted on me staying there.",
     "She insisted on my staying there.",
     "She insisted in my staying there."],
    ["You can meet my father only when he goes to prison.",
     "You can meet father only when he goes into prison.",
     "You can meet my father only when he goes in prison.",
     "You can meet my father only when he goes to the prison."],
]

EXERCISES["C"] = [
    ["Since the dividend being declared then the notices were prepared for mailing.",
     "No sooner had the dividend being declared then the notices were prepared for mailing.",
     "No sooner had the dividend been declared than the notices were prepared for mailing.",
     "Scarcely had the dividend being declared than the notices were sent out."],
    ["He did not report for work today. He must has gone to the party.",
     "He did not report for work today. He must have gone to the party.",
     "He did not report for work today. He must go to the party.",
     "He did not report for work today. He must had gone to the party."],
    ["She is not as wise as his brother.",
     "She is not equally wise as his brother.",
     "She is not as wise like his brother.",
     "She is not so wise as his brother."],
    ["There will be a meeting in the long room at 4 o'clock of all the boys who play cricket and football.",
     "There will be in the long room at 4 o'clock a meeting of all the boys who play cricket and football.",
     "In the long room at 4 o'clock there will be a meeting of all the boys who play cricket and football.",
     "There will be a meeting of all the boys who play cricket and football at 4 o'clock."],
    ["The teacher made it a point to explain him the situation.",
     "The teacher made it a point to explain the situation him.",
     "The teacher made it a point explain him about the situation.",
     "The teacher made it a point to explain the situation to him."],
    ["The landlady made the servant to run to market to fetch her sweets.",
     "The landlady made the servant run to market to fetch her sweets.",
     "The landlady made to the servant to run to market to fetch her sweets.",
     "The landlady made to the servant run to market to fetch her sweets."],
    ["The audience looked at him while he spoke.",
     "The audience looked at him while he had spoken.",
     "The audience looked at him while he was speaking.",
     "The audience looked at him while he had been speaking."],
    ["Your answers are better than Mohan.",
     "Your answers are better than Mohan's.",
     "Your answers are better than those of Mohan's.",
     "Your answers are better than answered by Mohan."],
    ["Everybody knows that Rahul is nothing else but a cheat.",
     "Everybody knows that Rahul is nothing else than a cheat.",
     "Everybody knows that Rahul is nothing else except a cheat.",
     "Everybody knows that Rahul is nothing but for a cheat."],
    ["The manager asked him how he would avail this opportunity.",
     "The manager asked him how he would avail of this opportunity.",
     "The manager asked him how he would avail himself of this opportunity.",
     "The manager asked him how he would avail himself this opportunity."],
    ["The teacher asked the students to thoroughly study this book.",
     "The teacher asked the students thoroughly to study this book.",
     "The teacher asked thoroughly the students to study this book.",
     "The teacher asked the students to study thoroughly this book."],
    ["The important lessons are following.",
     "The important lessons are as following.",
     "The important lessons are as follows.",
     "The important lessons are as follow."],
    ["The teacher asked the student with a frown on his face to leave the room.",
     "The teacher asked with a frown on his face the student to leave the room.",
     "With a frown on his face the teacher asked the student to leave the room.",
     "The teacher asked the student to leave the room with a frown on his face."],
    ["The typists had corrected the errors had they known that the supervisors would have seen the report.",
     "The supervisors reprimanded the typists whom they believed had made careless errors.",
     "The errors in the typed reports were so numerous that they could hardly be overlooked.",
     "The typist would have corrected the errors had they known that the supervisor would see the reports."],
    ["He carried the little child and me on his shoulders.",
     "It was me that gave away the prizes.",
     "All what he said had no effect on me.",
     "They who did this thing should be punished."],
    ["In order to solve the murder case a C.B.I. officer is looking about the matter.",
     "It is high time that you went to bed.",
     "Though he looked innocent he turned into be cheat.",
     "The majority of the workers was divided on the issue."],
    ["You cannot win my confidence until you are sincere.",
     "When he lost the book he searched it everywhere.",
     "She was intent to harm her friends.",
     "I have not met my friend for the last five days."],
    ["He started to work hard lest he might starve in old age.",
     "He started working hard lest he should not starve in old age.",
     "He started to work hard lest he should starve in old age.",
     "He started working hard lest he should starve in old age."],
    ["If I had money I would have bought the new house tomorrow.",
     "If I had had money I would have bought a new house tomorrow.",
     "If I had had money I would buy a new house tomorrow.",
     "If I had money I would buy a new house tomorrow."],
    ["Taking my food I left for college.",
     "While I was taking my food I left for college.",
     "Having taken my food I left for college.",
     "Taking my food I shall leave for college."],
]

EXERCISES["D"] = [
    ["The harassed wife shot herself after bidding her husband the last good bye with a gun.",
     "The harassed wife with a gun shot herself after bidding her husband the last good bye.",
     "The harassed wife shot herself with a gun after bidding her husband the last good bye.",
     "With a gun the harassed wife shot herself after bidding her husband the last good bye."],
    ["He repeated the essay word by word.",
     "Being a rainy day he did not go out.",
     "She is senior but not more efficient than I.",
     "All his friends are very sincere."],
    ["She had waited long before her husband had returned.",
     "She waited long when her husband returned.",
     "She had waited long after her husband returned.",
     "She had waited long before her husband returned."],
    ["Even if intelligent he may be he can't succeed.",
     "If intelligent he may be he can't succeed.",
     "However intelligent he may be he can't succeed.",
     "Even intelligent he may be he can't pass."],
    ["Had I been you I would help him.",
     "If I had been you I would help him.",
     "Should I you I would help him.",
     "Were I you I would help him."],
    ["I realised later on that he cheated me.",
     "I had realised later that he cheated me.",
     "I had realised later that he had cheated me.",
     "I realised later on that he had cheated me."],
    ["They arrived early because they may not miss the train.",
     "They arrived early that they may not miss the train.",
     "They arrived early when they miss the train.",
     "They arrived early so that they might not miss the train."],
    ["I was rather impressed by the manner of the speaker than by his matter.",
     "I was impressed by the manner of the speaker rather than by his matter.",
     "Rather I was impressed by the manner of the speaker than by his matter.",
     "I was impressed rather by the manner of the speaker than by his matter."],
    ["He is vain as though he were a millionaire.",
     "She acted as if her mother asked her to do.",
     "She carried the child carefully lest it should not fall.",
     "I don't relish the food whose taste is sour."],
    ["The nature of my brother is the same as yours.",
     "This is one of those novels which is admired all over the world.",
     "He is such a friend that will sacrifice for me.",
     "I wish he comes everyday."],
    ["So quickly he returned from market that I was surprised.",
     "So quickly did he returned from the market that I was surprised.",
     "So quickly did he return from the market that I was surprised.",
     "So quickly did he return from the market that I had been surprised."],
    ["Would you help my brother I shall get you a decent job.",
     "Had you helped my brother I shall get you a decent job.",
     "Did you help my brother I shall get you a decent job.",
     "Should you help my brother I'll get you a decent job."],
    ["A summon has been served on him.",
     "A summons have been served on him.",
     "A summons has been served on him.",
     "A summon have been served to him."],
    ["You are not allowed to enter into the house.",
     "You are not allowed to enter the house.",
     "You are not allowed to enter in the house.",
     "You are not allowed to enter on the house."],
    ["Little care was needed to avert the accident.",
     "The little care was needed to avert the accident.",
     "A little care was needed to avert the accident.",
     "Less care was needed to avert the accident."],
    ["Could you please help me with any money?",
     "Could you please help me with some money?",
     "Would you please help me with any money?",
     "Can you please help me with some money?"],
    ["Leena is a most intelligent student in the class.",
     "Leena is the most intelligent student.",
     "Leena is a most intelligent student.",
     "Leena is most intelligent student in the class."],
    ["She is more intelligent than any other boy in the class.",
     "She is more intelligent than any girl in the class.",
     "She is more intelligent than any other girl in the class.",
     "She is the most intelligent than any other girl in the class."],
    ["The teaching staff must take their lectures regularly when are asked by the Principal.",
     "The teaching staff would have taken lectures regularly had they known that the Principal would know about it.",
     "The teaching staff had taken the lectures regularly had they known that the Principal would come to know about it.",
     "Many irregularities were found in their lectures by the Principal and he could not be disregarded them."],
    ["Anita was sitting with her husband on the steps of the temple with her lap full of newspapers when Bunty and Bitto came up.",
     "Anita with her lap full of newspapers was sitting with her husband on the steps of the temple when Bunty and Bitto came up.",
     "With her lap full of newspapers Anita was sitting with her husband on the steps of the temple when Bunty and Bitto came up.",
     "Anita was sitting with her husband on the steps of the temple when Bunty and Bittu came up with her lap full of newspapers."],
]

EXERCISES["E"] = [
    ["As he is careless he will not hear what the teacher says.",
     "As he is careless he will not hear to what the teacher says.",
     "As he is careless he will not listen what the teacher says.",
     "As he is careless he will not listen to what the teacher says."],
    ["Shikha has been known by me for five years.",
     "Shikha is known by me for five years.",
     "Shikha is known to me for five years.",
     "Shikha has been known to me for five years."],
    ["As soon as holidays be begin than this beach will become very crowded.",
     "Since the holidays being started this beach becomes very crowded.",
     "As soon as the holidays begin, this beach becomes very crowded.",
     "No sooner did the holiday begin than this beach will become very crowded."],
    ["You must aspire for the post according to your capability.",
     "You must aspire to the post according to your capability.",
     "You must aspire after the post according to your capability.",
     "You must aspire the post according to your capability."],
    ["A good teacher provides a student all the useful information.",
     "A good teacher provides to a student all the useful information.",
     "A good teacher provides a student with all the useful information.",
     "A good teacher provides to student with all the useful information."],
    ["Nobody will want to play in his team if he does not treat people kindly.",
     "If he will not treat people kindly nobody will want to play in his team.",
     "Nobody will treat people kindly if he does not want to play in his team.",
     "Nobody will want to treat people if he does not play in his team kindly."],
    ["The priest read to the dying man couplets from the scriptures.",
     "The priest read the dying man the couplets from the scriptures.",
     "The priest read for the dying man the couplets from the scriptures.",
     "The priest read the couplets from the scriptures for the dying man."],
    ["I do not understand to whom she is talking.",
     "I do not understand whom she is talking about.",
     "I do not understand who she is talking to.",
     "I do not understand whom she is talking."],
    ["The boy regretted that with a plastered leg he had spent a greater part of his vacation in the chair.",
     "The boy regretted that he had spent a greater part of his vacation in the chair with a plastered leg.",
     "With a plastered leg, the boy regretted that he had spent a greater part of his vacation in the chair.",
     "The boy with a plastered leg regretted that he had spent a greater part of his vacation in the chair."],
    ["In thirty-seven bomb blasts, fortunately only five lives were lost.",
     "In thirty-seven bomb blasts, only five lives were fortunately lost.",
     "In fortunately thirty-seven bomb blasts only five lives were lost.",
     "Fortunately, in thirty-seven bomb blasts, only five lives were lost."],
    ["She is annoyed with you. You ought not to tell her secrets to her mother.",
     "She is annoyed with you. You ought not to have told her secrets to her mother.",
     "She is annoyed with you, you ought to tell her secrets to her mother.",
     "She is annoyed with you. You ought to have told her secrets to her mother."],
    ["It is the best which she could do for me.",
     "It is the best what she could do for me.",
     "It is the best that she could do for me.",
     "It is best that she could for me."],
    ["The early age of three or four years, would begin our first recollection of the world, for many of us.",
     "Our first recollection of the world, for many of us, would be early age of three or four years.",
     "For many of us, our first recollection of the world is from the early age of only three or four years.",
     "For many of us, our first recollection of the world has been the early age of only three or four years."],
    ["Now-a-days singing is a very profitable profession.",
     "Now-a-days the singing is a very profitable profession.",
     "Now-a-days singing is very profitable profession.",
     "Now-a-days the singing is very profitable profession."],
    ["The report was useless to them because there was no needed information.",
     "Since the report lacked needed information would have not been useful to them.",
     "Since the report did not control the needed information it was not really useful to them.",
     "Since the report lacked the needed information it was of no use to them."],
    ["Men are rather impressed by beauty than by character.",
     "Men are impressed rather by beauty than by character.",
     "Rather men are impressed by beauty than by character.",
     "Men are impressed by beauty than by character."],
    ["So quickly she ran upstairs that she over took me.",
     "So quickly did she ran upstairs that she over took me.",
     "She ran so quickly upstairs that she had overtaken me.",
     "So quickly did she run upstairs that she overtook me."],
    ["He wasn't rich by any means, although he never turned down anyone who needed help.",
     "Being not rich by any means he never turned away, anyone who needed help.",
     "He wasn't rich by any means but he never turned away anyone who needed help.",
     "Since he wasn't rich by any means, he never turned away anyone who needed help."],
    ["Some people consider Karan the valorous hero of all the characters in the Mahabharata.",
     "Some people consider Karan as the most valorous hero of all the characters in the Mahabharata.",
     "Some people consider Karan the most valorous hero of all the other characters in the Mahabharata.",
     "Some people consider Karan the most valorous hero of all the characters in the Mahabharata."],
    ["Neither she comes nor she writes.",
     "Neither does she comes nor she writes.",
     "Neither does she come nor writes.",
     "Neither does she come nor does she write."],
]


def build_questions():
    out = []
    for letter in "ABCDE":
        key = ANSWERS[letter].replace(" ", "")
        blocks = EXERCISES[letter]
        if len(blocks) != 20 or len(key) != 20:
            raise SystemExit(f"exercise {letter}: expected 20 questions and 20 answers")
        for number, options in enumerate(blocks, 1):
            if (letter, number) in SKIP:
                continue
            if len(options) != 4:
                raise SystemExit(f"{letter}{number}: expected 4 options")
            if len(set(options)) != 4:
                raise SystemExit(f"{letter}{number}: duplicate option text")
            out.append((options, options["ABCD".index(key[number - 1])]))
    return out


def indent_block(obj, spaces):
    """Serialise obj at the surrounding file's indentation."""
    pad = " " * spaces
    body = json.dumps(obj, ensure_ascii=False, indent=2)
    return "\n".join(pad + line for line in body.split("\n"))


def append_to_bank(questions):
    """Insert the new entries before the closing bracket, leaving the rest of the
    file byte-for-byte as it was."""
    raw = BANK.read_text(encoding="utf-8")
    bank = json.loads(raw)
    if len(bank) != EXPECTED_BANK_SIZE:
        raise SystemExit(f"bank has {len(bank)} questions, expected {EXPECTED_BANK_SIZE}")

    start = len(bank)
    entries = [
        {
            "id": f"pronoun_{start + offset + 1}",
            "question": PROMPT,
            "options": options,
            "correctAnswer": answer,
        }
        for offset, (options, answer) in enumerate(questions)
    ]

    close = raw.rstrip().rfind("]")
    head = raw[:close].rstrip()
    if not head.endswith("}"):
        raise SystemExit("unexpected shape at the end of pronoun.json")

    added = ",\n" + ",\n".join(indent_block(e, 2) for e in entries) + "\n"
    updated = head + added + raw[close:]

    check = json.loads(updated)
    if check[:start] != bank:
        raise SystemExit("existing questions changed - aborting")
    if len(check) != start + len(entries):
        raise SystemExit("unexpected question count after append")

    BANK.write_text(updated, encoding="utf-8")
    print(f"pronoun.json: appended {len(entries)} questions "
          f"({entries[0]['id']} .. {entries[-1]['id']}), total {len(check)}")
    return start


def schedule_quizzes(start_index, total):
    raw = SCHEDULE.read_text(encoding="utf-8")
    original = json.loads(raw)

    chunks, remaining, offset, day = [], total, start_index, 35
    while remaining > 0:
        size = min(25, remaining)
        chunks.append((day, offset, size))
        remaining -= size
        offset += size
        day += 1

    for position, (day, offset, size) in enumerate(chunks):
        plan = next(p for p in original["plans"] if p["day"] == day)
        if plan["english"].get("grammarQuizzes"):
            raise SystemExit(f"day {day} already has grammarQuizzes - refusing to overwrite")

        entry = {
            "topic": "pronoun",
            "label": f"SENTENCE — Set {5 + position}",
            "questions": size,
            "duration": 10,
            "from": offset,
        }

        # locate this day's english block, then the grammarQuiz line inside it
        day_at = raw.find(f'"day": {day},')
        if day_at < 0:
            raise SystemExit(f"day {day} not found in the schedule file")
        english_at = raw.find('"english": {', day_at)
        anchor = raw.find('        "grammarQuiz":', english_at)
        if not english_at < anchor < raw.find('"reasoning":', english_at):
            raise SystemExit(f"day {day}: could not place the quiz inside the english block")

        block = indent_block([entry], 8)
        raw = raw[:anchor] + f'        "grammarQuizzes": {block.lstrip()},\n' + raw[anchor:]
        print(f"day {day}: {size} questions from index {offset}  ({entry['label']})")

    expected = json.loads(SCHEDULE.read_text(encoding="utf-8"))
    for position, (day, offset, size) in enumerate(chunks):
        plan = next(p for p in expected["plans"] if p["day"] == day)
        plan["english"]["grammarQuizzes"] = [{
            "topic": "pronoun",
            "label": f"SENTENCE — Set {5 + position}",
            "questions": size,
            "duration": 10,
            "from": offset,
        }]
    if json.loads(raw) != expected:
        raise SystemExit("schedule changed beyond the new quizzes - aborting")

    SCHEDULE.write_text(raw, encoding="utf-8")


def main():
    questions = build_questions()
    start = append_to_bank(questions)
    schedule_quizzes(start, len(questions))


if __name__ == "__main__":
    main()
