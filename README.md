Example for a cookiecutter.json file:

```json
{
  "question_1": {
    "prompt": "What Powerranger you identify the most (Think of Power Ranger Samurai)?",
    "answer": ["yellow", "blue", "green", "gold", "pink"]
  },
  "question_2": {
    "prompt": "That sucks! Are you sure?",
    "answer": ["yes", "no"],
    "depends_on": {"question_1": "blue"}
  }
}
```