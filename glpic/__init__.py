from ast import literal_eval
from dateutil.parser import parse
from datetime import date, timedelta
import json
import ssl
import os
import sys
from urllib.request import urlopen, Request
from urllib.parse import urlencode


def handle_parameters(parameters):
    overrides = {}
    processed_keys = []
    if parameters is None:
        return {}
    for parameter in parameters:
        if len(parameter.split('=')) < 2:
            error(f"Wrong parameter {parameter}. Should be key=value")
            sys.exit(1)
        else:
            if len(parameter.split('=')) == 2:
                key, value = parameter.split('=')
            else:
                split = parameter.split('=')
                key = split[0]
                value = parameter.replace(f"{key}=", '')
            if key in processed_keys:
                error(f"Repeated parameter {key}")
                sys.exit(1)
            else:
                processed_keys.append(key)
            if value.isdigit():
                value = int(value)
            elif value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value == 'None':
                value = None
            elif value == '[]':
                value = []
            elif value.startswith('[') and value.endswith(']'):
                if '{' in value:
                    value = literal_eval(value)
                else:
                    value = value[1:-1].split(',')
                    for index, v in enumerate(value):
                        v = v.strip()
                        value[index] = v
            overrides[key] = value
    return overrides


def _delete(url, headers):
    request = Request(url, headers=headers, method='DELETE')
    try:
        return urlopen(request)
    except Exception as e:
        error(e.read().decode())


def _get(url, headers):
    if not os.path.basename(url).split('?')[0].isnumeric():
        encoded_params = urlencode({"range": '0-9999'})
        delimiter = '&' if '?' in url else '?'
        url += f'{delimiter}{encoded_params}'
    try:
        return json.loads(urlopen(Request(url, headers=headers)).read())
    except Exception as e:
        error(e.read().decode())


def _patch(url, headers, data):
    data = json.dumps(data).encode('utf-8')
    try:
        return urlopen(Request(url, data=data, headers=headers, method='PATCH'))
    except Exception as e:
        error(e.read().decode())


def _post(url, headers, data):
    data = json.dumps(data).encode('utf-8')
    try:
        return urlopen(Request(url, data=data, headers=headers, method='POST'))
    except Exception as e:
        error(e.read().decode())


def _put(url, headers, data):
    data = json.dumps(data).encode('utf-8')
    try:
        return urlopen(Request(url, data=data, headers=headers, method='PUT'))
    except Exception as e:
        error(e.read().decode())


def error(text):
    color = "31"
    print(f'\033[0;{color}m{text}\033[0;0m')


def warning(text):
    color = "33"
    print(f'\033[0;{color}m{text}\033[0;0m')


def info(text):
    color = "36"
    print(f'\033[0;{color}m{text}\033[0;0m')


def curl_base(headers):
    return f"curl -H 'Content-Type: application/json' -H \"Session-Token: {headers['Session-Token']}\""


