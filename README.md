## Table of Contents

## About The Project

The code implements *HINTER*. *HINTER* combines mutation analysis and metamorphic oracles to automatically generate bias-prone test inputs that expose intersectional bias instances.

The approach uses a bias dictionary produced from [SBIC](https://paperswithcode.com/dataset/sbic) to generate a test suite containing bias mutations from texts.

The repository evaluates *HINTER* using [LexGLUE](https://github.com/coastalcph/lex-glue) Benchmark **four** legal datasets (*Ecthr*, *Scotus*, *Eurlex*, *Ledgar*) and **four** LLM architectures (*BERT*, *Legal-BERT*, *RoBERTA*, *DeBERTA*) resulting in **16** models to evaluate **three** sensitive attributes (*race*, *gender*, *body*). In addition, we use Llama2 and GPT3.5 in our experiments, and IMDB, for a total of **18** models and **five** datasets.

Details of the performance of our fine-tuned models versus the original from [LexGLUE](https://github.com/coastalcph/lex-glue).

More details can be found in the [paper](7817HINTERExposingHidden.pdf), and in the [supplementary material](supplementary_material.pdf).

Some hidden fairness issues can be tested in this [hugging face space](https://huggingface.co/spaces/Anonymous1925/Hinter).

## Getting Started

Reproducing the testing takes weeks, and even the processing of the results requires hours as it involves opening and processing a multitude of files.

If you want to simply test the tool on your data, you can find the tool with a README adapted inside the folder [Hinter\_tool\_usage](./Hinter_tool_usage).

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

A script located at `src/script.sh` can be used to run the code on all lists for both atomic and intersectional methods across all models.



### Llama/GPT Models

#### Setup

- Ensure all dependencies in `requirements_gen_llm.txt` are installed. Use a separate virtual environment specifically for Llama/GPT experiments to prevent conflicts with BERT dependencies.
- Download the IMDB dataset from [this link](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews) if you plan to test it.
- Access the Llama model `meta-llama/Llama-2-7b-chat-hf` on Hugging Face. You may need to complete a form to request access from Meta [here](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf).
- Use OpenAI's `gpt-3.5-turbo-0125` model. Ensure you have sufficient credits in your OpenAI account. You can manage credits and billing [here](https://platform.openai.com/settings/organization/billing/overview) and find specific billing details for the `gpt-3.5-turbo-0125` model [here](https://platform.openai.com/docs/models/gpt-3-5#gpt-3-5-turbo).

Tokens for accessing both models will be required during testing.

#### Testing

To test Llama and GPT models, you must first generate the mutants using the [mutation\_llms.py](./src/mutation_llms.py) script. This script processes the dataset with the specified dictionaries to produce the mutants. Below are the parameters for the script:

- `dataset_name`: Name of the dataset to use.
- `dict_path`: Path to the sensitive attribute pair of words.
- `set`: Dataset split to process (`train`, `validation`, `test`).
- `--inter_dict_path` (optional): Path to the second words file for intersectional bias testing. Required for intersectional methods.
- `--output_path` (optional): Directory where the generated mutants will be saved (default: `../output/`).
- `--data_path` (optional): Path to the folder containing the IMDB dataset. The default path for IMDB is `../data/imdb/imdb.csv`. If the dataset file moves, for example to `../../dataset/imdb/imdb.csv`, you need to update `--data_path` to `../../dataset/`.

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

