from typing import Optional

import datasets
import fire
from llama import Llama
from tools import methods
from nltk.tokenize import word_tokenize

def main(
    tokenizer_path: str = "models/tokenizer.model",
    ckpt_dir: str = "models/7b-chat/",
    temperature: float = 0,
    top_p: float = 0.9,
    max_seq_len: int = 1024,
    max_batch_size: int = 4,
    max_gen_len: Optional[int] = 3):
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    pick = methods.getFromPickle("../generative_ai/ecthr_a_selected_bias.pkl", "rb")

    data_name= "ecthr_a"
    dataset_name_question = "ECTHR"
    articles = ["Article 2", "Article 3", "Article 5", "Article 6", "Article 8", "Article 9", "Article 10", "Article 11", "Article 14", "Article 1 of Protocol 1"]

    dict_result = dict()
    errors_list = pick['body']+pick['race']+pick['gender']
    ##Lama######################
    ############################
    result = []
    for case in range(0,len(errors_list)):
        line = errors_list[case]
        truncated_case = line[3][5]
        if case%50 == 0:
            print(">>>Doing case ", case, "/", len(errors_list))
        article_violated = []
        answers = []
        for article_num in range(0,len(articles)):
            question = "Is "+ articles[article_num] + " of the "+ dataset_name_question + " violated in the following case ? Reply with a binary answer without explanation : " + truncated_case +"."
            dialogs = [[{"role": "user", "content": question}]]
            answer = generator.chat_completion(
                dialogs,  # type: ignore
                max_gen_len=max_gen_len,
                temperature=temperature,
                top_p=top_p,
            )[0]['generation']['content']
            answers.append(answer)
            if answer.lower().replace(' ', '').startswith("yes") : article_violated.append(article_num)
        result.append([article_violated, answers]+line)
        print(article_violated)
    methods.writePickle(result, "result_original_"+data_name+"_lama.pkl", 'wb')
    print("Done")

fire.Fire(main)