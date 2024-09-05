## Innoboost

## Dependencies

- [Transformers](https://pypi.org/project/transformers/)
- [HTML Encoder](https://www.freeformatter.com/url-encoder.html#before-output)

## Setup

- Install dependencies
  `pip install`

- Start project
  `flask run`

- Encode prompt you want to test into HTML Encoded query string with [this tool](https://www.freeformatter.com/url-encoder.html#before-output)

- Target route with prompt key as query string and prompt as value. This one is for sentiment analysis
  http://127.0.0.1:5000/sentiment?prompt=Life+is+good+right+now

- Target route with prompt key as query string and prompt as value. This one is for subject analysis
  http://127.0.0.1:5000/subject?prompt=The+presidential+elections+are+this+year

- Target route with prompt key as query string and prompt as value. To complete a sentence:
  http://127.0.0.1:5000/generate?prompt=Roses+are+red

## Technology stacks

Langflow, Haystack, Gradio, Vercel AI SDK

1. Create a new prompt chat
   POST https://api.1long.ai/chats/new
   2. Show history of chats
   GET https://api.1long.ai/chats
   [
    {
      id: null,
      prompt: 'what is RAG'
    },
   ]

2. Show history of chats
   GET https://api.1long.ai/chats
   [
    {
      id: 123abc,
      title: 'what is RAG'
    },
    {
      id: 123abcdef,
      title: 'what is AL/ML'
    },
   ]

3. Get detailed & most recent messages for the chat.
   GET https://api.1long.ai/chats/[id]

   [
    {
      id: 123abc,
      user: 'Loi',
      body: 'what is RAG'
    },
    {
      id: 123abcdef,
      user: 'AI',
      body: 'Rag is a too lblah blah blah'
    }
   ]

```sh
# Example
GET https://api.1long.ai/chats/1231929812828abassuyv121
```
