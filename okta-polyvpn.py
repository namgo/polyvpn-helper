import requests
import argparse
import logging
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0'

r = requests.Session()
r.headers['User-Agent'] = user_agent

def get_saml_url(username, password, appid='exkb6cxaui2AIoZ9y697'):
    resp = r.post('https://identification.polymtl.ca/api/v1/authn', json={'username': username, 'password': password})
    session_token = resp.json()['sessionToken']
    resp = r.post('https://identification.polymtl.ca/api/v1/sessions?additionalFields=cookieToken', json={'sessionToken': session_token})
    cookietoken = resp.json()['cookieToken']
    url = f'https://identification.polymtl.ca/app/cisco_asa_vpn_saml/{appid}/sso/saml?onetimetoken={cookietoken}'
    return url

def get_webvpn_cookie(saml_url, group_name='SSLProfileQuartz'):
    resp = r.get(saml_url)
    html = BeautifulSoup(resp.text, features='html.parser')
    saml = html.find('input', attrs={'name': 'SAMLResponse'})['value']
    resp = r.post(f'https://ssl.vpn.polymtl.ca/+CSCOE+/saml/sp/acs?tgname={group_name}', data={'SAMLResponse': saml, 'RelayState': ''}, cookies={'webvpnlogin': '1', 'webvpnLang': 'en', 'CSRFtoken': ''})

    html = BeautifulSoup(resp.text, features='html.parser')
    saml = html.find('input', attrs={'name': 'SAMLResponse'})['value']
    csrf = html.find('input', attrs={'name': 'csrf_token'})['value']
    group_list = html.find('input', attrs={'name': 'group_list'})['value']
    #r.headers.update({'Referer': 'https://ssl.vpn.polymtl.ca/+CSCOE+/saml/sp/acs?tgname=SSLProfileQuartz'})
    resp = r.post('https://ssl.vpn.polymtl.ca/+webvpn+/index.html',
                  data={'SAMLResponse': saml,
                        'group_list': group_list, 
                        'tgroup': '', 'next': '', 'tgcookieset': '',
                        'csrf_token': csrf,
                        'username': '',
                        'password': '',
                        'ctx': '', 'Login': 'Login'}, cookies={'webvpnlogin': '1', 'webvpnLang': 'en', 'CSRFtoken': csrf})
    return resp.cookies['webvpn']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='okta_polyvpn', description='Automate getting webvpn cookie from polymtl okta for use with openconnect',
                            epilog='pipe to: openconnect --protocol=anyconnect --authgroup=PolyQuartz --cookie-on-stdin https://ssl.vpn.polymtl.ca/')
    parser.add_argument('-u', '--username', help='full username (first.last@polymtl.ca)', required=True)
    parser.add_argument('-p', '--password', help='the VPN password you normally use to log in to ssl.vpn.polymtl.ca', required=False)
    parser.add_argument('-P', '--password-on-stdin', help='optionally take password via stdin instead of as argument', action='store_true')
    parser.add_argument('-a', '--internal-appid', help='internal okta appid for CSCOE', required=False, default='exkb6cxaui2AIoZ9y697')
    parser.add_argument('-n', '--internal-groupname', help='internal okta group name for CSCOE', required=False, default='SSLProfileQuartz')
    args = parser.parse_args()
    if args.password_on_stdin:
        password = input()
    else:
        password = args.password


    saml_url = get_saml_url(args.username, password, args.internal_appid)
    cookie = get_webvpn_cookie(saml_url, args.internal_groupname)
    print(cookie)
