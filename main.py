# Welcome to bk_sync_map, this script pulls all tickets that need taxonomy created. It creates the proper bot query
# to sync all audiences, and then updates the mapping in the ticket to reflect the sync

# Start by marking all fulfillment tickets that you would like to sync with a cf label (label will be removed later)
# Once all tickets are marked, you can run the script. Plug the query into Fulbot and then progress the script with a
# 'y' to complete the mapping update

#Testing git setup

from jira.client import JIRA  # --> installed with `pip install jira` in the terminal
import re  # Regex component
import webbrowser
import sys

chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
count = 0
count1 = 0
update_count = 0

# Logon credentials to hit API
options = {'server': 'server_address.com'}
jira = JIRA(options, basic_auth=('username', 'pass'))

#JQL to pull "parent" target issues 

issues_in_proj = jira.search_issues('project = ABC AND issuetype in ("Ticket Type") '
                                    'AND status = Open AND cf[12345] ~ Platform AND "Fulfill Channel ID" ~ 123 AND '
                                    'labels = "cf"')

#Sub-query to pull "child" target issue, which is where the needed data is stored

for issue in issues_in_proj:
    strategy = jira.search_issues('issue in linkedIssues(' + str(issue) + ', "Strategy") AND status in (Audience, '
                                                                          '"Scorecard Approval", "Post Processing")')

branded = 'Branded'

no_sync = []
issues_in_proj_sync = []
listed = []

overall_mapping_maids = []
overall_mapping_no_maids = []

#This loop filters tickets based on a boolean field in Jira. Determines if data needs to be synced to additional component.
#Data is then cleaned using regex and .join, then formats the data using .replace.

for issue in issues_in_proj:
    summary = str(issue.raw['fields']['summary'])
    if branded.lower() in summary.lower():
        no_sync.append(issue)
        count1 += 1
    elif issue.fields.customfield_17027 == 'true':
        issues_in_proj_sync.append(str(issue))
        mapping = "".join(re.sub(r'\((\d+)*\)', "", issue.fields.customfield_123456)).replace("", "")
        overall_mapping_maids.append(mapping)
        listed.append(issue.fields.customfield_10911)
        count += 1
    elif issue.fields.customfield_17027 == 'false':
        issues_in_proj_sync.append(str(issue))
        mapping = "".join(re.sub(r'\((\d+)*\)', "", issue.fields.customfield_123456)).replace("", "")
        overall_mapping_no_maids.append(mapping)
        listed.append(issue.fields.customfield_10911)
        count += 1

print('Data for DLX PRIVATE tickets')

#Produces formatted data that is designed to be input into fulbot, an internal slackbot that helps sync data to new components.

print('\nFulbot command to sync to 314')
print('sync p ' + (','.join(overall_mapping_maids)) + ' to c 447')

print('\nFulbot command to sync to 585 only (Should be auto-synced)')
print('sync p ' + (','.join(overall_mapping_no_maids)) + ' to c 731')

#Basic metrics that are used to ensure that we are capturing all the data needed

counter = ((','.join(listed)).count(','))+1
print('\nNumber of audiences to be synced: ' + str(counter))
print('Number of tickets needing taxonomy: ' + str(count))

#Interacts with chrome to open tabs. Depending on daily volume this can be > 20 tabs

print('\nJira links (Should open automatically)')
for issue in issues_in_proj_sync:
    jira_link = 'https://jira.server.com/browse/' + issue
    print(jira_link)
    webbrowser.get('chrome').open_new_tab(jira_link)

print('\nTickets Not Opened')

for issue in no_sync:
    print((issue.raw['fields']['summary'][31:]) + '- ' + 'https://jira.server.com/browse/' + str(issue))

print('\nTotal tickets in queue: ' + str(count + count1))

# Added in code from CPG_Plus_Mapping, it seemed unnecessary to have them operating as independent scripts
print('\n')

proceed = str(input('Would you like to update mappings in Jira (Y/N): '))

if proceed.lower() == 'y':
    print('Now updating mapping in Jira\n')
elif proceed.lower() == 'n':
    print('\nExiting program, no mapping has been updated\n')
    sys.exit(0)

original_mapping_585 = []
new_mapping_maids = []

#Hits Jira API to add new mappings

for issue in issues_in_proj:
    if issue.fields.customfield_34567 == 'true':
        strategy = jira.search_issues('issue in linkedIssues(' + str(issue) + ', "Strategy") AND status in (Audience, '
                                                                              '"Scorecard Approval", '
                                                                              '"Post Processing"))
        original_mapping_585.append(issue.fields.customfield_11111)
        print('\nStrategy Ticket: https://jira.server.com/browse/' + str(strategy)[19:-17])
        print('Original Mapping: ' + str(','.join(original_mapping_585)))
        maids_mapping = (re.sub(r'\((\d+)*\)', "(314)", issue.fields.customfield_11111))
        print('Updated Mapping: ' + str(','.join(original_mapping_585)) + ',' + str(maids_mapping))
        for issue in strategy:
            issue.update(fields={'customfield_11111': (str(','.join(original_mapping_585)) + ',' + str(maids_mapping))})

        original_mapping_585.clear()
        update_count += 1

print('\n' + str(update_count) + ' tickets updated')
