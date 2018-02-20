#! /usr/bin/env python3

import os
import re
import sys
import platform
import itertools
import socket
from time import time
from tempfile import NamedTemporaryFile
from deoplete.source.base import Base
from deoplete.util import error
sys.path.insert(1, os.path.dirname(__file__) + '/../../nvim_typescript')

from utils import getKind, convert_completion_data, convert_detailed_completion_data
# from simpletcp.clientsocket import ClientSocket
# import client
RELOAD_INTERVAL = 1
RESPONSE_TIMEOUT_SECONDS = 20


class Source(Base):

    # Base options
    def __init__(self, vim):
        Base.__init__(self, vim)
        self.name = "typescript"
        self.mark = self.vim.vars['nvim_typescript#completion_mark']
        self.filetypes = ["typescript", "tsx", "typescript.tsx", "javascript", "jsx", "javascript.jsx"] \
            if self.vim.vars["nvim_typescript#javascript_support"] \
            else ["typescript", "tsx", "typescript.tsx", "vue"] \
            if self.vim.vars["nvim_typescript#vue_support"] \
            else ["typescript", "tsx", "typescript.tsx"]
        self.rank = 1000
        self.min_pattern_length = 1
        self.input_pattern = '((?:\.|(?:,|:|->)\s+)\w*|\()'
        self._last_input_reload = time()
        self._max_completion_detail = self.vim.vars[
            "nvim_typescript#max_completion_detail"]
        self.client = socket.socket().connect(('127.0.0.1', 5000))
        # self.client = ClientSocket("localhost", 5000, single_use=False)
        # self._client = client
        # client.logFun = self.log

    def log(self, message):
        """
        Log message to vim echo
        """
        self.debug('************')
        self.debug('{} \n'.format(message))
        self.debug('************')

    def reload(self):
        """
        send a reload request
        """
        filename = self.relative_file()
        contents = self.vim.eval("join(getline(1,'$'), \"\n\")")

        tmpfile = NamedTemporaryFile(delete=False)
        tmpfile.write(contents.encode("utf-8"))
        tmpfile.close()
        client.reload(filename, tmpfile.name)
        os.unlink(tmpfile.name)

    def relative_file(self):
        """
        returns the relative file
        """
        return self.vim.current.buffer.name

    def get_complete_position(self, context):
        """
        returns the cursor position
        """
        # self.log(sys.modules['client'])
        m = re.search(r"\w*$", context['input'])
        return m.start() if m else self.vim.current.window.cursor.col

    def gather_candidates(self, context):
        self.log(client)
        # self.client.send('test')
        # response = self.client.recv(4096)
        # response = self.client.send('helloo')
        # self.vim.out_write('{} \n'.format(response))
        # self.log(response.decode())
        return []

        # try:
        #     if time() - self._last_input_reload > RELOAD_INTERVAL or re.search(r"\w*\.", context["input"]):
        #         self._last_input_reload = time()
        #         self.reload()
        #     data = self._client.completions(
        #         file=self.relative_file(),
        #         line=context["position"][1],
        #         offset=context["complete_position"] + 1,
        #         prefix=context["complete_str"]
        #     )
        #     # self.log(data)

        #     if len(data) == 0:
        #         return []

        #     if len(data) > self._max_completion_detail:
        #         filtered = []
        #         for entry in data:
        #             if entry["kind"] != "warning":
        #                 filtered.append(entry)
        #         return [convert_completion_data(e, self.vim) for e in filtered]

        #     names = []
        #     maxNameLength = 0

        #     for entry in data:
        #         if entry["kind"] != "warning":
        #             names.append(entry["name"])
        #             maxNameLength = max(maxNameLength, len(entry["name"]))

        #     detailed_data = self._client.completion_entry_details(
        #         file=self.relative_file(),
        #         line=context["position"][1],
        #         offset=context["complete_position"] + 1,
        #         entry_names=names
        #     )

        #     if len(detailed_data) == 0:
        #         return []

        #     return [convert_detailed_completion_data(e, self.vim) for e in detailed_data]

        # except:
        #     return []
