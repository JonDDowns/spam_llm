"""
File: create_splits.py
Author: Jon Downs
Date: 5/24/2024
Description: Takes processed mailbox files and converts them into
             train/test/validation splits for Sequence Modeling.
             Currently one label: 'junk'.
"""

import os, logging, sys
from spam_llm.mailbox_folder import mbox_folder
import pickle as pkl
import yaml
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer

log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Load configuration settings
with open('config.yaml', 'r') as f:
    cfg = yaml.safe_load(f)
tokenizer = AutoTokenizer.from_pretrained(cfg['base_model'])

# These columns will be combined into a single field for model input
encode_cols = ['From', 'Subject', 'Received', 'Content']

# Loop through dataset, append to central set
all_data = []
for filepath in cfg['mailbox_folders']:
    log.info(f'Loading data/raw/{filepath}')
    fn = os.path.join('data/raw', filepath)
    with open(fn, 'rb') as f:
        raw = pkl.load(f)

        # If there are messages, load them and structure data for RoBERTa
        # Otherwise, note that the file is empty
        if len(raw.message_list) > 0:
            for msg in raw.message_list:
                try:
                    tmp_X = ' '.join([str(msg[x]) for x in encode_cols if x in msg])
                    tmp_X = tmp_X.split()
                    tmp_X = ' '.join(tmp_X)

                    all_data.append({
                        'text': tmp_X,
                        'label': 1 if raw.junk else 0,
                        'input_ids': tokenizer(tmp_X, truncation=True)['input_ids']
                    })
                except:
                    log.info('Something went wrong')
        else:
            log.info(f'{filepath} was an empty set')

log.info('Making training, validation, and testing sets')
train, val = train_test_split(all_data, test_size = 0.05, random_state=24)
val, test = train_test_split(val, test_size = 0.2, random_state=24)
out = {'train': train, 'val': val, 'test': test}

log.info('Saving splits at: data/processed/emails.pkl')
os.makedirs('data/processed', exist_ok=True)
with open('data/processed/emails.pkl', 'wb') as f:
    pkl.dump(out, f)
