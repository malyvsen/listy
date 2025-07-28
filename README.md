# listy

Turns voice messages into letters (these long-form text things people barely write anymore).

## Usage

1. Install [`moon`](https://moonrepo.dev/) and [`uv`](https://docs.astral.sh/uv/).

1. Populate `.env` with your [Groq API key](https://console.groq.com/keys).

1. Run `moon run run -- file1.ogg file2.wav` to transcribe some files. The output will be printed to the console. You can also add `--language` - by default, it's `pl`, because let's face it, I'm making this for my own use.
