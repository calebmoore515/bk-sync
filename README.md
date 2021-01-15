# bk-sync

#### Description

Queries internal jira server (server name removed) for all active issues marked with a `cf` label. This script is designed to work in tandem with jira-ticket.py, both utilize the same JQL query. This script is run first, followed by jira-ticket.

A single field containing pertinent information is then pulled from each issue, the data is cleaned and formatted using regex, into an output that is used as a command into an internal slackbot. It also opens all issues in a chrome browser so that necessary data can be pulled from each ticket and placed into a spreadsheet.

The script then leverages the same Jira API to update the ticket field to reflect a new value, which is needed for another internal workflow to function.

#### Time Saved

Process orginally took ~30min to complete and now takes <1 min. Over the course of the week ~2.5hrs saved

#### Troubleshooting

1. Be sure you are logged onto proper VPN

2. Jira credintials are up to date (changes every 90 days)

3. Be sure that the mapping field is populated with the proper blank mapping

4. If the fulbot command is failing, check the query for double commas `ex. sync p 1234,4567,,6789 to p 447`. Remove and then resubmit command. This is caused when data type is segment instead of profile. Segments must be manaully synced.

#### Future improvements 
1. It would be helpful to update the code to distinguish and automatically parse out segment data types (which is what causes \#4 above). I have not done this yet since there is no clear marker in the ticket that can be used to filter, and they are somewhat uncommon occurences so I cannot currently justify the developement effort.

2. It's not necessary to improve functionality, but producing a log file of the output would be helpful. This would allow us to save the fulbot command and re-run it if we discover issues later in the workflow. 

