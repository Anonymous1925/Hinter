<a name="readme-top"></a>

<br />
<div align="center">

<h3 align="center">HINTER</h3>

  <p align="center">
  HINTER's code and experimental data repository. This is the repository for the paper titled "HINTER: Exposing Hidden Intersectional Bias in Large Language Models".
    <br />
    <br />
    <br />
  </p>
</div>

The [paper](7817HINTERExposingHidden.pdf) and [supplementary material](supplementary_material.pdf) can be found in the repository. 

## Table of Contents
<details>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
              </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#llm-testing">LLM Testing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



## About The Project

The code implements *HINTER*. *HINTER* combines mutation analysis and metamorphic oracles to automatically generate bias-prone test inputs that expose intersectional bias instances. 

The approach uses a bias dictionary produced from [SBIC](https://paperswithcode.com/dataset/sbic) to generate a test suite containing bias mutations from texts.

The repository evaluates *HINTER* using [LexGLUE](https://github.com/coastalcph/lex-glue) Benchmark **four** legal datasets (*Ecthr A*, *Scotus*, *Eurlex*, *Ledgar*) and **four** LLM architectures (*BERT*, *Legal-BERT*, *RoBERTA*, *DeBERTA*) resulting in **16** models to evaluate **three** sensitive attributes (*race*, *gender*, *body*). In addition, we use Llama2 and GPT3.5 in our experiments, and IMDB, for a total of **18** models and **five** datasets. <!--Note that only the non-hierarchical were used.-->

Details of the performance of our fine-tuned models versus the original from [LexGLUE](https://github.com/coastalcph/lex-glue).

More details can be found in the [paper](7817HINTERExposingHidden.pdf), and in the [supplementary material](supplementary_material.pdf).

Some hidden fairness issues can be tested in this [hugging face space](https://huggingface.co/spaces/Anonymous1925/Hinter).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Getting Started

This section explains how to install the necessary components and launch the experiments.

### Prerequisites
The experiments were tested on both Windows and Linux (Ubuntu 20.04). 

**Important:**

It is recommended to use **separate virtual environments** for BERT models and Llama/GPT models to avoid dependency conflicts. This ensures a smoother setup and operation for each model type.
* At least one non-hierarchical model trained from [LexGLUE](https://github.com/coastalcph/lex-glue) (all 16 combinations of BERT models/datasets cited above to reproduce everything)
* Python 3.8

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Usage

### BERT Models

#### Setup

* Ensure all dependencies in `requirements_bert_mutation.txt` are installed. It is best to use a dedicated virtual environment for BERT-related experiments.

#### Training
Train the BERT models using the datasets specified in [LexGLUE](https://github.com/coastalcph/lex-glue).

#### Testing
To test a BERT model, simply launch ```mutation.py``` with the appropriate parameters. Be sure to test a model for biases using the datasets it was trained with.

* ```model``` : the path to the model you want to test.
* ```dataset_path``` : the path to the dataset (can be a local path, or a path to a [Hugging Face](https://huggingface.co/) datasets proposed in [LexGLUE](https://github.com/coastalcph/lex-glue)).
* ```dict_path``` : the path to the sensitive attribute pair of words.
* ```method``` : modification method to use between ```replacement```, ```intersectional``` and ```deletion```.
* ```set``` : set to test between ```train```, ```validation```, and ```test```.
* (Optional) ```inter_dict_path``` : path to the second ```dataset_path``` to use for intersectional bias testing. Only use it if ```intersectional``` is set for ```method``` as it is necessary.
* (Optional) ```description``` : a tag that will be added to the results.

Here is an example of usage where a *bert-base-uncased* model trained with *ecthr_a* is intersectional bias tested with both *race* and *gender* sensitive attributes on the *test* split of *ecthr_a* :

```python3 mutation.py model/ecthr_a/bert-base-uncased/ lex_glue data/race/american_asian.csv --inter_dict_path=data/gender/male_female.csv race_gender intersectional test```

Once finished, the program should have created an *Output* folder with the results in it.

### Llama/GPT Models

#### Setup

* Ensure all dependencies in `requirements_gen_llm.txt` are installed. Use a separate virtual environment specifically for Llama/GPT experiments to prevent conflicts with BERT dependencies.
* Download the IMDB dataset from [this link](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews) if you plan to test it.
* Access the Llama model `meta-llama/Llama-2-7b-chat-hf` on Hugging Face. You may need to complete a form to request access from Meta [here](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf).
* Use OpenAI's `gpt-3.5-turbo-0125` model. Ensure you have sufficient credits in your OpenAI account.

Tokens for accessing both models will be required during testing.

#### Testing

Instructions on testing Llama and GPT models will be added here in the future.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Contact
<!-- TODO -->
Anonymous
<!--
 Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com 

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)
-->
<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Acknowledgments

* [LexGLUE](https://github.com/coastalcph/lex-glue)
* [SBIC](https://paperswithcode.com/dataset/sbic)
* [IMDB Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews)
* [Best README Template](https://github.com/othneildrew/Best-README-Template/tree/master)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

