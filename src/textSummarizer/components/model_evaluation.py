from transformers import AutoModelForSeq2SeqLM , AutoTokenizer
from datasets import load_dataset, load_from_disk
import evaluate
import torch
import pandas as pd
from tqdm import tqdm
from textSummarizer.entity import ModelEvaluationConfig


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig()):
        self.config = config

    def generate_batch_sized_chunks(self,list_of_elements, batch_size):
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i : i + batch_size]



    def calculate_metric_on_test_ds(self,dataset, metric, model, tokenizer,batch_size=16,
            device="cuda" if torch.cuda.is_available() else "cpu",column_text="article",column_summary="highlights"):
        article_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))

        for article_batch, target_batch in tqdm(
            zip(article_batches, target_batches), total=len(article_batches)):

            inputs = tokenizer(article_batch, max_length=1024,  truncation=True,
                            padding="max_length", return_tensors="pt")

            summaries = model.generate(input_ids=inputs["input_ids"].to(device),
                            attention_mask=inputs["attention_mask"].to(device),
                            length_penalty=0.8, num_beams=8, max_length=128)
            # Finally, we decode the generated texts,
            # replace the  token, and add the decoded texts with the references to the metric.
            decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True,
                                    clean_up_tokenization_spaces=True)
                for s in summaries]

            decoded_summaries = [d.replace("", " ") for d in decoded_summaries]


            metric.add_batch(predictions=decoded_summaries, references=target_batch)

        #  Finally compute and return the ROUGE scores.
        score = metric.compute()
        return score
    
    def evaluate(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)
        dataset_samsum_pt = load_from_disk(self.config.data_path)
        rogue_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
        rogue_metric =  evaluate.load("rouge")
        score = self.calculate_metric_on_test_ds(dataset_samsum_pt["test"][0:10], rogue_metric, model_pegasus, 
                                                 tokenizer, batch_size=2, device=device, column_text = 'dialogue', column_summary= 'summary')
        rogue_dict = dict((rn, score[rn].fmeasure) for rn in rogue_names)
        # rouge_dict = dict((rn, score[rn].mid.fmeasure ) for rn in rouge_names )
        df = pd.DataFrame(rogue_dict, index=['pegasus'])
        df.to_csv(self.config.metrics_file_name, index=False)



# class ModelEvaluation:
#     def __init__(self, config: ModelEvaluationConfig):
#         self.config = config
#         # self.model = AutoModelForSeq2SeqLM.from_pretrained(config.model_path)
#         # self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_path)
#         # self.metric = evaluate.load("rouge")

#     def generate_batch_sized_chunks(self,list_of_elements, batch_size):
#         for i in range(0, len(list_of_elements), batch_size):
#             yield list_of_elements[i : i + batch_size]



#     def calculate_metric_on_test_ds(self,dataset, metric, model, tokenizer,batch_size=16,
#             device="cuda" if torch.cuda.is_available() else "cpu",column_text="article",column_summary="highlights"):
#         article_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
#         target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))

#         for article_batch, target_batch in tqdm(
#             zip(article_batches, target_batches), total=len(article_batches)):

#             inputs = tokenizer(article_batch, max_length=1024,  truncation=True,
#                             padding="max_length", return_tensors="pt")

#             summaries = model.generate(input_ids=inputs["input_ids"].to(device),
#                             attention_mask=inputs["attention_mask"].to(device),
#                             length_penalty=0.8, num_beams=8, max_length=128)
#             # Finally, we decode the generated texts,
#             # replace the  token, and add the decoded texts with the references to the metric.
#             decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True,
#                                     clean_up_tokenization_spaces=True)
#                 for s in summaries]

#             decoded_summaries = [d.replace("", " ") for d in decoded_summaries]


#             metric.add_batch(predictions=decoded_summaries, references=target_batch)

#         #  Finally compute and return the ROUGE scores.
#         score = metric.compute()
#         return score
    
#     def evaluate(self):
#         device = "cuda" if torch.cuda.is_available() else "cpu"
#         tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
#         model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)
#         dataset_samsum_pt = load_from_disk(self.config.data_path)
#         rogue_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
#         rogue_metric =  evaluate.load("rouge")
#         score = self.calculate_metric_on_test_ds(dataset_samsum_pt["test"][0:10], rogue_metric, model_pegasus, 
#                                                  tokenizer, batch_size=2, device=device, column_text = 'dialogue', column_summary= 'summary')
#         rogue_dict = dict((rn, score[rn].mid.fmeasure) for rn in rogue_names)
#         # rouge_dict = dict((rn, score[rn].mid.fmeasure ) for rn in rouge_names )
#         df = pd.DataFrame(rogue_dict, index=['pegasus'])
#         df.to_csv(self.config.metrics_file_name, index=False)
