# Restore Deleted Messages in Telegram Group

It is surprisingly easy to batch delete messages in a Telegram group, either to delete the entire chat history or to delete messages from a specific user. 
Unfortunately telegram doesn't have an user interface or an API to restore deleted messages in groups, but however provides a possibility to view deleted message as group admin within 48 hours after deletion. 
Here are python scripts to dump and resend deleted messages in a Telegram group. 

It is majorly based on https://gist.github.com/avivace/4eb547067e364d416c074b68502e0136 and its comments.
I did not find a license in the original gist, so if the author wants to add a license, please let me know.

## Features

- Fetch and resend deleted messages in a Telegram group.
- Supported message type:
  - text
  - media
  - file (documents, uncompressed media, etc)


## Usage

1. Clone the repository:
```bash
git clone https://github.com/simonmysun/restore-deleted-messages-in-telegram-group.git
```
2. Navigate to the project directory:
```bash
cd restore-deleted-messages-in-telegram-group
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Set up your Telegram API credentials and group chat ID you want to restore messages in:
```
cat > .env <<EOF
GROUP_CHAT_ID=
API_ID=
API_HASH=
EOF
```
  - Get credentials from https://my.telegram.org, under API Development.
  - Get the group chat ID by copy message link and extract the chat ID from the link, or from web client, from the URL.
5. Run the script to start fetching messages:
```bash
python dump.py
```
6. To restore deleted messages, run:
```bash
python send.py
```

It is recommend to read the source code before running the scripts to make necessary customizations.
