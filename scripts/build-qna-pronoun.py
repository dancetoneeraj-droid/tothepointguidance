"""Build pronoun.json entries from datas/English/qna.pdf (pages 1-10 + answer key 11-12)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "data" / "english" / "pronoun.json"

# fmt: off
QUESTIONS: dict[int, dict] = {
    1: {"q": "If you had seen yesterday's cricket I am sure you would have enjoyed seeing our team bat.", "p": ["If you had seen", "yesterday's cricket", "I am sure you would have enjoyed", "seeing our team bat"]},
    2: {"q": "I enquired of him why he is so negligent in his studies.", "p": ["I enquired of him", "why", "he is so negligent", "in his studies."]},
    3: {"q": "As the meeting was about to end he insisted to ask several questions.", "p": ["As the meeting", "was about to end", "he insisted to ask", "several questions."]},
    4: {"q": "The ship was loaded with cotton.", "p": ["The ship", "was", "loaded", "with cotton."]},
    5: {"q": "When he will come I will make sure I meet him.", "p": ["When he will come", "I will", "make sure", "I meet him."]},
    6: {"q": "Due to inflation the prices of essential items are arising.", "p": ["Due to inflation", "the prices of", "essential items", "are arising."]},
    7: {"q": "I began relating several details connecting with the accident unmindful of boring the audience.", "p": ["I began relating", "several details connecting with", "the accident unmindful of", "boring the audience."]},
    8: {"q": "Weather permitted there will be a garden party at Government House tomorrow.", "p": ["Weather permitted", "there will be a garden", "party at Government House", "tomorrow."]},
    9: {"q": "The traveller being weary he sat by woodside to rest.", "p": ["being weary", "he sat by", "woodside", "to rest."]},
    10: {"q": "It is high time that we leave this place.", "p": ["It is high time", "that", "we leave", "this place."]},
    11: {"q": "He did not and could not have understood the full facts of the case.", "p": ["He did not", "and could not have", "understood", "the full facts of the case."]},
    12: {"q": "Neither Rohit nor Kabir have done his lesson.", "p": ["Neither Rohit", "nor Kabir", "have done", "his lesson."]},
    13: {"q": "I am opposed to the plan of action not because it is ill conceived but that it seems impracticable.", "p": ["I am opposed", "to the plan of action not because", "it is ill conceived but that", "it seems impracticable."]},
    14: {"q": "He as well as you is tired of this long and troublesome affair.", "p": ["He as well as you", "is tired", "of this long", "and troublesome affair."]},
    15: {"q": "There are many important details to attend to before this book gets printed.", "p": ["There are many", "important details", "to attend to", "before this book gets printed."]},
    16: {"q": "Along the northern frontier of India is seen the Himalayas mighty in their splendour.", "p": ["Along the northern frontier", "of India", "is seen the Himalayas", "mighty in their splendour."]},
    17: {"q": "The recommendations of the committee that the age should be lowered down immediately was not accepted.", "p": ["The recommendations of the committee", "that the age should be lowered down", "immediately", "was not accepted."]},
    18: {"q": "He is overworked and that seems to have seriously effected his health.", "p": ["He is overworked", "and that seems", "to have", "seriously effected his health."]},
    19: {"q": "Each of the students whom I have chosen to take part in the discussion have indicated that he will be happy to do so.", "p": ["Each of the students whom", "I have chosen to take part in the discussion", "have indicated", "that he will be happy to do so."]},
    20: {"q": "Honestly speaking I like him not because he is handsome and charming but that he is exceedingly kind.", "p": ["Honestly speaking", "I like him not because", "he is handsome and charming but", "that he is exceedingly kind."]},
    21: {"q": "The father with the son were mysteriously missing from the house.", "p": ["The father with", "the son", "were mysteriously missing", "from the house."]},
    22: {"q": "It is in 1929 when we first flew to the United States.", "p": ["It is", "in 1929", "when we first", "flew to the United States."]},
    23: {"q": "Our country need a number of self sacrificing and devoted political leaders.", "p": ["Our country need", "a number of", "self sacrificing", "and devoted political leaders."]},
    24: {"q": "The constant shouting of slogans do not solve the problems of the country.", "p": ["The constant shouting", "of slogans do not", "solve the problems", "of the country."]},
    25: {"q": "Crossing the road a car knocked him down.", "p": ["Crossing the road", "a car", "knocked", "him down."]},
    26: {"q": "We erect monuments in the memory of the great lest their achievements might be forgotten.", "p": ["We erect monuments", "in the memory", "of the great lest", "their achievements might be forgotten."]},
    27: {"q": "The alarmed report of an earthquake frightened everyone in that disaster prone village.", "p": ["The alarmed report", "of an earthquake", "frightened everyone in that", "disaster prone village."]},
    28: {"q": "He used rather harsh words in denouncing her but he must have had some very strong reasons to do so.", "p": ["He used rather harsh", "words in denouncing her", "but he must have had", "some very strong reasons to do so."]},
    29: {"q": "Instead of his busy and hard life, he still retains freshness and robustness.", "p": ["Instead of", "his busy and hard life,", "he still retains", "freshness and robustness."]},
    30: {"q": "The issues are complex and has been obscured by other factors.", "p": ["The issues are", "complex and", "has been obscured", "by other factors."]},
    31: {"q": "He is working hard with a view to compete with Mohan.", "p": ["He is working hard", "with", "a view to compete", "with Mohan."]},
    32: {"q": "Since he has not yet attained the age of eighteen, he had no right to vote in the present election.", "p": ["Since he has not", "yet attained the age of eighteen,", "he had no right to", "vote in the present election."]},
    33: {"q": "He was so tired that he fell asleep on the bed fully dressed.", "p": ["He was", "so tired", "that he fell asleep", "on the bed fully dressed."]},
    34: {"q": "Is there further reasons you can give me for your failure to do as you promised?", "p": ["Is there", "further", "reasons you can give me", "for your failure to do"]},
    35: {"q": "If anyone of the guests choose to leave before the ceremony is over lead him to exit quickly.", "p": ["If anyone of the guests choose", "to leave before", "the ceremony is over", "lead him to exit quickly."]},
    36: {"q": "While proceeding on leave he had orally committed that he will resume after two days.", "p": ["While proceeding on leave", "he had orally", "committed that", "he will resume"]},
    37: {"q": "I am disappointed in not having saw any place while I was in Delhi on vacation.", "p": ["I am disappointed", "in not having saw", "any place while", "I was in Delhi"]},
    38: {"q": "Now-a-days he along with his friends go for a ride every evening.", "p": ["Now-a-days he", "along with his friends go", "for a ride", "every evening."]},
    39: {"q": "They treated us not even to cocktails but also to dinner.", "p": ["They treated", "us not even", "to cocktails but", "also to dinner."]},
    40: {"q": "What India needs today are more scientists technicians and planners.", "p": ["What India needs today", "are more scientists", "technicians", "and planners."]},
    41: {"q": "Him not agreeing to accept the proposals outlined by the committee is baffling.", "p": ["Him not agreeing", "to accept", "the proposals outlined", "by the committee is baffling."]},
    42: {"q": "If you had work hard you would have certainly got the scholarship.", "p": ["If you had", "work hard", "you would have", "certainly got the scholarship."]},
    43: {"q": "No sooner did the thief saw the policeman than he ran away.", "p": ["No sooner did", "the thief saw the", "policeman than", "he ran away."]},
    44: {"q": "Until I do not inform my teacher I shall not go out of the school.", "p": ["Until I do not", "inform my teacher", "I shall not", "go out of the school."]},
    45: {"q": "Neither the size nor the colour of the gloves were right.", "p": ["Neither the size", "nor the colour", "of the gloves", "were right."]},
    46: {"q": "Bangladesh has come into existence thirty-six years ago.", "p": ["has come", "into", "existence", "thirty-six years ago."]},
    47: {"q": "If it was possible to get near where one of these eruptions took place, we could have a grand sight.", "p": ["If it was possible", "to get near", "where one of these eruptions took place, we", "could have a grand sight."]},
    48: {"q": "By the time the plane had arrived I nearly had despaired of being able to board it.", "p": ["By the time", "the plane had arrived", "I nearly had", "despaired of being able"]},
    49: {"q": "Neither your earnest pleadings nor your profuse tears have made me to change my decision.", "p": ["Neither your earnest pleadings", "nor your", "profuse tears", "have made me to change"]},
    50: {"q": "The gentleman together with his wife and children were drowned.", "p": ["The gentleman", "together with his wife", "and children were", "drowned."]},
    51: {"q": "Sometimes the ministers behave as if they are ministers for all time.", "p": ["Sometimes", "the ministers behave", "as if", "they are ministers"]},
    52: {"q": "Entering the crowded store I saw two vaguely familiar faces.", "p": ["Entering", "the crowded store", "I saw", "two vaguely familiar faces."]},
    53: {"q": "The Director knowing of my interest in linguistics asked me that I would like to attend the national seminar.", "p": ["knowing of my", "interest in", "linguistics asked me that", "I would like to"]},
    54: {"q": "Hardly had I left the house than it began to rain.", "p": ["Hardly had", "I left the house", "than it began", "to rain."]},
    55: {"q": "Turning to the right the town hall at once catches your eye.", "p": ["Turning to the right", "the town hall", "at once", "catches your eye."]},
    56: {"q": "The request of the student union president that fee be lowered were immediately supported by vast majority.", "p": ["of the student union president that fee", "be", "lowered", "were"]},
    57: {"q": "Most of us are not aware that eating some varieties of mushrooms result in death.", "p": ["aware", "that", "eating some varieties", "of mushrooms result"]},
    58: {"q": "After Napoleon had lost the battle of Waterloo in 1815, he had been exiled to the Island of St. Helena.", "p": ["After Napoleon", "had lost the battle of Waterloo in 1815, he", "had been exiled", "to the Island of St. Helena."]},
    59: {"q": "We always complain that prices are too high and that we were not getting our money's worth.", "p": ["We always", "complain that prices are too high and that we", "were not getting", "our money's worth."]},
    60: {"q": "Please rest for a while and when you rest I'll take you round the garden to show you our new roses.", "p": ["Please rest for a while", "and when you rest", "I'll take you round", "the garden to show you our new roses."]},
    61: {"q": "Imagine a town which lacks not only phased growth but is burdened with unauthorised colonies.", "p": ["Imagine a town which", "lacks not only", "phased growth but is burdened", "with unauthorised colonies."]},
    62: {"q": "The manager asked Sunil if he was free to go on tour immediately.", "p": ["The manager asked Sunil", "if he", "was free to go", "on tour immediately."]},
    63: {"q": "Sixty years have passed since India became free.", "p": ["Sixty years", "have passed", "since", "India became free."]},
    64: {"q": "It is easy distinguishing this pen from that.", "p": ["It is easy", "distinguishing", "this pen", "from that."]},
    65: {"q": "When asked a question he rose his hand to catch the teacher's attention.", "p": ["When asked a question", "he rose his hand", "to catch", "the teacher's attention."]},
    66: {"q": "The reason for the train being late was because the train was involved in an accident.", "p": ["The reason", "for the train", "being late", "was because the train was involved in an accident."]},
    67: {"q": "He never has and never will play at cards.", "p": ["He never has", "and never", "will play", "at cards."]},
    68: {"q": "Boys study in order that they could earn their livelihood.", "p": ["Boys study in order", "that they could", "earn their", "livelihood."]},
    69: {"q": "Would you please request him not to tore open the envelope without my consent?", "p": ["Would you please request", "him not to", "tore open the envelope", "without my consent?"]},
    70: {"q": "Consider his young age the achievement of the player is really admirable and appreciable.", "p": ["Consider his young age", "the achievement of the player", "is really admirable", "and appreciable."]},
    71: {"q": "Your statement that you find this bag in the street will not be trusted.", "p": ["Your statement that", "you find this bag", "in the street", "will not be trusted."]},
    72: {"q": "To be elated in the moments of success or to be disconsolate in the moments of failure are a sign of immaturity.", "p": ["To be elated in the", "moments of success or", "to be disconsolate in the moments", "of failure are a sign of immaturity."]},
    73: {"q": "The man who was killed he was my cousin.", "p": ["The man", "who was", "killed he was", "my cousin."]},
    74: {"q": "I think everyone of these men are incompetent.", "p": ["I think", "everyone of", "these men", "are incompetent."]},
    75: {"q": "He was reading very hard for six months still he failed.", "p": ["He was reading", "very hard for", "six months", "still he failed."]},
    76: {"q": "Please believe that money and peace of mind does not go hand in hand.", "p": ["Please believe that", "money and peace of mind", "does not go", "hand in hand."]},
    77: {"q": "He who possess good qualities is bound to impress others.", "p": ["He who possess", "good qualities", "is bound to", "impress others."]},
    78: {"q": "Mother asked me where was I going in such a hurry.", "p": ["Mother asked me", "where was I going", "in such a hurry."]},
    79: {"q": "Despite of his repeated requests the thieves beat him mercilessly.", "p": ["Despite of", "his repeated requests", "the thieves", "beat him mercilessly."]},
    80: {"q": "People like Mahesh looks always cheerful not because of the peace of mind but merely because of successful gestures.", "p": ["People like", "Mahesh looks always", "cheerful not because of the peace of mind", "but merely because of successful gestures."]},
    81: {"q": "She had been a nurse for three years and then she wants to study medicine.", "p": ["She had been", "a nurse for three years", "and then", "she wants to study medicine."]},
    82: {"q": "It is undeniably true that many amongst us felt that the whole building is vibrating.", "p": ["It is undeniably true", "that many amongst us", "felt that", "the whole building is vibrating."]},
    83: {"q": "Everyone of those who came here are foolish and cannot be relied upon.", "p": ["Everyone of those", "who came here", "are foolish and", "cannot be relied upon."]},
    84: {"q": "If I fail in this examination I shall give the next examination.", "p": ["If I fail in", "this examination", "I shall give", "the next examination."]},
    85: {"q": "He hanged his head in shame when he came to know of his son's mischief.", "p": ["He hanged his", "head in shame", "when he came to know of his", "son's mischief."]},
    86: {"q": "The reason why he was late was because he had been caught in rain.", "p": ["The reason why", "he was late was", "because he had been", "caught in rain."]},
    87: {"q": "They are going to start early in order that they will not be late.", "p": ["They are going to", "start early", "in order that", "they will not be late."]},
    88: {"q": "Each of the boys whom I had invited to dinner have indicated that he would be happy to come.", "p": ["Each of the boys", "whom I had invited to dinner", "have indicated that", "he would be happy to come."]},
    89: {"q": "They have been very close friends until they quarrelled.", "p": ["They have been", "very close friends", "until", "they quarrelled."]},
    90: {"q": "The number of students appearing at the written examination increases every year.", "p": ["The number of students", "appearing at", "the written examination", "increases every year."]},
    91: {"q": "When he comes to see us he usually will bring something with him.", "p": ["When he comes", "to see us", "he usually will bring", "something with him."]},
    92: {"q": "I did not want her to have spent all her money at the fair yesterday.", "p": ["I did not", "want her", "to have spent", "all her money at the fair yesterday."]},
    93: {"q": "When at last we got to the theatre the much publicised play was already begun.", "p": ["When at last", "we got to", "the theatre the much publicised play", "was already begun."]},
    94: {"q": "I am sorry I did not know you have left your coat here when you came to see me last Thursday.", "p": ["I am sorry I did not know", "you have left", "your coat here when you came to see", "me last Thursday."]},
    95: {"q": "Had he told me earlier I may have lent him money to save him from disgrace.", "p": ["Had he told me earlier", "I may have lent him money", "to save him", "from disgrace."]},
    96: {"q": "On a rainy day like this I prefer to be at home to going out meeting friends.", "p": ["On a rainy day like this", "I prefer to be at home", "to going out", "meeting friends."]},
    97: {"q": "It is time you decide on your next course of action.", "p": ["It is time", "you decide", "on your next", "course of action."]},
    98: {"q": "I was surprised at not having seen her even though she was standing in front of me.", "p": ["I was surprised at", "not having seen her", "even though", "she was standing in front of me."]},
    99: {"q": "I did not practise music since I was twenty-four.", "p": ["I did not practise", "music", "since", "I was twenty-four."]},
    100: {"q": "The Superintendent of police has announced that those who are found guilty of breach of peace or of taking the law into their hands they will be taken to task.", "p": ["The Superintendent of police has announced that those who are found", "guilty of breach of peace", "or of taking the law into their hands", "they will be taken to task."]},
    101: {"q": "It is not difficult to believe that a man who has lived in this city for a long time he will never feel at home anywhere else in the world.", "p": ["It is not difficult to believe that a man", "who has lived in this city", "for a long time", "he will never feel at home anywhere else in the world."]},
    102: {"q": "Being a destitute I admitted him to an old people's home.", "p": ["Being a destitute", "I admitted him", "to an old", "people's home."]},
    103: {"q": "Due to me being a newcomer I was unable to get a house suitable for my wife and me.", "p": ["Due to me", "being a newcomer", "I was unable to get a house", "suitable for my wife and me."]},
    104: {"q": "Inspite of the doctor's stern warning he continued taking sugar in his tea.", "p": ["Inspite of the doctor's", "stern warning", "he continued taking", "sugar in his tea."]},
    105: {"q": "Never set a bad example; always remember that good and bad behaviour is inculcated by example.", "p": ["Never set a bad", "example; always remember that", "good and bad behaviour", "is inculcated by example."]},
    106: {"q": "Being a very hot day all of us sat at home and watched television and enjoyed ourselves the whole day.", "p": ["Being a very hot day", "all of us sat at home", "and watched", "television and enjoyed ourselves the whole day."]},
    107: {"q": "Had the function not been postponed because of the strike she may have been able to participate.", "p": ["Had the function", "not been postponed", "because of the strike", "she may have been able to participate."]},
    108: {"q": "He ultimately decided to willingly and cheerfully accept the responsibility entrusted to him.", "p": ["He ultimately decided", "to willingly and cheerfully", "accept the responsibility", "entrusted to him."]},
    109: {"q": "Being the only people there their presence was most important.", "p": ["Being the only", "people there", "their presence was", "most important."]},
    110: {"q": "There is no objection to him joining the feast if he is willing to share the expenses.", "p": ["There is", "no objection to him", "joining the feast if he is willing", "to share the expenses."]},
    111: {"q": "She saw that there was nothing else she could do because the room was as clean as it had never been before.", "p": ["She saw that there was nothing else", "she could do", "because the room was as", "clean as it had never been before."]},
    112: {"q": "When the teachers are on strike and a notice to this effect is pasted on the college gate there is no sense to go there.", "p": ["When the teachers are on strike", "and a notice to this effect", "is pasted on the college gate", "there is no sense to go there."]},
    113: {"q": "Not one of the hundreds of striking workers were allowed to go near the factory.", "p": ["Not one of the hundreds", "of striking workers", "were allowed to go", "near the factory."]},
    114: {"q": "More widely popular than the hunting of deer or fox were the pursuit of the hare.", "p": ["More widely popular", "than the hunting of", "deer or fox", "were the pursuit of the hare."]},
}

ANSWERS: dict[int, tuple[str, str]] = {
    1: ("e", "No grammatical error in the sentence."),
    2: ("c", "Use 'was very negligent' instead of 'is so negligent'."),
    3: ("c", "Use 'on being asked' or 'on asking' instead of 'to ask'."),
    4: ("b", "Use 'laden with' instead of 'loaded with'."),
    5: ("a", "Use 'comes' instead of 'will come'."),
    6: ("d", "Use 'rising' instead of 'arising'."),
    7: ("b", "Use 'connected with' instead of 'connecting with'."),
    8: ("a", "Use 'Weather permitting' instead of 'Weather permitted'."),
    9: ("b", "Delete 'he' — 'The traveller being weary, he sat...' is redundant."),
    10: ("c", "Use 'left' instead of 'leave' after 'It is high time that'."),
    11: ("a", "Add 'understand' after 'did not'."),
    12: ("c", "Use 'has' instead of 'have' with 'Neither...nor'."),
    13: ("c", "Use 'but because' instead of 'but that'."),
    14: ("e", "No grammatical error in the sentence."),
    15: ("c", "Use 'to be attended to' instead of 'to attend to'."),
    16: ("c", "Use 'are seen' instead of 'is seen'."),
    17: ("d", "Use 'were not' instead of 'was not'."),
    18: ("d", "Use 'affected' instead of 'effected'."),
    19: ("c", "Use 'has' instead of 'have' with 'Each of'."),
    20: ("c", "Use 'because' instead of 'but that'."),
    21: ("c", "Use 'was' instead of 'were'."),
    22: ("a", "Use 'It was' instead of 'It is'."),
    23: ("a", "Use 'needs' instead of 'need'."),
    24: ("b", "Use 'does not' instead of 'do not'."),
    25: ("a", "Use 'While he was crossing the road' instead of 'Crossing the road'."),
    26: ("d", "Use 'be' instead of 'might be' after 'lest'."),
    27: ("a", "Use 'alarming' instead of 'alarmed'."),
    28: ("d", "Use 'for doing so' correctly — 'some very strong reasons for doing so'."),
    29: ("a", "Use 'In spite of' instead of 'Instead of'."),
    30: ("c", "Use 'have been' instead of 'has been'."),
    31: ("c", "Use 'a view to competing' instead of 'a view to compete'."),
    32: ("c", "Use 'he has' instead of 'he had'."),
    33: ("d", "Place 'fully dressed' after 'asleep'."),
    34: ("a", "Use 'Are' instead of 'Is' with plural 'reasons'."),
    35: ("a", "Use 'chooses' instead of 'choose'."),
    36: ("d", "Use 'would' instead of 'will'."),
    37: ("b", "Use 'in not having seen' instead of 'in not having saw'."),
    38: ("b", "Use 'goes' instead of 'go'."),
    39: ("b", "Use 'not only' instead of 'not even'."),
    40: ("b", "Use 'is' instead of 'are'."),
    41: ("a", "Use 'His not agreeing' instead of 'Him not agreeing'."),
    42: ("b", "Use 'worked hard' instead of 'work hard'."),
    43: ("b", "Use 'see' instead of 'saw' after 'No sooner did'."),
    44: ("a", "Delete 'do not' — use 'Until I inform'."),
    45: ("d", "Use 'was' instead of 'were'."),
    46: ("a", "Use 'came' instead of 'has come'."),
    47: ("a", "Use 'if it were possible' instead of 'if it was possible'."),
    48: ("b", "Use 'arrived' instead of 'had arrived'."),
    49: ("d", "Delete 'to' — 'made me change' not 'made me to change'."),
    50: ("c", "Use 'was' instead of 'were'."),
    51: ("c", "Use 'were' instead of 'are' after 'as if'."),
    52: ("e", "No grammatical error in the sentence."),
    53: ("c", "Use 'if' instead of 'that' after 'asked me'."),
    54: ("c", "Use 'when' instead of 'than' after 'Hardly had'."),
    55: ("a", "Use 'When you turn to the right' instead of 'Turning to the right'."),
    56: ("d", "Use 'was' instead of 'were'."),
    57: ("d", "Use 'results' instead of 'result'."),
    58: ("c", "Use 'was exiled' instead of 'had been exiled'."),
    59: ("c", "Use 'are' instead of 'were'."),
    60: ("b", "Use 'when you have rested' instead of 'when you rest'."),
    61: ("c", "Use 'but also' — 'lacks not only X but also Y'."),
    62: ("e", "No grammatical error in the sentence."),
    63: ("e", "No grammatical error in the sentence."),
    64: ("b", "Use 'to distinguish' instead of 'distinguishing'."),
    65: ("b", "Use 'raised' instead of 'rose'."),
    66: ("d", "Use 'that' instead of 'because' — 'The reason... was that'."),
    67: ("a", "Add 'played' after 'has' — 'He never has played and never will play'."),
    68: ("b", "Use 'can' instead of 'could'."),
    69: ("c", "Use 'tear' instead of 'tore'."),
    70: ("a", "Use 'Considering his' instead of 'Consider his'."),
    71: ("b", "Use 'found' instead of 'find'."),
    72: ("d", "Use 'is a sign of' instead of 'are a sign of'."),
    73: ("c", "Remove 'he' — 'The man who was killed was my cousin'."),
    74: ("c", "Use 'is' instead of 'are'."),
    75: ("a", "Use 'had been reading' instead of 'was reading'."),
    76: ("c", "Use 'do not' instead of 'does not'."),
    77: ("a", "Use 'possesses' instead of 'possess'."),
    78: ("b", "Use 'where I was going' instead of 'where was I going' in indirect speech."),
    79: ("a", "Use 'Despite' and remove 'of'."),
    80: ("b", "Use 'look' instead of 'looks'."),
    81: ("d", "Use 'wanted' instead of 'wants'."),
    82: ("d", "Use 'was vibrating' instead of 'is vibrating'."),
    83: ("b", "Use 'is' instead of 'are'."),
    84: ("c", "Use 'take' instead of 'give'."),
    85: ("a", "Use 'hung' instead of 'hanged'."),
    86: ("c", "Use 'that' instead of 'because'."),
    87: ("d", "Use 'may' instead of 'will'."),
    88: ("c", "Delete 'have' — 'Each of the boys... has indicated'."),
    89: ("a", "Use 'had been' instead of 'have been'."),
    90: ("e", "No grammatical error in the sentence."),
    91: ("c", "Use 'brings' instead of 'will bring'."),
    92: ("c", "Use 'to spend' instead of 'to have spent'."),
    93: ("d", "Use 'had already begun' instead of 'was already begun'."),
    94: ("b", "Use 'had left' instead of 'have left'."),
    95: ("b", "Use 'might have' instead of 'may have'."),
    96: ("b", "Use 'being' instead of 'to be'."),
    97: ("b", "Use 'you decided' instead of 'you decide'."),
    98: ("e", "No grammatical error in the sentence."),
    99: ("a", "Use 'have not practised' instead of 'did not practise'."),
    100: ("d", "Delete 'they'."),
    101: ("d", "Omit 'he'."),
    102: ("a", "Add 'he' before 'being destitute'."),
    103: ("a", "Use 'my being' instead of 'me being'."),
    104: ("c", "Use 'to take' instead of 'taking'."),
    105: ("c", "Use 'good or bad' instead of 'good and bad'."),
    106: ("a", "Use 'It being' instead of 'Being'."),
    107: ("d", "Use 'might have' instead of 'may have'."),
    108: ("b", "Use 'to accept willingly and cheerfully' instead of 'to willingly and cheerfully accept'."),
    109: ("a", "Add 'They' before 'being'."),
    110: ("b", "Use 'his joining' instead of 'him joining'."),
    111: ("e", "No grammatical error in the sentence."),
    112: ("d", "Use 'no sense in going' instead of 'no sense to go'."),
    113: ("c", "Use 'was' instead of 'were'."),
    114: ("d", "Use 'was' instead of 'were'."),
}
# fmt: on


def letter_to_index(letter: str, num_parts: int) -> int:
    letter = letter.lower()
    if letter == "e" or (letter == "d" and num_parts == 3):
        return num_parts  # No error slot
    return {"a": 0, "b": 1, "c": 2, "d": 3}[letter]


def build_entry(num: int, next_id: int) -> dict:
    qdata = QUESTIONS[num]
    parts = qdata["p"]
    letter, explanation = ANSWERS[num]

    options = parts + ["No error"]
    idx = letter_to_index(letter, len(parts))
    correct = options[idx]

    if letter.lower() in ("e",) or (letter.lower() == "d" and len(parts) == 3 and correct == "No error"):
        pass  # already correct
    elif correct == "No error":
        explanation = "No grammatical error in the sentence."

    return {
        "id": f"pronoun_{next_id:03d}",
        "question": re.sub(r"\s+", " ", qdata["q"]).strip(),
        "options": [re.sub(r"\s+", " ", o).strip() for o in options],
        "correctAnswer": re.sub(r"\s+", " ", correct).strip(),
        "explanation": explanation.strip(),
    }


def main() -> None:
    assert len(QUESTIONS) == 114, f"Expected 114 questions, got {len(QUESTIONS)}"
    assert len(ANSWERS) == 114, f"Expected 114 answers, got {len(ANSWERS)}"
    assert set(QUESTIONS) == set(ANSWERS), "Question/answer number mismatch"

    existing = json.loads(TARGET.read_text(encoding="utf-8"))
    start_id = len(existing) + 1

    added = [build_entry(n, start_id + i) for i, n in enumerate(sorted(QUESTIONS))]

    # Validate every correctAnswer is in options
    errors: list[str] = []
    for e in added:
        if e["correctAnswer"] not in e["options"]:
            errors.append(f"{e['id']}: correctAnswer not in options")

    if errors:
        raise SystemExit("Validation failed:\n" + "\n".join(errors))

    merged = existing + added
    TARGET.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")

    print(f"Added {len(added)} questions -> {TARGET}")
    print(f"IDs: pronoun_{start_id:03d} .. pronoun_{start_id + len(added) - 1:03d}")
    no_err = sum(1 for e in added if e["correctAnswer"] == "No error")
    print(f"No-error answers: {no_err}")


if __name__ == "__main__":
    main()
