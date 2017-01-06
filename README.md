# Homicide Report
![Homicide Report Tests](https://api.travis-ci.org/denverpost/homicide-report.png)

The Homicide Report code takes a google spreadsheet and filters it into various CSVs, JSONs and JSONPs, which are then FTP'd to a production server. It also has basic tools for a putting a homicide list and homicide map online.

# Project Setup
The back-end, spreadsheet-publishing portion assumes these environment variables:
```
# The spreadsheet user account
export ACCOUNT_USER='user@gmail.com'
# The spreadsheet user's account key
export ACCOUNT_KEY=''
# The production FTP server's user, directory the files will be uploaded to, and hostname.
export FTP_USER=''
export REMOTE_DIR=''
export REMOTE_HOST=''
```

# How-To's

## How to get the Homicide Report ready for a new year

The Homicide Report is tied to reporting homicides for a particular city in a particular year. Come January, the hard-coded years need to be updated. Every hard-coded year that needs changing is marked nearby (usually on the line above) with a `NEWYEAR` label. That means running `git grep NEWYEAR` will show a list of files that need editing.

Here's how it works.

1. Run `git grep NEWYEAR` on the command line.
2. Edit the files listed, changing the years in them to the current year. Many files will require more than one edit.
3. Upload the files to production ( `/DenverPost/app/homicide-report` ).
4. Commit and push your changes.
5. Pull the changes from production, run the new deploy script.
6. Update the iframe URLs that reference the previous year on http://www.denverpost.com/denver-homicides/ 



# License
Copyright © 2015-2017 The Denver Post

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
