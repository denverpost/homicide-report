# Homicide Report
![Homicide Report Tests](https://api.travis-ci.org/denverpost/homicide-report.png)
The Homicide Report code takes a google spreadsheet and filters it into various CSVs, JSONs and JSONPs, which are then FTP'd to a production server. It also has rudimentary publishing tools for a homicide list and homicide map.

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

# License
Copyright © 2015 The Denver Post

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
