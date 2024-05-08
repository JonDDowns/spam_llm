"""
File: train.py
Author: Jon Downs
Date: 5/24/2024
Description: Training script for the spam_llm model. Relies heavily on settings in config.yaml
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding, TrainingArguments, Trainer
import logging, sys
import pickle as pkl
from spam_llm import compute_metrics
import yaml

log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

log.info('Loading config.yaml...')
with open('config.yaml', 'r') as f:
    cfg = yaml.safe_load(f)

log.info('Loading tokenizer...')
tokenizer = AutoTokenizer.from_pretrained(cfg['base_model'])

log.info('Loading data...')
with open('data/processed/emails.pkl', 'rb') as f:
    emails = pkl.load(f)


log.info('Creating model...')
id2label = {0: "Not spam", 1: "Spam"}
label2id = {"Not spam": 0, "Spam": 1}
spam_model = AutoModelForSequenceClassification.from_pretrained(
    cfg['base_model'],
    num_labels=2,
    id2label=id2label,
    label2id=label2id
)

log.info('Create trainer and begin')
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
training_args = TrainingArguments(
    output_dir=cfg['model_output_dir'],
    learning_rate=cfg['learning_rate'],
    per_device_train_batch_size=cfg['per_device_train_batch_size'],
    gradient_accumulation_steps=cfg['gradient_accumulation_steps'],
    per_device_eval_batch_size=cfg['per_device_eval_batch_size'],
    num_train_epochs=cfg['num_train_epochs'],
    weight_decay=cfg['weight_decay'],
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=spam_model,
    args=training_args,
    train_dataset=emails["train"],
    eval_dataset=emails["val"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics
)

trainer.train()
