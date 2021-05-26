# Cribbed from https://github.com/theirix/ptpimg-uploader/blob/master/ptpimg_uploader.py

"""
BSD 2-Clause License

Copyright (c) 2017, theirix
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import contextlib
import mimetypes
import os
from io import BytesIO

import requests

mimetypes.init()


class UploadFailed(Exception):
    def __str__(self):
        msg, *args = self.args
        return msg.format(*args)


class PtpimgUploader:
    """ Upload image or image URL to the ptpimg.me image hosting """

    def __init__(self, api_key, timeout=None):
        self.api_key = api_key
        self.timeout = timeout

    @staticmethod
    def _handle_result(res):
        image_url = 'https://ptpimg.me/{0}.{1}'.format(
            res['code'], res['ext'])
        return image_url

    def _perform(self, resp):
        if resp.status_code == requests.codes.ok:
            try:
                # print('Successful response', r.json())
                # r.json() is like this: [{'code': 'ulkm79', 'ext': 'jpg'}]
                return [self._handle_result(r) for r in resp.json()]
            except ValueError as e:
                raise UploadFailed(
                    'Failed decoding body:\n{0}\n{1!r}', e, resp.content
                ) from None
        else:
            raise UploadFailed(
                'Failed. Status {0}:\n{1}', resp.status_code, resp.content)

    def _send_upload(self, files: dict):
        headers = {'referer': 'https://ptpimg.me/index.php'}
        data = {'api_key': self.api_key}
        service_url = 'https://ptpimg.me/upload.php'
        return requests.post(service_url, headers=headers, data=data, files=files)

    def upload_file(self, filename):
        """ Upload file using form """
        # The ExitStack closes files for us when the with block exits
        with contextlib.ExitStack() as stack:
            open_file = stack.enter_context(open(filename, 'rb'))
            mime_type, _ = mimetypes.guess_type(filename)
            if not mime_type or mime_type.split('/')[0] != 'image':
                raise ValueError(
                    'Unknown image file type {}'.format(mime_type))

            name = os.path.basename(filename)
            try:
                # until https://github.com/shazow/urllib3/issues/303 is
                # resolved, only use the filename if it is Latin-1 safe
                e_name = name.encode('latin-1', 'replace')
                name = e_name.decode('latin-1')
            except UnicodeEncodeError:
                name = 'justfilename'

            files = {'file-upload[]': (
                name, open_file, mime_type)}
            resp = self._send_upload(files=files)

        return self._perform(resp)

    def upload_url(self, url):
        """ Upload image URL """
        with contextlib.ExitStack() as stack:
            resp = requests.get(url, timeout=self.timeout)
            if resp.status_code != requests.codes.ok:
                raise ValueError(
                    'Cannot fetch url {} with error {}'.format(url, resp.status_code))

            mime_type = resp.headers['content-type']
            if not mime_type or mime_type.split('/')[0] != 'image':
                raise ValueError(
                    'Unknown image file type {}'.format(mime_type))

            open_file = stack.enter_context(BytesIO(resp.content))

            files = {'file-upload[]': (
                'justfilename', open_file, mime_type)}
            resp = self._send_upload(files)

            return self._perform(resp)


def _partition(files):
    file_list = []
    for file in files:
        if os.path.exists(file):
            file_list.append({'type': 'file',
                                  'path': file})
        else:
            raise ValueError(
                'Not an existing file or image URL: {}'.format(file))
    return file_list


def upload(api_key, files, timeout=None):
    uploader = PtpimgUploader(api_key, timeout)
    file_list = _partition(files)
    results = []
    if file_list:
        for file in file_list:
            results += uploader.upload_file(file['path'])
    return results