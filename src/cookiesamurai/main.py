# cookiesamurai/main.py
import argparse
import os
import requests
import json
from cookiecutter.main import cookiecutter


def get_answer(prompt, answer):
    print(f"{prompt}[{answer}]:")
    if isinstance(answer, list):
        print('oooo\n')
        choices = []
        for i, option in enumerate(answer):
            print(f"{i + 1}. {option}")
            choices.append(i + 1)
        valid = False
        while not valid:
            choice = input("Enter choice number: ")
            try:
                choice = int(choice)
                valid = choice in choices
                if not valid:
                    print(f'{choice} is an invalid choice.')
                else:
                    answer = answer[choice - 1]
            except:
                print(f'{choice} is an invalid choice.')
    else:
        answer = input()
    return answer


def prompt_cookiecutter_json(cookiecutter_json):
    res = {}
    for key, value in cookiecutter_json.items():
        depends_on = None
        if isinstance(value, dict) and value.get('prompt'):
            prompt = value.get('prompt')
            answer = value.get('answer')
            if value.get('depends_on'):
                depends_on = value['depends_on']
        else:
            prompt = key
            answer = value
        if prompt.startswith('__'):
            res[key] = value
        elif depends_on is None or (isinstance(depends_on, dict)):
            if isinstance(depends_on, dict):
                valid = True
                for key in depends_on:
                    valid = valid and res[key] == depends_on[key]
            if depends_on is None or valid:
                res[key] = get_answer(prompt, answer)
            else:
                res[key] = 'DEFAULT'
    return res


def main():
    parser = argparse.ArgumentParser(description='A Cookiecutter wrapper for advanced user prompts.')
    parser.add_argument('template', help='The template to use (can be a GitHub repository or local directory)')

    args = parser.parse_args()

    template = args.template

    # Check if the template is a GitHub repository
    if template.startswith("https://github.com/"):
        # Extract the repository name and branch from the URL
        parts = template.replace("https://github.com/", "").split("/")
        repo_name = parts[0] + "/" + parts[1]
        branch = "main"  # Change this to the branch name you want to use

        # Construct the URL for the raw cookiecutter.json file
        url = f"https://raw.githubusercontent.com/{repo_name}/{branch}/cookiesamurai.json"

        # Send a request to retrieve the cookiecutter.json file
        response = requests.get(url)
        if response.status_code == 200:
            # Load the JSON data from the response
            cookiecutter_json = json.loads(response.text)
        else:
            print(f"Unable to retrieve cookiesamurai.json from {url}")
            return

    elif os.path.isdir(template):
        # Get the path to the cookiecutter.json file in the local directory
        cookiecutter_json_path = os.path.join(template, "cookiesamurai.json")
        if os.path.exists(cookiecutter_json_path):
            # Load the JSON data from the local file
            with open(cookiecutter_json_path, "r") as f:
                cookiecutter_json = json.load(f)
        else:
            print(f"No cookiesamurai.json found in {template}")
            return
    else:
        print(f"Unrecognized template format: {template}")
        return

    cookiecutter_json = prompt_cookiecutter_json(cookiecutter_json)

    # path to the Cookiecutter template


    # generate the project using the context dictionary
    cookiecutter(template, no_input=True, extra_context=cookiecutter_json)