class Glpic(object):
    def __init__(self, base_url, user, api_token, debug=False):
        self.debug = debug
        self.base_url = base_url
        self.user = user
        ssl._create_default_https_context = ssl._create_unverified_context
        headers = {'Content-Type': 'application/json', 'Authorization': f"user_token {api_token}"}
        response = _get(f'{base_url}/initSession?get_full_session=true', headers)
        self.headers = {'Content-Type': 'application/json', "Session-Token": response['session_token']}

    def get_user(self, user=None):
        if user is None:
            user = self.user
        users = _get(f'{self.base_url}/User', headers=self.headers)
        for u in users:
            if user in u['name']:
                return u

    def info_computer(self, computer, full=False):
        computers = _get(f'{self.base_url}/Computer?with_devices', headers=self.headers)
        if not str(computer).isnumeric():
            computers = [c for c in _get(f'{self.base_url}/Computer?with_devices',
                                         headers=self.headers) if c['name'].strip() == computer]
            if computers:
                result = computers[0]
            else:
                error(f"Computer {computer} not found")
                return {}
        else:
            result = _get(f'{self.base_url}/Computer/{computer}?with_devices', headers=self.headers)
        if full:
            return result
        info = {'id': result['id'], 'name': result['name'], 'serial': result['serial']}
        if result['comment'] not in ['', 'None']:
            info['comment'] = result['comment']
        for link in result['links']:
            if link['rel'] == 'ComputerModel':
                info['model'] = _get(link['href'], headers=self.headers)['name']
            if link['rel'] == 'Manufacturer':
                info['manufacturer'] = _get(link['href'], headers=self.headers)['name']
            if link['rel'] == 'Item_DeviceProcessor':
                processor = _get(link['href'], headers=self.headers)[0]
                info['processor'] = f"{processor['nbcores']} cores and {processor['nbthreads']} threads"
            if link['rel'] == 'Item_DeviceMemory':
                memory = 0
                memory_data = _get(link['href'], headers=self.headers)
                if memory_data and 'links' in memory_data[0]:
                    memory_links = memory_data[0]['links']
                    for memory_link in memory_links:
                        if memory_link['rel'] == 'DeviceMemory':
                            new_memory = _get(memory_link['href'], headers=self.headers)
                            memory += new_memory['size_default']
                if memory > 0:
                    info['memory'] = memory
            if link['rel'] == 'ReservationItem':
                # reservation = _get(link['href'], headers=self.headers)[0]
                info['reserved'] = True
        return info

    def info_reservation(self, reservation):
        return _get(f'{self.base_url}/ReservationItem/{reservation}', headers=self.headers)

    def list_reservations(self, overrides={}):
        user = overrides.get('user') or self.user
        response = _get(f'{self.base_url}/Reservation', headers=self.headers)
        user_id = self.get_user(user)['id']
        return [r for r in response if r['users_id'] == user_id]

    def list_computers(self, user=None, overrides={}):
        computers = _get(f'{self.base_url}/Computer?with_devices', headers=self.headers)
        if not overrides:
            return computers
        results = []
        memory = overrides.get('memory')
        numcpus = overrides.get('numcpus')
        number = overrides.get('number', 3)
        for computer in computers:
            for link in computer['links']:
                if numcpus is not None and link['rel'] == 'Item_DeviceProcessor':
                    processor = _get(link['href'], headers=self.headers)[0]
                    current_numcpus = processor['nbcores']
                if memory is not None and link['rel'] == 'Item_DeviceMemory':
                    current_memory = 0
                    memory_data = _get(link['href'], headers=self.headers)
                    if memory_data and 'links' in memory_data[0]:
                        memory_links = memory_data[0]['links']
                        for memory_link in memory_links:
                            if memory_link['rel'] == 'DeviceMemory':
                                new_memory = _get(memory_link['href'], headers=self.headers)
                                current_memory += new_memory['size_default']
            if numcpus is not None and current_numcpus < int(numcpus):
                continue
            if memory is not None and current_memory < int(memory):
                continue
            results.append(computer)
            if len(results) >= number:
                break
        return results

    def create_reservation(self, reservation, overrides):
        valid_keys = list(_get(f'{self.base_url}/Reservation/', self.headers)[0].keys())
        wrong_keys = [key for key in overrides if key not in valid_keys]
        if wrong_keys:
            error(f"Ignoring keys {','.join(wrong_keys)}")
            for key in wrong_keys:
                del overrides[key]
        # post = {"reservationitems_id": reservation_id, "begin": begin, "end": end, "users_id": user_id,
        #        "comment": f'reservation for {self.user}'}
        if not overrides:
            info("Nothing to create")
            return
        if 'end' not in overrides:
            overrides['end'] = date.today() + timedelta(days=30)
        overrides['end'] = parse(str(overrides['end'])).strftime('%Y-%m-%d 00:00:00')
        data = {'input': overrides}
        if self.debug:
            base_curl = curl_base(self.headers)
            msg = f"{base_curl} -X POST -Lk {self.base_url}/Reservation/{reservation} -d \"{json.dumps(data)}\""
            print(msg)
        return _post(f'{self.base_url}/Reservation/{reservation}', self.headers, data)

    def delete_reservation(self, reservation):
        if self.debug:
            base_curl = curl_base(self.headers)
            print(f"{base_curl} -X DELETE -Lk {self.base_url}/Reservation/{reservation}")
        return _delete(f'{self.base_url}/Reservation/{reservation}', headers=self.headers)

    def update_reservation(self, reservation, overrides):
        valid_keys = list(_get(f'{self.base_url}/Reservation/', self.headers)[0].keys()) + ['user']
        wrong_keys = [key for key in overrides if key not in valid_keys]
        if wrong_keys:
            error(f"Ignoring keys {','.join(wrong_keys)}")
            for key in wrong_keys:
                del overrides[key]
        if not overrides:
            info("Nothing to update")
            return
        if 'end' in overrides:
            overrides['end'] = parse(str(overrides['end'])).strftime('%Y-%m-%d 00:00:00')
        new_user = overrides.get('user') or overrides.get('users_id')
        if new_user is not None and not str(new_user).isnumeric():
            overrides['users_id'] = self.get_user(new_user)['id']
        if 'user' in overrides:
            del overrides['user']
        data = {'input': overrides}
        if self.debug:
            base_curl = curl_base(self.headers)
            msg = f"{base_curl} -X PUT -Lk {self.base_url}/Reservation/{reservation} -d \"{json.dumps(data)}\""
            print(msg)
        result = _put(f'{self.base_url}/Reservation/{reservation}', self.headers, data)
        return result
