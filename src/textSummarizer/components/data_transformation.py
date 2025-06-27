import os
from textSummarizer.logging import logger
from transformers import AutoTokenizer
from datasets import load_dataset, load_from_disk
from textSummarizer.entity import DataTransformationConfig



class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_name, use_fast=False)
    # def __init__(self, config: DataTransformationConfig):
    #     self.config = config
    #     tokenizer_name = str(self.config.tokenizer_name).replace("\\", "/")
    #     self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def convert_examples_to_features(self, example_batch):
        input_recordings = self.tokenizer(example_batch['dialogue'], max_length=1024, truncation=True, padding='max_length')

        with self.tokenizer.as_target_tokenizer():
            target_recordings = self.tokenizer(example_batch['summary'], max_length=128, truncation=True, padding='max_length')
        return {
            'input_ids': input_recordings['input_ids'],
            'attention_mask': input_recordings['attention_mask'],
            'labels': target_recordings['input_ids']
        }
    def convert(self):
        dataset_samsum = load_from_disk(self.config.data_path)
        dataset_samsum_pt = dataset_samsum.map(self.convert_examples_to_features, batched=True)
        dataset_samsum_pt.save_to_disk(os.path.join(self.config.root_dir, 'samsum_dataset'))