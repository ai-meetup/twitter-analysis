from __future__ import print_function, division, unicode_literals

import json
import codecs

from torchmoji.create_vocab import VocabBuilder
from torchmoji.word_generator import TweetWordGenerator

from torchmoji.sentence_tokenizer import SentenceTokenizer
from torchmoji.model_def import torchmoji_feature_encoding
from torchmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH

import json
import csv
import numpy as np

from torchmoji.sentence_tokenizer import SentenceTokenizer
from torchmoji.model_def import torchmoji_emojis
from torchmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH

OUTPUT_PATH = 'test_sentences.csv'

def parse_line_maybe(x):
    try:
        return [json.loads(x)['text']]
    except:
        return []

TEST_SENTENCES = [
    r
    for x in codecs.open('tweets.txt', 'rU', 'utf-8')
    for r in parse_line_maybe(x)
]

# codecs.open('tweets.txt', 'rU', 'utf-8').read().split('\n')

def top_elements(array, k):
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]

maxlen = 30

print('Tokenizing using dictionary from {}'.format(VOCAB_PATH))
with open(VOCAB_PATH, 'r') as f:
    vocabulary = json.load(f)
    # print(vocabulary)

st = SentenceTokenizer(vocabulary, maxlen)

print('Loading model from {}.'.format(PRETRAINED_PATH))
model = torchmoji_emojis(PRETRAINED_PATH)
print(model)
print('Running predictions.')
tokenized, _, _ = st.tokenize_sentences(TEST_SENTENCES)
print(tokenized)
prob = model(tokenized)

for prob in [prob]:
    # Find top emojis for each sentence. Emoji ids (0-63)
    # correspond to the mapping in emoji_overview.png
    # at the root of the torchMoji repo.
    print('Writing results to {}'.format(OUTPUT_PATH))
    scores = []
    for i, t in enumerate(TEST_SENTENCES):
        t_tokens = tokenized[i]
        t_score = [t]
        t_prob = prob[i]
        ind_top = top_elements(t_prob, 5)
        t_score.append(sum(t_prob[ind_top]))
        t_score.extend(ind_top)
        t_score.extend([t_prob[ind] for ind in ind_top])
        scores.append(t_score)
        print(t_score)

    with open(OUTPUT_PATH, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=str(','), lineterminator='\n')
        writer.writerow(['Text', 'Top5%',
                        'Emoji_1', 'Emoji_2', 'Emoji_3', 'Emoji_4', 'Emoji_5',
                        'Pct_1', 'Pct_2', 'Pct_3', 'Pct_4', 'Pct_5'])
        for i, row in enumerate(scores):
            try:
                writer.writerow(row)
            except:
                print("Exception at row {}!".format(i))