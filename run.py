import requests
import json
import random

# Initialize session
rs = requests.Session()

# To store the created emails
created_emails = []

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
    print("▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ")

def display_info():
    print("🌐 Welcome to NULL-MAIL!")
    print("👤 Created by: HACKINTER")
    print("🔖 Version: 1.0")
    print("🐦 Twitter: _anonix_z")
    print("© 2024 HACKINTER. All rights reserved.\n")

def create_custom_email(email_name):
    # Fetch available domains
    domains = json.loads(rs.get("https://api.internal.temp-mail.io/api/v3/domains").text)["domains"]
    domain_list = [domain['name'] for domain in domains]

    # Display available domains and get user selection
    print("🌐 Available domains:")  # Updated emoji here
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
                print("❌ Invalid selection, using a random domain instead.")
                selected_domain = random.choice(domain_list)
        except ValueError:
            print("❌ Invalid input, using a random domain instead.")
            selected_domain = random.choice(domain_list)

    email = f"{email_name}@{selected_domain}"
    response = rs.post(
        "https://api.internal.temp-mail.io/api/v3/email/new",
        json={"name": email_name, "domain": selected_domain}
    )

    if response.status_code == 200:
        print(f"✅ Successfully created email: {email}")
        created_emails.append(email)  # Store the created email
        save_email_info(email)
        check_inbox(email)
    else:
        print("❌ Error: Failed to create email. Try again.")

def save_email_info(email):
    with open("domain.txt", "w") as file:
        file.write(email)

def check_inbox(email):
    """Check the inbox for new messages."""
    inbox_url = f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages"
    response = rs.get(inbox_url)
    
    if response.status_code == 200:
        messages = response.json()
        if messages:
            print(f"\n📥 You have {len(messages)} new message(s) in your inbox:\n")
            for msg in messages:
                display_message(msg)
        else:
            print("📭 No new messages in the inbox.")
    else:
        print("❌ Error checking inbox. Please try again later.")

def display_message(msg):
    print(f"🆕 New Message:")
    print(f"📧 From: {msg['from']}")
    print(f"📝 Subject: {msg['subject']}")
    print(f"📜 Message:\n{msg['body_text']}")

def generate_random_email():
    length = random.randint(10, 15)
    response = rs.post(
        "https://api.internal.temp-mail.io/api/v3/email/new",
        json={"min_name_length": length, "max_name_length": length}
    )
    if response.status_code == 200:
        data = response.json()
        email = data["email"]
        print(f"🎉 Random email created: {email}")
        created_emails.append(email)  # Store the created email
        save_email_info(email)
        check_inbox(email)
    else:
        print("❌ Error: Failed to create random email.")

def display_total_emails_created():
    """Display all created emails."""
    if created_emails:
        print("\n📊 Total emails created:")
        for email in created_emails:
            print(email)
    else:
        print("📭 No emails have been created yet.")

def main():
    display_logo()
    display_info()  # Display additional information
    display_divider()  # Display the divider after the info

    while True:
        choice = input(
            "[C] Create a custom email\n"
            "[R] Generate a random email\n"
            "[I] Check inbox\n"
            "[T] Display total emails created\n"
            "[exit] Type to quit\n"
            "Type what you want to do: "
        ).strip().lower()

        if choice == 'c':
            email_name = input("🖊️ Enter your custom email name: ")
            create_custom_email(email_name)
        elif choice == 'r':
            generate_random_email()
        elif choice == 'i':
            email = input("📧 Enter your email address to check the inbox: ")
            check_inbox(email)
        elif choice == 't':
            display_total_emails_created()  # Call the function to display total emails
        elif choice == 'exit':
            print("👋 Exiting the program. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
