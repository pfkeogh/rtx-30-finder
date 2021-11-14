# RTX 30 Finder

Rough stab at scraping for in stock cards.

[GitHub](https://github.com/pfkeogh/rtx-30-finder)

### Usage
##### CLI
```
pip install --index-url https://test.pypi.org/simple/ pip install rtx30finder

rtx30finder
```  
If a card is found to be in stock, its info will be be printed along with the URL.


### Run this from your phone as an IOS Shortcut
enable remote login // SSH

System Preferences -> Sharing -> Enable Remote Login

install via pip on the remote host

use "Run script over SSH"

input:
/usr/local/bin/rtx30finder

