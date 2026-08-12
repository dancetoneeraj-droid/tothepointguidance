"""Build pronoun.json entries from Spotting Errors (Miscellaneous) Exercises A-E.
Chapter 16, Objective General English — 125 questions appended as pronoun_763..887.

Run: python scripts/build-spotting-error-pronoun.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "data" / "english" / "pronoun.json"
START_ID = 763

QUESTIONS: list[dict] = [{'parts': ['Another baffling change', 'that I notice in him now-a-days', 'is that he avoids to speak to me.']},
 {'parts': ['I asked him', 'how could he go out', 'if it started raining.']},
 {'parts': ['One of the state in which', 'Satyagraha was offered was Rajkot,', 'where he had spent his youth.']},
 {'parts': ['Hardly the inspector had arrived there', 'to investigate the crime', 'when the house was set ablaze.']},
 {'parts': ['Since his arrival at his native town',
            'he is trying to the best of his power',
            'to spread education among the poor masses.']},
 {'parts': ['In various parts of the country', 'ponds just dry down', 'in the scorching heat of summer.']},
 {'parts': ['He lay the watch on the table', 'and then forgot all about it', 'when he went out.']},
 {'parts': ['Although he draws a reasonably good salary,',
            'he has a large family to support,',
            'and he finds it difficult to make both ends meet.']},
 {'parts': ['While it is apparent',
            'that biotechnology offers significant benefits',
            'adequate attention has not been focussed to this vital area.']},
 {'parts': ['Being a sunny day', 'I decided to skip', 'work and stay at home.']},
 {'parts': ['We had to cancel our trip to Delhi', 'because when we reached the railway', 'station, the train left.']},
 {'parts': ['Many a student', 'has failed in the Mathematics test', 'but Dilip has scored 100 per cent.']},
 {'parts': ['The General with over 1000 officers and soldiers',
            'have surrendered to the',
            'Indian troops who are patrolling the valley.']},
 {'parts': ['If he wrote the examination faster',
            'and had answered one more question',
            'he would have scored better.']},
 {'parts': ['For decades', 'there have been', 'a debate on whether schizophrenia is a psychological condition.']},
 {'parts': ['Mohan is the one', 'who always finds', 'fault with whatever Ram does.']},
 {'parts': ['There is a need', 'to revising Government policies', 'on controlling unauthorized constructions.']},
 {'parts': ['We know where it begins', "but we don't know", 'that where it ends.']},
 {'parts': ['The simplest method', 'of welding two pieces of metal together', 'in known as pressure welding.']},
 {'parts': ['One of the important benefits', 'of machine age', 'is that our standard of life has improved.']},
 {'parts': ['There is sense of urgency',
            'in locating alternative sources of water',
            'to augment the dwindling supply.']},
 {'parts': ['Although there is virtually no production in India',
            "the 'Encyclopaedia Britannica'",
            'estimate that India has perhaps the largest accumulated stocks of silver in the world.']},
 {'parts': ['Neither the severe earthquake',
            'or the subsequent famine',
            'could demoralize the people of the country.']},
 {'parts': ['As soon as I shall reach New Delhi', 'I shall send you the file', 'you have asked for.']},
 {'parts': ['All the furnitures have been', 'replaced by the owner of the house', 'before shifting.']},
 {'parts': ['Beware of', 'a fair weather friend', 'who is neither a friend in need nor a friend indeed.']},
 {'parts': ['Copernicus proved', 'that Earth', 'moves round the Sun.']},
 {'parts': ['Seldom we have been treated', 'in such a rude manner', 'by the police personnel.']},
 {'parts': ['Some men are born great', 'some achieve greatness', 'and some had greatness thrust on them.']},
 {'parts': ['The property', 'was divided', 'among the two brothers.']},
 {'parts': ['I am quite certain', 'that the lady is not only greedy', 'but miserly.']},
 {'parts': ['There are a number of reasons', 'I do not like him,', 'but his selfishness is intolerable.']},
 {'parts': ['I have read an interesting book yesterday',
            'and underlined the new words',
            'which are simple but effective.']},
 {'parts': ['He cannot be trusted',
            'with important secret informations;',
            'otherwise I would have made him my assistant.']},
 {'parts': ['Is there further reasons', 'you can give me for your failure', 'to do as you promised?']},
 {'parts': ['During the final minutes of the speech', 'the speaker requested to', 'the audience to have patience.']},
 {'parts': ['He is running temperature since last Friday', 'and doctors suspect', 'that he is down with typhoid.']},
 {'parts': ['Travel agents around the world have come to rely on computers',
            'to book seats',
            'in air flights or rooms in hotels, either today or a year from now.']},
 {'parts': ['She expressed her gratitudes', 'to all those', 'who had supported her.']},
 {'parts': ['When the meeting was over,', 'he was very tired', 'so that he went home immediately.']},
 {'parts': ['Modern man must pull himself off together',
            'and act his part in life',
            "as God's own most favourite creature."]},
 {'parts': ['There would be fewer follies,',
            'and happiness and good feeling all round',
            'if we applied the scientific attitude for all our affairs.']},
 {'parts': ['Heera told to the teacher', "that she couldn't come for the rehearsals", 'the next day.']},
 {'parts': ['I am told that Anjali has been', 'suffering from fever', 'since ten days.']},
 {'parts': ['The armed forces have been working around the clock',
            'to bring a semblance of',
            'normality',
            'in the flood affected areas.']},
 {'parts': ["Just when Alfred Nobel's discoveries were beginning to bring him rewards,",
            'which were to make him one of the richest man of his day,',
            'an anti-Nobel campaign was started in France.']},
 {'parts': ['This is the second communication we have sent', 'and we are much surprised', 'at receiving no answer.']},
 {'parts': ['Several guests noticed Mr. Sharma', 'falling back in his chair', 'and gasping for breath.']},
 {'parts': ['Long life is good', 'if one be happy', 'and has friends.']},
 {'parts': ['His assistants have', 'and are still doing', 'excellent work for the organization.']},
 {'parts': ['None of the diplomats at the conference', 'was able either', 'to comprehend or solve the problem.']},
 {'parts': ['Rather than go', 'with Amit, he decided', 'to stay at home.']},
 {'parts': ['He always practices', 'justice and', 'cares for moral principles.']},
 {'parts': ['The whole block of flats', 'including two shops were', 'destroyed in fire.']},
 {'parts': ['He feels his troubles', 'as much or', 'even more than they.']},
 {'parts': ['Such rules', 'do not apply to', 'you and I.']},
 {'parts': ['It is a', 'quarter to ten', 'by my watch.']},
 {'parts': ['I like reading', 'more than', 'to play games.']},
 {'parts': ['The sum and substance', 'of this poem', 'is as follows.']},
 {'parts': ['The team was', 'now in the field and', 'about to take their place.']},
 {'parts': ['Perhaps you know', 'that I have passed', 'the examination in 1990.']},
 {'parts': ['The teacher', 'kept advising us', 'to work hard.']},
 {'parts': ['At a very young age', 'he died with', 'heart disease.']},
 {'parts': ['The average age', 'at which people', 'begin to need', 'eye-glasses are increasing.']},
 {'parts': ['He is trying', 'to earn money', 'for myself', 'and him.']},
 {'parts': ['We Indians', "don't understand that", 'driving vehicles', 'require care and skill.']},
 {'parts': ['Indians are', 'wedded in the', 'democratic way', 'of life in a peaceful manner.']},
 {'parts': ['The present president of',
            'the United States',
            'is thinking of',
            'becoming the most supreme leader of the world.']},
 {'parts': ['Although the truck was', 'moving very fast', 'the driver stopped it', 'in a skilfully manner.']},
 {'parts': ['Although', 'he achieved great success', 'but he', 'could not win fame.']},
 {'parts': ['I pretended as if', 'interested in the conversation', 'but really it was very boring.']},
 {'parts': ["I don't usually like staying at hotels,",
            'but last summer we spent a few days',
            'at a very nice hotel by sea.']},
 {'parts': ['I will try to be on time', 'but do not worry', 'when I am late.']},
 {'parts': ['The teacher remarked that', 'they all had', 'done it very badly.']},
 {'parts': ['The train is supposed', 'to arrive at 10 a.m. yesterday', 'but it was an hour late.']},
 {'parts': ['Ritu will be surprised', 'as she hears', 'the news.']},
 {'parts': ['I asked two persons', 'the way to the station', 'but none of them knew it.']},
 {'parts': ['Despite of a good monsoon this year,', 'the production of food grains in the', 'country did not go up.']},
 {'parts': ['The last of the Mughal emperors of India',
            'was first imprisoned and',
            'was later sent into exile by the British.']},
 {'parts': ['Hardly as I stepped out of my house', 'when I saw some policemen', 'coming towards my house.']},
 {'parts': ['Today, the cost of living',
            'is such higher that many people',
            'find it difficult to keep their hearth burning.']},
 {'parts': ['Rina was trying for admission in the engineering college',
            'even though her parents',
            'wanted her to take up medicine.']},
 {'parts': ['Yavanika is one of the latest', 'additions to good drama', 'which appeared in recent times.']},
 {'parts': ['Children visiting the park', 'are amused by the monkeys', 'play in the cages.']},
 {'parts': ['I am better acquainted', 'with the country', 'than you.']},
 {'parts': ['Being occupied with important matters', 'he had no leisure', 'to see us.']},
 {'parts': ['He was not promoted to the', 'rank of a Colonel', 'till for a few months of his resignation.']},
 {'parts': ['The man who is perpetually',
            'hesitating which of the two things he will do first',
            'will ultimately do either.']},
 {'parts': ['No other hill station is as', 'beautiful as Darjeeling', 'with its scenic beauties.']},
 {'parts': ['Being a well-known physicist, he', 'was invited to deliver', 'a lecture on laser technology.']},
 {'parts': ['The chief idea of every common type',
            'of traveller is to see as',
            'many objects of interest as he possibly could.']},
 {'parts': ['He was hard down', 'for money and was', 'being harassed by his creditor.']},
 {'parts': ['If we really set to', 'we can get the whole house', 'cleaned in an afternoon.']},
 {'parts': ['The main reason', 'for his fiscal success', 'is that', 'he is hardworking.']},
 {'parts': ['Since the two parties each won',
            'the same number of seats,',
            'the minority party holds the balance of power.']},
 {'parts': ["It's arrogant for you", "to assume you'll", 'win every time.']},
 {'parts': ["We've paid for our travel and accommodation,", 'so we need only to take', 'some pocket-money with us.']},
 {'parts': ["There's no evidence to show",
            'that information technology secrets are more',
            'vulnerable in India than Britain or the U.S.']},
 {'parts': ['It is shameful that hunting',
            'is still considered sport',
            'by some unscrupulous people in the civilized world.']},
 {'parts': ['The vacancy was filled by Mr. Rao', 'who the manager', 'thought worthy of promotion.']},
 {'parts': ['She was taller', 'than either of', 'her five sisters.']},
 {'parts': ["'Treasure Island' is one", 'of the best pirate stories', 'that was ever written.']},
 {'parts': ['The population of Kolkata', 'is greater than', 'in any town in England.']},
 {'parts': ['He has a scheme of his own', 'which he thinks more preferable', 'to that of any other person.']},
 {'parts': ['Some people complain when they',
            'encounter a small misfortune in the',
            'course of their thorough happy life.']},
 {'parts': ['I am sorry worrying you with my troubles,',
            'but when I have explained',
            'I am sure you will understand.']},
 {'parts': ['I am very sorry that', 'a previous engagement will prevent me', 'from calling on you tonight.']},
 {'parts': ['No student is', 'as intelligent', 'as my son.']},
 {'parts': ['The most important feature', 'of our products are that', 'they are developed in house.']},
 {'parts': ['When he was tired', 'he took rest under', 'the shade of a tree.']},
 {'parts': ['The principal along', 'with the students', 'have gone to Simla.']},
 {'parts': ['When you have gone', 'through my book', 'give the same to me.']},
 {'parts': ['He said a number of lies', 'and then went without', 'saying me good bye.']},
 {'parts': ['Not only we saw', 'the Education Minister but', 'also the Chief Minister.']},
 {'parts': ['I came directly', 'to my residence', 'from the airport.']},
 {'parts': ['I signed on the receipt', 'in the morning but the pay', 'has not been disbursed to me.']},
 {'parts': ['This is the same story', 'which I heard', 'from him yesterday.']},
 {'parts': ['What to speak of', 'food even water', 'was not available.']},
 {'parts': ['It was difficult to get out', 'because the street was full of people', 'from one end to another.']},
 {'parts': ['It has been our custom', 'from time immemorial to be', 'hospitable to those who come to our doors.']},
 {'parts': ['She does not hardly', 'know what', 'happened yesterday.']},
 {'parts': ['In my opinion', 'a pencil is always', 'more preferable to a pen.']},
 {'parts': ['The salesman tried', 'to mislead me', 'with a talk of amazing savings on heating bills.']},
 {'parts': ['He is well up', 'these days despite', 'having ill health']},
 {'parts': ['He regarded his marriage', 'as a mean to an end;', "he just wanted his wife's wealth."]}]

ANSWERS: list[dict] = [{'letter': 'c', 'explanation': "Say 'speaking to' for 'to speak'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'how he could go out'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'states'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'Hardly had the inspector'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'trying his best'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'dry up'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'laid'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'c', 'explanation': "Say 'been focused on'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'It being'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'had left'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'but Dilip has'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'has surrendered'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'If he had written'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'has been a debate'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'b', 'explanation': "Say 'to revise'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'where it ends'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'is known'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'living standard'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'b', 'explanation': "Say 'estimates'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'nor'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'As soon as I reach'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'furniture has been'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'b', 'explanation': "Say 'the Earth'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'Seldom have we'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'have' for 'had'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'between' for 'among'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'a miser' for 'miserly'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'why I do not like him'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'read' for 'have read'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'information' for 'informations'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'a further reason' for 'further reasons'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'requested the audience'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'has been running'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'a', 'explanation': "Say 'gratitude' for 'gratitudes'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'so' for 'so that'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'pull himself together'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'to' for 'for'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'told the teacher'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'for ten days'.", 'noError': False},
 {'letter': 'd', 'explanation': "Say 'into the flood affected areas'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'which was' for 'which were'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'very surprised' for 'much surprised'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'b', 'explanation': "Say 'is happy' for 'be happy'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'is still doing' for 'are still doing'.", 'noError': False},
 {'letter': 'b', 'explanation': "Delete 'either'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'c', 'explanation': "Say 'about' for 'for'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'was' for 'were'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'them' for 'they'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'me' for 'I'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'c', 'explanation': "Say 'playing' for 'to play'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'a', 'explanation': "Say 'The team were'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'passed' for 'have passed'.", 'noError': False},
 {'letter': 'b', 'explanation': "Add 'on' after 'kept'.", 'noError': False},
 {'letter': 'b', 'explanation': "Use 'of' in place of 'with'.", 'noError': False},
 {'letter': 'd', 'explanation': "Use 'is' in place of 'are'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'for me'.", 'noError': False},
 {'letter': 'd', 'explanation': "Say 'requires'.", 'noError': False},
 {'letter': 'b', 'explanation': "Use 'to' in place of 'in'.", 'noError': False},
 {'letter': 'd', 'explanation': "Delete 'most'.", 'noError': False},
 {'letter': 'd', 'explanation': "Say 'in a skilful manner'.", 'noError': False},
 {'letter': 'c', 'explanation': "Remove 'but'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'I were interested'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'by the sea'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'if' for 'when'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'a', 'explanation': "Say 'was supposed'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'when' for 'as'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'neither of them' in place of 'none'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'despite' for 'Despite of'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'sent to exile'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'hardly had I'.", 'noError': False},
 {'letter': 'b', 'explanation': "Say 'so high'.", 'noError': False},
 {'letter': 'a', 'explanation': "Use 'to' in place of 'in'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'which have appeared'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'playing' for 'play'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'c', 'explanation': "Use 'Until' in place of 'till for'.", 'noError': False},
 {'letter': 'c', 'explanation': "Use 'neither' in place of 'either'.", 'noError': False},
 {'letter': 'c', 'explanation': "Use 'Beauty' in place of 'Beauties'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'c', 'explanation': "Use 'can' in place of 'could'.", 'noError': False},
 {'letter': 'a', 'explanation': "Use 'hard up' in place of 'hard down'.", 'noError': False},
 {'letter': 'c', 'explanation': 'In the afternoon.', 'noError': False},
 {'letter': 'b', 'explanation': "Say 'financial' for 'fiscal'.", 'noError': False},
 {'letter': 'a', 'explanation': "Use 'have won' in place of 'won'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'arrogant of' for 'arrogant for'.", 'noError': False},
 {'letter': 'b', 'explanation': "Use 'to take only' in place of 'need only'.", 'noError': False},
 {'letter': 'c', 'explanation': "Use 'than those of Britain' in place of 'than Britain'.", 'noError': False},
 {'letter': 'b', 'explanation': "Use 'a sport' for 'sport'.", 'noError': False},
 {'letter': 'b', 'explanation': "Use 'whom' in place of 'who'.", 'noError': False},
 {'letter': 'b', 'explanation': "Use 'any one' in place of 'either'.", 'noError': False},
 {'letter': 'c', 'explanation': "Use 'were' in place of 'was'.", 'noError': False},
 {'letter': 'c', 'explanation': "Use 'that of any' in place of 'in any'.", 'noError': False},
 {'letter': 'b', 'explanation': "Remove 'more'.", 'noError': False},
 {'letter': 'c', 'explanation': "Use 'thoroughly' for 'thorough'.", 'noError': False},
 {'letter': 'a', 'explanation': "Use 'to worry' in place of 'worrying'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'a', 'explanation': "Use 'No other students' in place of 'No students'.", 'noError': False},
 {'letter': 'b', 'explanation': "Use 'is' in place of 'are'.", 'noError': False},
 {'letter': 'b', 'explanation': "Use 'in the shade'.", 'noError': False},
 {'letter': 'c', 'explanation': "Use 'has gone to Simla'.", 'noError': False},
 {'letter': 'c', 'explanation': "Use 'it' in place of 'the same'.", 'noError': False},
 {'letter': 'a', 'explanation': "Use 'told' in place of 'said'.", 'noError': False},
 {'letter': 'a', 'explanation': "Place 'not only' after 'saw'.", 'noError': False},
 {'letter': 'a', 'explanation': "Say 'direct'.", 'noError': False},
 {'letter': 'a', 'explanation': "Drop 'on' after 'signed'.", 'noError': False},
 {'letter': 'b', 'explanation': "Use 'that' in place of 'which'.", 'noError': False},
 {'letter': 'a', 'explanation': "Use 'Not to speak of' in place of 'What to speak of'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'one end to other'.", 'noError': False},
 {'letter': 'c', 'explanation': "Say 'door'.", 'noError': False},
 {'letter': 'a', 'explanation': "Drop 'hardly'.", 'noError': False},
 {'letter': 'c', 'explanation': "Drop 'more'.", 'noError': False},
 {'letter': 'd', 'explanation': 'No grammatical error in the sentence.', 'noError': True},
 {'letter': 'a', 'explanation': "Use 'off' for 'up'.", 'noError': False},
 {'letter': 'b', 'explanation': "Use 'means' for 'mean'.", 'noError': False}]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def build_options(parts: list[str]) -> list[str]:
    if len(parts) == 4 and all(normalize(p).lower() != "no error" for p in parts):
        return [normalize(p) for p in parts]
    return [normalize(p) for p in parts] + ["No error"]


def letter_to_index(letter: str, parts: list[str], options: list[str]) -> int:
    letter = letter.lower()
    if letter == "d" and len(parts) == 3:
        return 3
    idx = {"a": 0, "b": 1, "c": 2, "d": 3}[letter]
    if idx >= len(options):
        raise ValueError(f"Letter {letter} out of range for {len(options)} options")
    return idx


def build_entry(num: int) -> dict:
    q = QUESTIONS[num - 1]
    ans = ANSWERS[num - 1]
    parts = q["parts"]
    options = build_options(parts)
    idx = letter_to_index(ans["letter"], parts, options)
    correct = options[idx]
    explanation = ans["explanation"].strip()
    if ans.get("noError") or correct == "No error":
        explanation = "No grammatical error in the sentence."

    question = q.get("question") or normalize(" ".join(parts))

    return {
        "id": f"pronoun_{START_ID + num - 1:03d}",
        "question": question,
        "options": options,
        "correctAnswer": correct,
        "explanation": explanation,
    }


def main() -> None:
    assert len(QUESTIONS) == 125, f"Expected 125 questions, got {len(QUESTIONS)}"
    assert len(ANSWERS) == 125, f"Expected 125 answers, got {len(ANSWERS)}"

    existing = json.loads(TARGET.read_text(encoding="utf-8"))
    assert len(existing) == START_ID - 1, (
        f"Expected {START_ID - 1} existing entries, got {len(existing)}"
    )

    added = [build_entry(n) for n in range(1, 126)]

    errors: list[str] = []
    for e in added:
        if e["correctAnswer"] not in e["options"]:
            errors.append(
                f"{e['id']}: correctAnswer {e['correctAnswer']!r} not in options"
            )

    if errors:
        raise SystemExit("Validation failed:\n" + "\n".join(errors))

    merged = existing + added
    TARGET.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")

    print(f"Added {len(added)} questions -> {TARGET}")
    print(f"IDs: pronoun_{START_ID:03d} .. pronoun_{START_ID + len(added) - 1:03d}")
    no_err = sum(1 for e in added if e["correctAnswer"] == "No error")
    print(f"No-error answers: {no_err}")


if __name__ == "__main__":
    main()
