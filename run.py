import requests
import json
import random

# Initialize session
rs = requests.Session()

def display_logo():
    logo = r"""
    _   ____  ____    __         ____  ____ _  __
   / | / / / / / /   / /        / __ )/ __ \ |/ /
  /  |/ / / / / /   / /  ______/ __  / / / /   /
 / /|  / /_/ / /___/ /__/_____/ /_/ / /_/ /   |
/_/ |_/\____/_____/_____/    /_____/\____/_/|_|
    """
    print(logo)

def display_divider():
    print("/___/___/___/___/___/___/___/___/___/___/___/___/")

def display_info():
    print("Welcome to NULL-MAIL!")
    print("Created by: HACKINTER")
    print("Version: 1.0")
    print("Twitter: _anonix_z")
    print("© 2024 HACKINTER. All rights reserved.\n")

def fetch_available_domains():
    try:
        response = rs.get("https://api.internal.temp-mail.io/api/v3/domains")
        response.raise_for_status()  # Raise an error for bad responses
        domains = json.loads(response.text)["domains"]
        return [domain['name'] for domain in domains]
    except requests.RequestException as e:
        print(f"Error fetching domains: {e}")
        return []

def create_custom_email(email_name):
    domain_list = fetch_available_domains()

    if not domain_list:
        print("No domains available, unable to create email.")
        return

    # Display available domains and get user selection
    print("Available domains:")
    for i, domain in enumerate(domain_list, start=1):
        print(f"{i}. {domain}")

    domain_selection = input("Select a domain by number (or enter 'random' for a random domain): ")

    if domain_selection.lower() == 'random':
        selected_domain = random.choice(domain_list)
    else:
        try:
            selected_index = int(domain_selection) - 1
            if 0 <= selected_index < len(domain_list):
                selected_domain = domain_list[selected_index]
            else:
                print("Invalid selection, using a random domain instead.")
                selected_domain = random.choice(domain_list)
        except ValueError:
            print("Invalid input, using a random domain instead.")
            selected_domain = random.choice(domain_list)

    email = f"{email_name}@{selected_domain}"
    response = rs.post(
        "https://api.internal.temp-mail.io/api/v3/email/new",
        json={"name": email_name, "domain": selected_domain}
    )

    if response.status_code == 200:
        print(f"Successfully created email: {email}")
        save_email_info(email)
        inbox_check(email)
    else:
        print("Error: Failed to create email. Try again.")

def save_email_info(email):
    with open("domain.txt", "w") as file:
        file.write(email)

def inbox_check(email):
    inbox_url = f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages"
    response = rs.get(inbox_url)
    if response.status_code == 200:
        messages = response.json()
        if messages:
            for msg in messages:
                display_message(msg)
        else:
            print("No new messages in the inbox.")
    else:
        print("Error checking inbox.")

def display_message(msg):
    print(f"New Message:")
    print(f"From: {msg['from']}")
    print(f"Subject: {msg['subject']}")
    print(f"Message:\n{msg['body_text']}")

def generate_random_email():
    length = random.randint(10, 15)
    response = rs.post(
        "https://api.internal.temp-mail.io/api/v3/email/new",
        json={"min_name_length": length, "max_name_length": length}
    )
    if response.status_code == 200:
        data = response.json()
        email = data["email"]
        print(f"Random email created: {email}")
        save_email_info(email)
        inbox_check(email)
    else:
        print("Error: Failed to create random email.")

def main():
    display_logo()
    display_info()  # Display additional information
    display_divider()  # Display the divider after the info
    choice = input("Do you want to create a custom email (C) or generate a random email (R)? ").strip().lower()

    if choice == 'c':
        email_name = input("Enter your custom email name: ")
        create_custom_email(email_name)
    elif choice == 'r':
        generate_random_email()
    else:
        print("Invalid choice, exiting.")

if __name__ == "__main__":
    main()
