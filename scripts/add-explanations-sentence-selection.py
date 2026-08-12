"""Add a one-line grammar note to each sentence-selection question
(pronoun_888 .. pronoun_986). The source book prints only a letter key, so these
notes are written from the grammar point each question turns on.

Only the entries added by import-sentence-selection.py are rewritten; everything
before pronoun_888 is left byte-for-byte untouched.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "data" / "english" / "pronoun.json"
FIRST = "pronoun_888"
LAST = "pronoun_986"

NOTES = {
    # Revision Exercise (A)
    "pronoun_888": "Both halves of a comparison must take the same form, so 'Being intelligent' pairs with 'being hard working'.",
    "pronoun_889": "An improbable condition takes 'were to' in the if-clause and 'would' in the main clause.",
    "pronoun_890": "An unfulfilled past condition takes the past perfect in the if-clause and 'would have + past participle' in the main clause.",
    "pronoun_891": "'Last week' is a finished past time, so the simple past is required rather than any perfect tense.",
    "pronoun_892": "After 'It is high time', the verb goes into the past subjunctive.",
    "pronoun_893": "'As long as ninety feet' describes the alligator, so it must stand next to that noun.",
    "pronoun_894": "The villagers sat around one particular fire, so the definite article 'the' is needed.",
    "pronoun_895": "'Search for' is used when you are looking for something; 'search' alone means to examine a place or a person.",
    "pronoun_896": "'Ideal' is an absolute adjective and cannot be graded with 'most'.",
    "pronoun_897": "'One' begins with a consonant sound, so it takes 'a' and not 'an'.",
    "pronoun_898": "'Wait on' means to serve or attend to someone, which is the sense required here.",
    "pronoun_899": "'Out of the question' is the fixed idiom meaning impossible.",
    "pronoun_900": "'Without' is already negative, so no second negative may follow it.",
    "pronoun_901": "When it refers to a skill, 'know' takes 'how to' followed by the base verb.",
    "pronoun_902": "'Should' expresses the expected duty, and 'the questions of all the callers' avoids the wrong relative 'what'.",
    "pronoun_903": "This concessive pattern puts the adjective first: adjective + as + subject + verb.",
    "pronoun_904": "The comparison is between two subjects, so the nominative 'he' is required — she loves me more than he does.",
    "pronoun_905": "You differ with a person when you disagree; 'differ from' means to be unlike.",
    "pronoun_906": "'Alone' becomes redundant once 'nobody else' has been said.",
    "pronoun_907": "'For want of' is the idiom meaning 'because of a lack of'.",
    # Revision Exercise (B)
    "pronoun_908": "Both verbs need the same subject, and 'travel by the next' is the natural idiom.",
    "pronoun_909": "The perfect infinitive 'to have been' places the wealth earlier in time than 'appears'.",
    "pronoun_910": "'Buy cheap' is a fixed expression in which 'cheap' works adverbially.",
    "pronoun_911": "The sentence keeps its natural order with the time adverb next to the verb; the other versions invert it awkwardly.",
    "pronoun_912": "'Appoint' takes a direct object and a complement without 'as'.",
    "pronoun_913": "'Confident' is followed by 'of' and then a gerund.",
    "pronoun_914": "'One of the best' takes a plural noun, and the relative clause agrees with that plural.",
    "pronoun_915": "One article is enough because both nouns describe the same person.",
    "pronoun_916": "'Seldom or never' is the established idiom.",
    "pronoun_917": "After the preposition 'in', 'what' serves as the relative pronoun meaning 'the thing that'.",
    "pronoun_918": "A gerund after 'excuse' takes a possessive adjective, not an object pronoun.",
    "pronoun_919": "'To one's face' is the idiom for saying something openly to somebody.",
    "pronoun_920": "'Neither' is singular, so it takes a singular verb and a singular pronoun, and it already carries the negative.",
    "pronoun_921": "'Stare somebody in the face' keeps the person as the object of the verb.",
    "pronoun_922": "'Live on' is the idiom for the food a creature subsists on.",
    "pronoun_923": "'Compensate' takes the person as its object, followed by 'for' the thing lost.",
    "pronoun_924": "'Was to have gone' shows an arrangement that was never carried out.",
    "pronoun_925": "'Insist on' is followed by a gerund with a possessive adjective.",
    "pronoun_926": "'Go to the prison' means visiting the building, whereas 'go to prison' would mean being imprisoned.",
    # Revision Exercise (C)
    "pronoun_927": "'No sooner' inverts the auxiliary and pairs with 'than', and the passive needs 'been declared'.",
    "pronoun_928": "A deduction about the past takes 'must have' with the past participle.",
    "pronoun_929": "In a negative comparison, 'so ... as' is preferred to 'as ... as'.",
    "pronoun_930": "Placing the adverbials first keeps 'a meeting of all the boys' together and removes the ambiguity.",
    "pronoun_931": "'Explain' takes the thing explained as its object and the person after 'to'.",
    "pronoun_932": "After the causative 'make', the bare infinitive is used.",
    "pronoun_933": "'While' introduces an action in progress, which calls for the past continuous.",
    "pronoun_934": "Answers are being compared with answers, so the possessive 'Mohan's' is required.",
    "pronoun_935": "'Nothing else but' is the fixed idiom.",
    "pronoun_936": "'Avail' is used reflexively and followed by 'of'.",
    "pronoun_937": "The adverb follows the verb it modifies instead of splitting the infinitive.",
    "pronoun_938": "'As follows' never changes its form, however many items are listed.",
    "pronoun_939": "The frown belongs to the teacher, so the phrase must stand next to 'the teacher'.",
    "pronoun_940": "The 'so ... that' construction is complete here, while the other options misuse the conditional or the relative pronoun.",
    "pronoun_941": "As the object of 'carried', the pronoun takes its objective form 'me'.",
    "pronoun_942": "After 'It is high time', the past subjunctive 'went' is used.",
    "pronoun_943": "A period running up to the present takes the present perfect with 'for'.",
    "pronoun_944": "'Lest' already carries the negative and is followed by 'should'.",
    "pronoun_945": "An unreal present condition takes the past tense with 'would' and the base verb.",
    "pronoun_946": "The perfect participle 'having taken' shows the meal was finished before he left.",
    # Revision Exercise (D)
    "pronoun_947": "'With a gun' modifies 'shot', so it must stand beside that verb.",
    "pronoun_948": "Only this option is free of error: 'word by word' should be 'word for word', 'Being a rainy day' dangles, and 'senior' takes 'to' rather than 'than'.",
    "pronoun_949": "The earlier action takes the past perfect and the later one the simple past.",
    "pronoun_950": "'However' followed by the adjective is the correct concessive form.",
    "pronoun_951": "The subjunctive 'were' with inversion states an unreal present condition.",
    "pronoun_952": "The cheating happened before the realisation, so it takes the past perfect.",
    "pronoun_953": "A purpose clause after a past main verb takes 'so that' with 'might'.",
    "pronoun_954": "'Rather' stands immediately before the phrase that 'than' contrasts it with.",
    "pronoun_955": "'As though' introduces an unreal comparison and takes the subjunctive 'were'.",
    "pronoun_956": "'The same as' is the correct pairing for this comparison.",
    "pronoun_957": "When 'so + adverb' opens the sentence, the auxiliary is inverted and the main verb stays in its base form.",
    "pronoun_958": "'Should' with inversion expresses an open condition about the future.",
    "pronoun_959": "'Summons' in this legal sense is singular and takes a singular verb.",
    "pronoun_960": "'Enter' is transitive and needs no preposition after it.",
    "pronoun_961": "'A little' means some, the positive sense needed here; 'little' alone would mean hardly any.",
    "pronoun_962": "A polite request takes 'some' rather than 'any'.",
    "pronoun_963": "'A most' means 'very'; adding 'in the class' would call for the superlative 'the most'.",
    "pronoun_964": "Comparing a girl with the rest of her own group requires 'any other'.",
    "pronoun_965": "The unreal past condition takes 'had known' with 'would have taken'.",
    "pronoun_966": "The lap full of newspapers is Anita's, so the phrase must stand next to her name.",
    # Revision Exercise (E)
    "pronoun_967": "'Listen' means to pay attention and is followed by 'to'.",
    "pronoun_968": "A state continuing over a period takes the present perfect, and one is known 'to' a person.",
    "pronoun_969": "A general truth takes the simple present in both clauses.",
    "pronoun_970": "'Aspire' takes 'to' before the thing desired.",
    "pronoun_971": "The pattern is 'provide somebody with something'.",
    "pronoun_972": "The if-clause takes the simple present while the main clause takes the future.",
    "pronoun_973": "'Read' can take the indirect object before the direct object without a preposition.",
    "pronoun_974": "'Talk' needs its preposition 'to', which is kept at the end of the clause.",
    "pronoun_975": "The plastered leg belongs to the boy, so the phrase must stand next to 'the boy'.",
    "pronoun_976": "'Fortunately' comments on the whole sentence, so it belongs at the beginning.",
    "pronoun_977": "'Ought not to have told' expresses a past action that should not have happened.",
    "pronoun_978": "After a superlative, the relative pronoun used is 'that'.",
    "pronoun_979": "A recollection dates 'from' an age, and this version keeps the subject and verb in agreement.",
    "pronoun_980": "A gerund used in a general sense takes no article, while the countable 'profession' takes 'a'.",
    "pronoun_981": "After the 'Since' clause, the main clause still needs its own subject and verb — 'it was of no use to them'.",
    "pronoun_982": "'Rather' stands directly before the phrase that 'than' contrasts it with.",
    "pronoun_983": "The inversion after 'so quickly' leaves the main verb in its base form 'run'.",
    "pronoun_984": "The two clauses contrast, so 'but' is the right connective and 'turn away' the right phrasal verb.",
    "pronoun_985": "'Consider' takes no 'as', and the superlative already covers all the characters.",
    "pronoun_986": "'Neither ... nor' at the head of a sentence requires inversion in both halves.",
}


def indent_block(obj, spaces):
    pad = " " * spaces
    return "\n".join(pad + line for line in json.dumps(obj, ensure_ascii=False, indent=2).split("\n"))


def main():
    raw = BANK.read_text(encoding="utf-8")
    bank = json.loads(raw)

    ids = [q["id"] for q in bank]
    first, last = ids.index(FIRST), ids.index(LAST)
    if last != len(bank) - 1:
        raise SystemExit(f"{LAST} is not the final question in the bank")

    targets = bank[first:]
    missing = [q["id"] for q in targets if q["id"] not in NOTES]
    if missing:
        raise SystemExit(f"no note written for: {', '.join(missing)}")
    if len(NOTES) != len(targets):
        raise SystemExit(f"{len(NOTES)} notes for {len(targets)} questions")

    rebuilt = []
    for q in targets:
        entry = dict(q)
        entry["explanation"] = NOTES[q["id"]]
        rebuilt.append(entry)

    marker = raw.index(f'"id": "{FIRST}"')
    start = raw.rindex("\n  {\n", 0, marker)
    if not raw.rstrip().endswith("]"):
        raise SystemExit("unexpected shape at the end of pronoun.json")

    updated = (
        raw[:start]
        + "\n"
        + ",\n".join(indent_block(e, 2) for e in rebuilt)
        + "\n]\n"
    )

    check = json.loads(updated)
    if check[:first] != bank[:first]:
        raise SystemExit("questions before the new block changed - aborting")
    if len(check) != len(bank):
        raise SystemExit("question count changed - aborting")
    for before, after in zip(bank[first:], check[first:]):
        strip = lambda q: {k: v for k, v in q.items() if k != "explanation"}
        if strip(after) != strip(before):
            raise SystemExit(f"{before['id']}: changed beyond the explanation")

    BANK.write_text(updated, encoding="utf-8")
    print(f"added explanations to {len(rebuilt)} questions ({FIRST} .. {LAST})")


if __name__ == "__main__":
    main()
