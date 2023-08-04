# Tsukiyo

## Introduction

Tsukiyo is a conversational AI project, it's divided into server-side and client-side.

The overall architecture diagram is [here](/docs/architecture.png).

### Server Side

This side consists of the following components:

* Automatic Speech Recognition (ASR)
* Text-to-Speech Synthesis (TTS)
* Large Language Models (LLMs)
* Natural Language Processing (NLP)

The server side provides conversational abilities to the client side.

### Client Side

This side integrates with different external APIs to implement conversational AI in various games/applications. 

For example, in VRChat, it can integrate with Windows sound and VRChat OSC to enable interactive dialogue.

## Requirements

* Python 3.10.12
* Pytorch
* NVIDIA GPU for training/inference

## Installation

Create a new conda environment and activate it.

```bash
conda create --name tsukiyo python==3.10.12
conda activate tsukiyo
```

Install dependencies using poetry.

```bash
pip install --upgrade pip
pip install poetry
poetry install
```

Run the program.

```bash
python src\main.py
```

## License

Tsukiyo is under [MIT License](/LICENSE).
