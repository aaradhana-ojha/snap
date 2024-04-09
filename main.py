import json
import os

# Constants for file paths
USERS_FILE = 'users.json'
MESSAGES_FILE = 'messages.json'

# Ensure data files exist
def ensure_files():
    for file_path in [USERS_FILE, MESSAGES_FILE]:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump({}, f)

# Function to load data from a file
def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to save data to a file
def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Create an account
def create_account():
    users = load_data(USERS_FILE)
    username = input("Enter username: ")
    if username in users:
        print("Username already exists.")
        return
    password = input("Enter password: ")
    users[username] = {'password': password, 'messages': {}, 'blocked_users': []}
    save_data(USERS_FILE, users)
    print("Account creation successful!")

# Login
def login():
    users = load_data(USERS_FILE)
    username = input("Username: ")
    password = input("Password: ")
    if username in users and users[username]['password'] == password:
        print("Login successful.")
        return username
    else:
        print("Invalid username / password.")
        return None

# Send message with a limit of 15 messages per conversation
def send_message(sender):
    receiver = input("Enter the username of the person you want to message: ")
    message = input("Enter your message: ")
    messages = load_data(MESSAGES_FILE)
    
    # Ensure the sender has a messages entry
    if sender not in messages:
        messages[sender] = {}
    
    # Ensure the conversation exists and limit the messages to 15
    if receiver not in messages[sender]:
        messages[sender][receiver] = []
    messages[sender][receiver].append({'message': message, 'read': False})
    messages[sender][receiver] = messages[sender][receiver][-15:]
    
    save_data(MESSAGES_FILE, messages)
    print("Message sent.")

# View messages
def view_messages(username):
    messages = load_data(MESSAGES_FILE)
    for sender in messages:
        for receiver in messages[sender]:
            if receiver == username or sender == username:
                print(f"From {sender} to {receiver}: ")
                for msg in messages[sender][receiver]:
                    status = "Read" if msg['read'] else "Unread"
                    print(f"({status}) {msg['message']}")

# Delete message from a specific conversation
def delete_message(username):
    messages = load_data(MESSAGES_FILE)
    print("\nYour conversations:")
    for sender in messages:
        for receiver in messages[sender]:
            if receiver == username or sender == username:
                print(f"From {sender} to {receiver}")
    
    sender = input("\nEnter the sender username: ")
    receiver = input("Enter the receiver username: ")
    if sender in messages and receiver in messages[sender]:
        print("\nMessages in this conversation:")
        for i, msg in enumerate(messages[sender][receiver], 1):
            print(f"{i}. {msg['message']}")

        try:
            msg_index = int(input("\nEnter the message index to delete: ")) - 1
            if 0 <= msg_index < len(messages[sender][receiver]):
                del messages[sender][receiver][msg_index]
                save_data(MESSAGES_FILE, messages)
                print("Message deleted.")
            else:
                print("Invalid message index.")
        except ValueError:
            print("Invalid input.")
    else:
        print("Conversation not found.")

# Block or Unblock a user
def block_user(username):
    users = load_data(USERS_FILE)
    print("\nAvailable users to block/unblock:")
    for user in users:
        if user != username:
            print(user)
    
    block_choice = input("\nEnter the username to block/unblock: ")
    if block_choice in users:
        if block_choice in users[username]['blocked_users']:
            users[username]['blocked_users'].remove(block_choice)
            print(f"{block_choice} unblocked.")
        else:
            users[username]['blocked_users'].append(block_choice)
            print(f"{block_choice} blocked.")
        save_data(USERS_FILE, users)
    else:
        print("User not found.")

# Main function
def main():
    ensure_files()
    while True:
        print("\n1. Create Account\n2. Login\n3. Send Message\n4. View Messages\n5. Delete Message\n6. Block/Unblock User\n7. View Unread Messages\n8. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            create_account()
        elif choice == "2":
            user = login()
            if user:
                while True:
                    print("\n1. Send Message\n2. View Messages\n3. Delete Message\n4. Block/Unblock User\n5. View Unread Messages\n6. Logout")
                    user_choice = input("Choose an option: ")
                    if user_choice == "1":
                        send_message(user)
                    elif user_choice == "2":
                        view_messages(user)
                    elif user_choice == "3":
                        delete_message(user)
                    elif user_choice == "4":
                        block_user(user)
                    elif user_choice == "5":
                        view_unread_messages(user)
                    elif user_choice == "6":
                        break
                    else:
                        print("Invalid choice.")
        elif choice == "3":
            print("Please login to send a message.")
        elif choice == "4":
            print("Please login to view messages.")
        elif choice == "5":
            print("Please login to delete a message.")
        elif choice == "6":
            print("Please login to block/unblock a user.")
        elif choice == "7":
            view_unread_messages(None)
        elif choice == "8":
            break
        else:
            print("Invalid choice.")

# Function to view unread messages
def view_unread_messages(username):
    messages = load_data(MESSAGES_FILE)
    unread_count = 0
    for sender in messages:
        for receiver in messages[sender]:
            if receiver == username and not messages[sender][receiver][-1]['read']:
                unread_count += 1
    if username:
        print(f"You have {unread_count} unread messages.")
    else:
        print(f"There are {unread_count} unread messages in the system.")

if __name__ == "__main__":
    main()
