# bk-sync
Queries internal jira server (server name removed) for all active issues marked with a `cf` label

A single field containing pertinent information is then pulled from each issue, the data is cleaned and formatted using regex, into an output that is used as a command into an internal slackbot. 

User input then utilizes the same Jira API to update the ticket field to reflect a new value, which is needed for another internal workflow to function
