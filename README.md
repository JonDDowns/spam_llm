# spam_llm

spam_llm finetunes a large language model on Thunderbird inboxes to detect spam.

# Getting Started

Start by installing the module with:

```{bash}
# Clone repo, install
git clone https://JonDDowns/spam_llm.git
cd ./spam_llm
pip install .

# Make directories for model checkpoints and input data
mkdir checkpoints
mkdir data
```

Next, make a config.yaml file in the project root.
Use [config_example.yaml](./config_example.yaml) as a template.
While still in root, run the project scripts in this order:

```{bash}
python ./scripts/mbox_to_pickle.py
python ./scripts/create_splits.py
python ./scripts/train.py
```

# Contents

The [spam_llm](./spam_llm) subfolder includes helper utilities for parsing mailbox folders and setting up a trainer. 
A configuration file is expected at [config.yaml](./config.yaml).
This will specify the root directory of your Thunderbird inbox as well as the specific Berkley mailbox (mbox) files you wish to read in.
That mbox is not a universally consistent format, so custom handling was required based on my personal setup.
Your mileage may vary.
The code will skip any messages it is not successfully able to parse.
[./scripts/mbox_to_pickle.py] parses the mailbox files.
[./scripts/create_splits.py] creates train/test/validation splits.
And, finally, [./scripts/train] kicks off model training.
