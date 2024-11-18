# okta+polyvpn helper for openconnect

Automate getting webvpn cookie from polymtl okta for use with openconnect 

## Usage

This program assumes you are in the PolyQuartz vpn group - if you still need to auth via okta and are not in PolyQuartz please submit an issue and I can try to extend this program.

Ideally your password should be sent to the program's standard input with:

`python3 okta-polyvpn.py -u user.name@polymtl.ca -P`

If your username+password is recognized and all is well, you should receive a webvpn cookie.

This can be passed to the standard input of `openconnect --protocol=anyconnect --authgroup=PolyQuartz --cookie-on-stdin https://ssl.vpn.polymtl.ca/`

Or better yet, pipe it to openconnect directly:

`python3 okta-polyvpn.py -u user.name@polymtl.ca -P | openconnect --protocol=anyconnect --authgroup=PolyQuartz --cookie-on-stdin https://ssl.vpn.polymtl.ca/`


## Developer switches

`--internal-appid` and `--internal_groupname` exist in case upstream appid or auth group changes in the future.
