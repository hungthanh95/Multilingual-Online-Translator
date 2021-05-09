import requests
from bs4 import BeautifulSoup
import sys

languages_support = [
    'Arabic',
    'German',
    'English',
    'Spanish',
    'French',
    'Hebrew',
    'Japanese',
    'Dutch',
    'Polish',
    'Portuguese',
    'Romanian',
    'Russian',
    'Turkish'
]

# speed up requests
m_requests = requests.Session()


def check_language_support(src_lang):
    if src_lang in languages_support:
        pass
    else:
        print("Sorry, the program doesn't support {}".format(src_lang))
        exit(0)


# Select data from BeautifulSoup
def crawl_data(soup, pattern, max_data):
    list_data = []
    wrap_result = soup.select(pattern)
    for index, data in enumerate(wrap_result):
        # Just get enough data
        if index == max_data:
            break
        list_data.append(data.text.strip())
    return list_data


def translation(ori_lang, list_trans_lang, message, max_example):
    for trans_lang in list_trans_lang:
        list_words_trans = []
        list_sen_ori = []
        list_sen_trans = []
        word_trans_pattern = '.translation.ltr.dict'
        sen_ori_pattern = 'div.src.ltr > span.text'
        sen_trans_pattern = 'div.trg.ltr > span.text'

        # Arabic and Hebrew using another pattern
        if trans_lang in ['Arabic', 'Hebrew']:
            word_trans_pattern = '.translation.rtl.dict'
            sen_trans_pattern = 'div.trg.rtl > span.text'

        url = 'https://context.reverso.net/translation/{}-{}/{}'.format(ori_lang.lower(),
                                                                        trans_lang.lower(),
                                                                        message.lower())

        headers = {'User-Agent': 'Chrome',
                   'Content-type': 'text/plain; charset=utf-8'
                   }
        r = m_requests.get(url,  headers=headers)

        if r:
            soup = BeautifulSoup(r.content, 'html.parser')

            # find all translation word
            list_words_trans = crawl_data(soup, word_trans_pattern, max_example)
            # find all original sentences
            list_sen_ori = crawl_data(soup, sen_ori_pattern, max_example)
            # find all translate sentences
            list_sen_trans = crawl_data(soup, sen_trans_pattern, max_example)

            # Print translated word and sentences to the terminal
            print('{} Translations:'.format(trans_lang))
            for word in list_words_trans:
                print(word)
            print('\n{} Examples:'.format(trans_lang))
            for ori_sen, trans_sen in zip(list_sen_ori, list_sen_trans):
                print(ori_sen)
                print(trans_sen)
                print('\n')

            # Save word translated to file
            with open('{}.txt'.format(message), 'a', encoding='utf-8') as file:
                file.write('{} Translations:\n'.format(trans_lang))
                for word in list_words_trans:
                    file.write(word + '\n')
                file.write('\n{} Examples:\n'.format(trans_lang))
                for ori_sen, trans_sen in zip(list_sen_ori, list_sen_trans):
                    file.write(ori_sen + '\n')
                    file.write(trans_sen + '\n')
                    file.write('\n\n')
        elif r.status_code == 404:
            print("Sorry, unable to find {}".format(message))
            exit(0)
        else:
            print('Something wrong with your internet connection')
            exit(0)


def main():
    # Number of example need to display
    max_example = 1

    # handler arguments
    args = sys.argv
    ori_lang = str(args[1]).lower().capitalize()
    trans_lang = str(args[2]).lower().capitalize()
    word_need_trans = str(args[3]).lower()

    # Valid argv
    check_language_support(ori_lang)

    if trans_lang.lower() == 'all':
        languages_support.remove(ori_lang)
        list_trans_lang = languages_support
    else:
        check_language_support(trans_lang)
        list_trans_lang = [trans_lang]
        # With translated only a language, display multiple example
        max_example = 5

    # Start translate
    translation(ori_lang, list_trans_lang, word_need_trans, max_example)


if __name__ == "__main__":
    main()
