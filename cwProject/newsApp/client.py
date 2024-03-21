import requests
import argparse
import sys
import json
import os
import random
from prettytable import PrettyTable
def LogIn(url, username, password):
    data = {
        'username': username,
        'password': password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post("https://" + url + "/api/login", data=data, headers=headers)
    return r


def LogOut(token):
    headers = {
        'Authorization': f'Token {token}'
    }
    r = requests.post("http://fy19ahh.pythonanywhere.com/api/logout", headers=headers)
    if r.status_code == 200:
        return r.json().get('token')
    else:
        return None

def Post(token, headline, category, region, details):
        data = {
        'headline': headline,
        'category': category,
        'region' : region,
        'details' : details
    }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {token}'
        }
        r = requests.post("http://fy19ahh.pythonanywhere.com/api/stories", data=json.dumps(data), headers=headers)
        if r.status_code != 200:
            return (r)

def List():
    directory_url = "http://newssites.pythonanywhere.com/api/directory/"
    response = requests.get(directory_url)
    agencies = response.json()
    random_agencies = random.sample(agencies, 20)

    return random_agencies


def News(id, category, region, date):
    agency_url = None
    directory_url = "http://newssites.pythonanywhere.com/api/directory/"
    response = requests.get(directory_url)
    all_stories = []
    try:
        agencies = response.json()
    except:
        return ("Could not gather Stories")

    for agency in agencies:
        if id and agency["agency_code"].upper() == id.upper():
            agency_url = agency["url"]
    if category:
        story_cat = category
    else:
        story_cat = '*'
    if region:
        story_region = region
    else:
        story_region = '*'
    if date:
        story_date = date
    else:
        story_date = '*'

    if category is None:
        story_cat = '*'
    if region is None:
        story_region = '*'
    if date is None:
        story_date = '*'

    params = {
    'story_cat': story_cat,
    'story_region' : story_region,
    'story_date' : story_date
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    if agency_url is not None:
        r = requests.get(f"{agency_url}/api/stories", params=params, headers=headers)
        try:
            stories = json.loads(r.text)
            all_stories.append(stories)
        except json.decoder.JSONDecodeError:
            pass
    return all_stories

def Delete(token, key):
    headers = {
        'Authorization': f'Token {token}'
    }
    url = f"http://fy19ahh.pythonanywhere.com/api/stories/{key}"
    r = requests.delete(url, headers=headers)
    if r.status_code != 200:
        print ("Please check you are logged in and input a valid key")
    else:
        print (f"Story {key} Successfully Deleted")

def main():
    tokenValue = None
    key = 0
    while True:
        command = input('>>> ').strip().lower()
        # Log In
        if command.startswith("login"):
            arguments = command.split()
            if len(arguments) == 2:
                url = arguments[1]
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                try:
                    tokenValue = (LogIn(url, username, password)).json().get('token')
                    print ("\nSuccessful Login.\n")
                except:
                    print ("\nError: Invalid Credentials.\n")
            else:
                print("\nInvalid command format. Please enter login <url>.\n")
        # Log Out
        elif command == "logout":
            if tokenValue is not None:
                LogOut(tokenValue)
                print ("\nLogout successful.\n")
                tokenValue = None
            else:
                print ("\nError: No user logged in.\n")
                LogOut(None)
        # Post Story
        elif command == "post":
            if tokenValue is not None:
                headline = input("Headline: ").strip()
                category = input("Category [pol, art, tech, trivia]: ").strip()
                region = input("Region [uk, eu, w]: ").strip()
                details = input("Details: ").strip()
                newPost = (Post(token=tokenValue,
                    headline=headline,
                    category=category,
                    region=region,
                    details=details))
                if newPost.status_code != 201:
                    print ("\nFailed to post story.\n")
                else:
                    print ("\nStory Posted successfully.\n")
            else:
                print ("\nError: Please log in to post.\n")
                Post(token=None,
                    headline="",
                    category="",
                    region="",
                    details="")
        # List stories
        elif command.startswith("news"):
            #os.system('clear')
            command_args = command.split()[1:]
            agency_id = None
            category = None
            region = None
            date = None

            for arg in command_args:
                if arg.startswith("[-id="):
                    agency_id = arg.split("=")[1].rstrip("]").strip('"')
                elif arg.startswith("[-cat="):
                    category = arg.split("=")[1].rstrip("]").strip('"')
                elif arg.startswith("[-reg="):
                    region = arg.split("=")[1].rstrip("]").strip('"')
                elif arg.startswith("[-date="):
                    date = arg.split("=")[1].rstrip("]").strip('"')
            # Single Agency
            if (agency_id) is not None:
                if News(id=agency_id, category=category, region=region, date=date):
                    print ("\n******************************")
                    print (f"Gathering stories from: {agency_id}")
                    print ("******************************\n")
                    for story in News(id=agency_id, category=category, region=region, date=date):
                        if isinstance(story, dict) and 'stories' in story:
                            try:
                                for single_story in story['stories']:  # Iterate over the list of stories
                                    print("--------------------------------")
                                    print(f"Agency ID: {agency_id}")
                                    print(f"Key: {single_story['key']}")
                                    print(f"Headline: {single_story['headline']}")
                                    print(f"Category: {single_story['story_cat']}")
                                    print(f"Region: {single_story['story_region']}")
                                    print(f"Author: {single_story['author']}")
                                    print(f"Date: {single_story['story_date']}")
                                    print(f"Details: {single_story['story_details']}")
                            except KeyError:
                                pass
                        else:
                            pass
                else:
                    print ("\nNo Stories Found.\n")

            # All Agencies
            else:
                to_go_through = []
                for agency in List():
                        to_go_through.append(agency["agency_code"])
                for agency_code in to_go_through:
                    if News(id=agency_code, category=category, region=region, date=date):
                        print ("\n******************************")
                        print (f"Gathering stories from: {agency_code}")
                        print ("******************************\n")
                        for story in News(id=agency_code, category=category, region=region, date=date):
                            if isinstance(story, dict) and 'stories' in story:
                                try:
                                    for single_story in story['stories']:  # Iterate over the list of stories
                                        print("--------------------------------")
                                        print(f"Agency ID: {agency_code}")
                                        print(f"Key: {single_story['key']}")
                                        print(f"Headline: {single_story['headline']}")
                                        print(f"Category: {single_story['story_cat']}")
                                        print(f"Region: {single_story['story_region']}")
                                        print(f"Author: {single_story['author']}")
                                        print(f"Date: {single_story['story_date']}")
                                        print(f"Details: {single_story['story_details']}")
                                except KeyError:
                                    pass
                            else:
                                print ("Failed to gather stories.")

        elif command == "list":
            for agency in List():
                print ("\n----------------------------------------")
                print ("Name: " + agency["agency_name"])
                print ("Code: " + agency["agency_code"])
                print ("URL: " + agency["url"] + "\n")
            pass

        # Delete story
        elif command.startswith("delete"):
            if tokenValue is not None:
                arguments = command.split()
                if len(arguments) == 2:
                    key = arguments[1]
                    Delete(token=tokenValue, key=key)
                else:
                    print("\nInvalid command format. Please enter in the format 'delete <key>'.\n")
            else:
                print("\nPlease log in to delete a story.\n")
        # Exit
        elif command == "exit":
            print("\nExiting the client.\n")
            break
        else:
            print("\nInvalid command.\n")

if __name__ == "__main__":
    main()