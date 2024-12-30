# listy

Turns voice messages into letters (these long-form text things people barely write anymore).

## Usage

Install [PDM](https://pdm-project.org/) and run `pdm install` to install the dependencies.

Populate `.env` with your [Groq API key](https://console.groq.com/keys).

Then run `pdm listy file1.ogg file2.wav` to transcribe some files. The output will be printed to the console.
