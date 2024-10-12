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

def fetch_domains():
    """Fetch available domains from the API."""
    response = rs.get("https://api.internal.temp-mail.io/api/v3/domains")
    if response.status_code == 200:
        return [domain['name'] for domain in response.json()["domains"]]
    else:
        print("Error fetching domains.")
        return []

def create_custom_email(email_name):
    """Create a custom email with the selected domain."""
    domain_list = fetch_domains()
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
    response = rs.post("https://api.internal.temp-mail.io/api/v3/email/new", json={"name": email_name, "domain": selected_domain})

    if response.status_code == 200:
        print(f"Successfully created email: {email}")
        save_email_info(email)
        inbox_check(email)
    else:
        print("Error: Failed to create email. Try again.")

def save_email_info(email):
    """Save the created email to a file."""
    with open("domain.txt", "w") as file:
        file.write(email)

def inbox_check(email):
    """Check the inbox for new messages."""
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
    """Display the details of a message."""
    print(f"\nNew Message:")
    print(f"From: {msg['from']}")
    print(f"Subject: {msg['subject']}")
    print(f"Message:\n{msg['body_text']}")

def generate_random_email():
    """Generate a random email address."""
    length = random.randint(10, 15)
    response = rs.post("https://api.internal.temp-mail.io/api/v3/email/new", json={"min_name_length": length, "max_name_length": length})
    
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
    display_info()
    display_divider()
    
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
