## Dependencies

- [Transformers](https://pypi.org/project/transformers/)
- [HTML Encoder](https://www.freeformatter.com/url-encoder.html#before-output)

- Install dependencies
  pip install

- Start project
  flask run

- Encode prompt you want to test into HTML Encoded query string
  https://www.freeformatter.com/url-encoder.html#before-output

- Target route with prompt key as query string and prompt as value. This one is for sentiment analysis
  http://127.0.0.1:5000/sentiment?prompt=Life+is+good+right+now

- Target route with prompt key as query string and prompt as value. This one is for subject analysis
  http://127.0.0.1:5000/subject?prompt=The+presidential+elections+are+this+year.
