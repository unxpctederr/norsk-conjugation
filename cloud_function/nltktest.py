from nltk import word_tokenize, pos_tag, sent_tokenize, data as nltk_data
import re
import uuid
import requests
import json
import os

# Load NLTK data manually
root = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(root, 'nltk_data')
os.chdir(download_dir)
nltk_data.path.append(download_dir)

tag_dict = {
    'VB': 'Verb Base',
    'VBD': 'Past Tense',
    'VBG': 'Gerund/Present Participle',
    'VBN': 'Past Participle',
    'VBP': 'Singular Present',
    'VBZ': '3rd Person Singular Present'
}

def translate(sentence: str, to_language: str):
    base_url = 'https://api.cognitive.microsofttranslator.com'
    endpoint = '/translate?api-version=3.0'
    params = '&to=' + to_language
    constructed_url = base_url + endpoint + params

    subscription_key = "7bfbbcdab65841f3a97a5a7786181a34"
    location = "southeastasia"

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text' : sentence
    }]
    response = requests.post(constructed_url, headers=headers, json=body)
    return response.json()[0]['translations'][0]['text']


def get_sentence_verbs(sentence: str):
    word_tokens = word_tokenize(sentence)
    sentence_parts = pos_tag(word_tokens)
    # Filter out only verbs
    verbs = []
    for part in sentence_parts:
        if part[1] in tag_dict.keys():
            verbs.append(part)
    return verbs

def get_data(textToExamine: str):
    # Preprocess the text
    combine_whitespace = re.compile(r"\s+")
    sample_formatted = textToExamine.replace('[Illustration]', '').replace('\n', ' ').replace('Mr.', 'Mr ').replace('Mrs. ', 'Mrs ')
    sample_formatted = combine_whitespace.sub(" ", sample_formatted).strip()

    sentences = sent_tokenize(sample_formatted)

    sentences_data = []

    for sentence in sentences:
        sentence_translated = translate(sentence, "nb")
        sentence_verbs_pos = get_sentence_verbs(sentence)

        verb_translations = {}
        for verb in sentence_verbs_pos:
            verb_translated = translate(verb[0], "nb")
            verb_translations[verb[0]] = verb_translated
        
        sentences_data.append({
            'sentence_eng': sentence,
            'sentence_no': sentence_translated,
            'verbs_eng_pos': sentence_verbs_pos,
            'verb_trans_no': verb_translations
        })
    return sentences_data
