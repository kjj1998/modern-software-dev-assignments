# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: Koh Jun Jie \
SUNet ID: NA \
Citations: NA

This assignment took me about 5 hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
response = chat(
    model="llama3.1",
    messages=[
        {
            "role": "system",
            "content": "Extract all action items from the given text. Action items are tasks, to-dos, or things that need to be done.",
        },
        {
            "role": "user",
            "content": text,
        },
    ],
    format=ActionItems.model_json_schema(),
)
``` 

Generated Code Snippets:
```
class ActionItems(BaseModel):
    action_items: List[str]


def extract_action_items_llm(text: str) -> List[str]:
    response = chat(
        model="llama3.1",
        messages=[
            {
                "role": "system",
                "content": "Extract all action items from the given text. Action items are tasks, to-dos, or things that need to be done.",
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        format=ActionItems.model_json_schema(),
    )
    
    result = ActionItems.model_validate_json(response.message.content or "")
    return result.action_items
```

### Exercise 2: Add Unit Tests
Prompt: 
```
Write unit tests for extract_action_items_llm() covering multiple inputs (e.g., bullet lists, keyword-prefixed lines, empty input) in week2/tests/test_extract.py.
``` 

Generated Code Snippets:
```python
def test_llm_bullet_list():
    text = """
    - Buy groceries
    - Schedule dentist appointment
    - Fix the leaking faucet
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) >= 3
    joined = " ".join(items).lower()
    assert "groceries" in joined
    assert "dentist" in joined
    assert "faucet" in joined


def test_llm_keyword_prefixed_lines():
    text = """
    todo: Update the README
    action: Review pull request #42
    next: Deploy to staging
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) >= 3
    joined = " ".join(items).lower()
    assert "readme" in joined
    assert "pull request" in joined
    assert "staging" in joined


def test_llm_empty_input():
    items = extract_action_items_llm("")
    assert isinstance(items, list)
    assert len(items) == 0


def test_llm_no_action_items():
    text = "The weather today is sunny and warm. I enjoyed my lunch."
    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) == 0


def test_llm_mixed_format():
    text = """
    Meeting notes:
    We discussed the roadmap. Everyone is happy with progress.
    - [ ] Write unit tests for auth module
    * Refactor database layer
    todo: Set up CI pipeline
    Also remember to update the docs.
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) >= 3
    joined = " ".join(items).lower()
    assert "test" in joined
    assert "database" in joined or "refactor" in joined
    assert "ci" in joined or "pipeline" in joined
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
refactor the code in action_items.py
refactor the code in notes.py
refactor extract.py
``` 

Generated/Modified Code Snippets:
```
action_items.py lines 15 to 83
notes.py lines 12 to 39
extract.py lines 6 to 83
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
Create a new /extract-llm endpoint that makes use of the extract_action_items_llm function
Update the frontend in frontend/index.html to include an "Extract LLM" button that when clicked, triggers the extraction process via the /extract-llm endpoint
Create an endpoint that retrieves all notes saved
Update the frontend to include a "List Notes" button that, when clicked, fetches and displays all saved notes
``` 

Generated Code Snippets:
```
notes.py lines 70 to 83
index.html lines 78 to 97
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
Analyze all the code in the week2 directory and generate a well-structured README.md file
The README should include, at a minimum:
- A brief overview of the project
- How to set up and run the project
- API endpoints and functionality
- Instructions for running the test suite
``` 

Generated Code Snippets:
```
README.md entire file
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 