import requests
import tqdm

# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'AIzaSyAxAP3RT00cK0Y5RSDtE2Mma36IoFabY3c'


def translate_text(text, source_language='en', target_language='ka'):
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        'q': text,
        'source': source_language,
        'target': target_language,
        'key': api_key,
    }

    response = requests.post(url, params=params)
    result = response.json()

    translated_text = result['data']['translations'][0]['translatedText']

    return translated_text


def parse_samples_from_text_data(fp):
    file_data = open(fp).read()

    sample_pattern = re.compile(r"Sample (\d+):\nGender: (\w+)\nText: \"(.+)\"\nIs_Hate_Speech: (\w+)")
    matches = re.findall(sample_pattern, file_data)

    # Convert matches to JSON format
    samples = [
        {"sample": int(match[0]), "gender": match[1], "text": match[2], "hate_speech": match[3].lower() == 'true'}
        for match in matches
    ]

    return samples


def translate_json_data(json_data):
    for item in tqdm.tqdm(json_data, desc="Translating Texts..."):
        item['translated_text'] = translate_text(text=item['text'])
    return json_data


if __name__ == '__main__':
    import re
    import json

    # Translate GPT Generated Datasets Into Georgian

    #
    # in_fps = [
    #     "gpt_generated_hate_speech_dataset/gpt_3_english_general_hate_speech.txt",
    #     "gpt_generated_hate_speech_dataset/gpt_3_english_political_hate_speech.txt"
    # ]
    # out_fps = [item.replace('.txt', '.json') for item in in_fps]

    # for in_fp, out_fp in zip(in_fps, out_fps):
    #     json_data = parse_samples_from_text_data(in_fp)
    #     translated_json_data = translate_json_data(json_data)
    #
    #     with open(out_fp, "w") as file:
    #         json.dump(translated_json_data, file)
