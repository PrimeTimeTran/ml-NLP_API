## Natural Language Processing(NLP)

Natural Language Processing using HuggingFace's pipelines that automatically loads a model & tokenizer.

The use of these tools allows us to do things like evaluate the sentiment of a prompt, classify it's subject, or generate additional text/context.

## Dependencies

- [Transformers](https://pypi.org/project/transformers/)
- [HTML Encoder](https://www.freeformatter.com/url-encoder.html#before-output)

## Setup

- Install dependencies
  `pip install`

- Start project
  `flask run`

- Encode prompt you want to test into HTML Encoded query string with [this tool](https://www.freeformatter.com/url-encoder.html#before-output)

## Demo

### 1. Classify Sentiment of a prompt

```sh
curl http://127.0.0.1:5000/sentiment?prompt=Life+is+good+right+now
curl http://127.0.0.1:5000/sentiment?prompt=Life+is+bad+right+now
curl http://127.0.0.1:5000/sentiment?prompt=Life+is+uncertain+right+now
```

### 2. Classify the subject of a prompt

```sh
curl http://127.0.0.1:5000/subject?prompt=The+presidential+elections+are+this+year
```

### 3. Generate additional text given a prompt

```sh
curl http://127.0.0.1:5000/generate?prompt=Roses+are+red
```
