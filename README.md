# Audio Transcription-Translation App

A transcription and translation app for 8 Languages. 
The transcription is based on the Whisper model from OpenAI, the GUI structure is borrowed from the whisper-gui-app repository of iamironman0 and for translation the Helsinki NLP models where used.

## Preview
![Bildschirm­foto 2023-04-25 um 19 46 40](https://user-images.githubusercontent.com/110823380/234359644-d3adeda0-45e0-4af9-9f77-9efb44f5fac8.png)

## Features
  - Models: Tiny, Base, Small, Medium, Large
  - Languages: German, English, Spanish, Italian, French, Japanese, Korean, Chinese
  - Task: Transscribe, Translate
  - Save result to a txt file
  - Change appearnce mode

## Setup
### Requirements
- Python version 3.9
- customtkinter
- torch
- ffmpeg
- pyaudio
- pydub
- transformers

1. Run this command to install the requirements:
```
pip install -r requirements.txt
```

2. Run program by executing this command in the shell/terminal in the directory where it is saved:
```
python3 main.py
```

## Known Issues
OpenAI's Whisper model can only work with audio files that are 30 seconds long.
To circumvent this issue, the audio recording and file will be split into 30-second chunks if they are longer than 30 seconds and will be processed that way by the Whisper Model.
However, this can lead to mistakes when words get cut into two different audio files.

## Acknowledgements
  - Whisper Model from OpenAI:                https://github.com/openai/whisper
  - Basic GUI structure from this repository: https://github.com/iamironman0/whisper-gui-app
  - Translation models from hugginface:       https://huggingface.co/Helsinki-NLP
