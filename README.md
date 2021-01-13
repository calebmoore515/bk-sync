# bk-sync
Queries internal jira server (server name removed) for all active issues marked with a `cf` label

A single field containing pertinent information is then pulled from each issue, the data is cleaned and formatted using regex, into an output that is used as a command into an internal slackbot. It also opens all issues in a chrome browser so that necessary data can be pulled from each ticket and placed into a spreadsheet.

User input then utilizes the same Jira API to update the ticket field to reflect a new value, which is needed for another internal workflow to function.

Time Savings: Process orginally took ~30min to complete and now takes <1 min. Over the course of the week ~2.5hrs saved

