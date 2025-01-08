## Table of Contents

## About The Project

The code implements *HINTER*. *HINTER* combines mutation analysis and metamorphic oracles to automatically generate bias-prone test inputs that expose intersectional bias instances.

The approach uses a bias dictionary produced from [SBIC](https://paperswithcode.com/dataset/sbic) to generate a test suite containing bias mutations from texts.

The repository evaluates *HINTER* using [LexGLUE](https://github.com/coastalcph/lex-glue) Benchmark **four** legal datasets (*Ecthr*, *Scotus*, *Eurlex*, *Ledgar*) and **four** LLM architectures (*BERT*, *Legal-BERT*, *RoBERTA*, *DeBERTA*) resulting in **16** models to evaluate **three** sensitive attributes (*race*, *gender*, *body*). In addition, we use Llama2 and GPT3.5 in our experiments, and IMDB, for a total of **18** models and **five** datasets.

Details of the performance of our fine-tuned models versus the original from [LexGLUE](https://github.com/coastalcph/lex-glue).

More details can be found in the [paper](7817HINTERExposingHidden.pdf), and in the [supplementary material](supplementary_material.pdf).

Some hidden fairness issues can be tested in this [hugging face space](https://huggingface.co/spaces/Anonymous1925/Hinter).

## Getting Started

If you want to simply test the tool on your data, you can find the tool with a README adapted inside the folder [Hinter_tool_usage](./Hinter_tool_usage).

This section explains how to install the necessary components and launch the experiments. 

**Important:**

Due to a known issue with Python's hash seed, it is recommended to run all scripts with the following command to ensure consistency and reproducibility:

```
PYTHONUNBUFFERED=1 PYTHONHASHSEED=0 python your_script.py
```

### Prerequisites

The experiments were tested on both Windows and Linux (Ubuntu 20.04).

- Python 3.8.
- At least one non-hierarchical model trained from [LexGLUE](https://github.com/coastalcph/lex-glue) (all 16 combinations of BERT models/datasets cited above to reproduce everything).
- Access to the Llama model `meta-llama/Llama-2-7b-chat-hf` on Hugging Face. You may need to complete a form to request access from Meta [here](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf).
- Access to OpenAI's `gpt-3.5-turbo-0125` model. Ensure sufficient credits in your OpenAI account. You can manage credits and billing [here](https://platform.openai.com/settings/organization/billing/overview) and find specific billing details [here](https://platform.openai.com/docs/models/gpt-3-5#gpt-3-5-turbo).
- Tokens for accessing both models will be required during testing.

It is recommended to use **separate virtual environments** for BERT models and Llama/GPT models to avoid dependency conflicts. This ensures a smoother setup and operation for each model type.

## Usage

### BERT Models

#### Setup

- Ensure all dependencies in `requirements_bert_mutation.txt` are installed. It is best to use a dedicated virtual environment for BERT-related experiments.

#### Training

Train the BERT models using the datasets specified in [LexGLUE](https://github.com/coastalcph/lex-glue).

#### Testing

To test a BERT model, simply launch `mutation.py` with the appropriate parameters. Be sure to test a model for biases using the datasets it was trained with.

- `model`: Path to the model you want to test.
- `dataset_path`: Hugging Face path to the dataset.
- `dict_path`: Path to the sensitive attribute pair of words.
- `description`: Technique description.
- `method`: Method to use for text modification (`replacement`, `deletion`, `intersectional`).
- `set`: Dataset split to test (`train`, `validation`, `test`).
- `--inter_dict_path` (optional): Path to the second words file for intersectional bias testing. Required only if `method` is `intersectional`.
- `--length` (optional): Maximum text length to truncate (default: 512).
- `--mutation_only` (optional): If set, only generate mutants without testing.

Here is an example of usage where a *bert-base-uncased* model trained with *ecthr_a* is intersectional bias tested with both *race* and *gender* sensitive attributes on the *test* split of *ecthr_a*:

```bash
python3 mutation.py model/ecthr_a/bert-base-uncased/ lex_glue data/race/american_asian.csv \
    --inter_dict_path=data/gender/male_female.csv \
    race_gender intersectional test
```

Once finished, the program should have created an *Output* folder with the results in it.

#### Results Interpretation

The results are saved in the `Output` folder, organized by the following structure:

```
output/
  └── dataset_name/
        └── model_name/
              └── split_name/
                    └── result.csv
```

Here is a breakdown of the output file and how to interpret it:

- **`result.csv`**:
   - **Description**: This file contains a summary of the fairness testing process.
   - **Columns**:
     - `Technique`: The method used for text modification (e.g., `replacement`, `deletion`, or `intersectional`) combined with the technique description.
     - `model`: The name of the tested model.
     - `dataset`: The name of the dataset used.
     - `num_errors`: The number of instances where the model's predictions changed after applying mutations.
     - `num_occurrences`: The total number of words replaced/mutated across the dataset. **This value includes mutants that did not pass the semantic similarity check.**
     - `num_cases_modified`: The number of cases in the dataset where at least one mutation occurred.
     - `err_rate`: The ratio of `num_errors` to `num_cases_modified`. This represents the error rate of the model under bias mutations.
     - `time (s)`: The total time taken to perform the testing in seconds.
     - `word_file`: The dictionary of sensitive words used for the mutations.
   - **How to Read**: This file provides an overall summary of the testing process and is useful for comparing quickly the performance of different models and techniques.

### Llama/GPT Models

#### Setup

- Ensure all dependencies in `requirements_gen_llm.txt` are installed. Use a separate virtual environment specifically for Llama/GPT experiments to prevent conflicts with BERT dependencies.
- Download the IMDB dataset from [this link](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews) if you plan to test it.
- Access the Llama model `meta-llama/Llama-2-7b-chat-hf` on Hugging Face. You may need to complete a form to request access from Meta [here](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf).
- Use OpenAI's `gpt-3.5-turbo-0125` model. Ensure you have sufficient credits in your OpenAI account. You can manage credits and billing [here](https://platform.openai.com/settings/organization/billing/overview) and find specific billing details for the `gpt-3.5-turbo-0125` model [here](https://platform.openai.com/docs/models/gpt-3-5#gpt-3-5-turbo).

Tokens for accessing both models will be required during testing.

#### Testing

Instructions on testing Llama and GPT models will be added here in the future.

## Contact

Anonymous

## Acknowledgments

- [ECTHR Dataset](https://github.com/coastalcph/lex-glue#ecthr-a) via LexGLUE for evaluating fairness in European Court of Human Rights cases.
- [EURLex Dataset](https://github.com/coastalcph/lex-glue#eurlex) via LexGLUE for providing legal texts for language model evaluation.
- [LEDGAR Dataset](https://github.com/coastalcph/lex-glue#ledgar) via LexGLUE for offering resources for legal contract analysis.
- [SCOTUS Dataset](https://case.law/) for providing access to Supreme Court legal cases used in testing.
- [Hugging Face](https://huggingface.co) for hosting models like `meta-llama/Llama-2-7b-chat-hf`.
- [LexGLUE](https://github.com/coastalcph/lex-glue) for legal language benchmarks.
- [SBIC](https://paperswithcode.com/dataset/sbic) for the bias dictionary.
- [IMDB Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews) for sentiment analysis.
- [Best README Template](https://github.com/othneildrew/Best-README-Template/tree/master) for the format inspiration.

