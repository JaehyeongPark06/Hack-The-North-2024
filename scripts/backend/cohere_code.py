import os
import cohere 
import json

# Initialize a new CohereClient with an API key
cohere_client = cohere.Client(os.environ.get('COHERE_API_KEY', ''))

# Define commit templates
commit_templates = [
    {
        'name': 'Conventional Commits',
        'description': 'type(scope): subject',
        'pattern': r'^(feat|fix|docs|style|refactor|test|chore)(\([a-z ]+\))?: .{1,50}$'
    },
    {
        'name': 'Angular',
        'description': 'type(scope): subject',
        'pattern': r'^(build|ci|docs|feat|fix|perf|refactor|style|test)(\([a-z ]+\))?: .{1,50}$'
    }
]

# Set the default template to Conventional Commits
current_template = commit_templates[0]

def analyze_commit_message(message: str) -> str:
    try:
        # Send a request to the Cohere API for analysis
        response = cohere_client.chat(
            model="command-r",
            message=f"Analyze the following git commit message and provide feedback on its clarity, structure, and adherence to the {current_template['name']} template ({current_template['description']}). The user's git commit message is:\n\n{message}\n\nFeedback:"
        )
        return response.text.strip()
    except Exception as error:
        print(f'Error analyzing commit message: {error}')
        return 'Error analyzing commit message. Please try again.'

# cohere_code.py
def get_commit_message():
    # Read the git commit message from the COMMIT_EDITMSG file
    try:
        with open('.git/COMMIT_EDITMSG', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("The COMMIT_EDITMSG file was not found.")
    except Exception as e:
        raise Exception(f"Error reading COMMIT_EDITMSG file: {e}")


def main():
    commit_message = get_commit_message()
    analysis = analyze_commit_message(commit_message)
    with open('data/commit_analysis.txt', 'w') as file:
        file.write(analysis, file)
    print(f"Commit Analysis: {analysis}")

if __name__ == "__main__":
    main()