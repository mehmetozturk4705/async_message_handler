import os
import asyncio
from multiprocessing import Queue, Lock
import threading
import queue
import uuid
import time

from dataclasses import dataclass

@dataclass
class CommandContext:
    tx_queue:Queue
    rx_queue:Queue
    _lock = Lock()
    _context = dict()

    def initialize(self):
        """
        Initializes current context as context of thread/process.
        """
        context_id = CommandContext._get_context_id()
        if context_id not in CommandContext._context:
            with CommandContext._lock:
                CommandContext._context[context_id] = self

    @classmethod
    def _get_context_id(cls):
        return f"{os.getpid()}/{threading.get_ident()}"

    @classmethod
    def get_current_context(cls):
        context_id = cls._get_context_id()
        with CommandContext._lock:
            if context_id not in cls._context:
                raise ValueError("There is no CommandContext initialized for this thread/process.")
            else:
                return cls._context[context_id]

    def get_next(self, block=True, timeout=None)->"ProcessCommand":
        """
        Gathers next ProcessCommand object.

        :param block: If this is remains default(True), this operation blocks current thread/process until new command.
        :param timeout: Timeout.
        :return: CommandContext
        """
        return self.tx_queue.get(block=block, timeout=timeout)



class ProcessCommand(object):
    def __init__(self, command_id:str, payload):
        """
        Creates a command object.

        :param command_id: Command id.
        :param command_context: CommandContext.
        :param payload: Command payload.
        """
        self._command_id = command_id
        self._response_status = False
        self._payload = payload

    def get_payload(self):
        """
        Gathers command payload.

        :return: Payload object
        """
        return self._payload

    def reply(self, payload):
        """
        Replies current command.

        :param payload: Reply payload object.
        :return:
        """
        if not self._response_status:
            command_context = CommandContext.get_current_context()
            command_context.rx_queue.put_nowait((self._command_id, payload))
            self._response_status = True
            self._payload = None
            self._command_id = None
        else:
            raise ValueError("You cannot reply to a command multiple times.")


class ProcessCommandHandler(object):
    def __init__(self, timeout:int=None):
        """
        Process command handler to manage data transfer from thread or process to async context.

        :param timeout: Awaiting timeout in seconds.
        """
        self._timeout = timeout
        self._tx_queue = Queue()
        self._rx_queue = Queue()
        self._command_ids = set()
        self._responses = dict()
        self._command_context = CommandContext(self._tx_queue, self._rx_queue)

    def _get_new_command_id(self):
        while True:
            cur_context_id = uuid.uuid4().hex
            if cur_context_id not in self._command_ids \
                    and cur_context_id not in self._responses:
                return cur_context_id

    def _tick(self):
        try:
            command_id, payload = self._rx_queue.get_nowait()
        except queue.Empty:
            return
        if command_id in self._command_ids:
            self._command_ids.remove(command_id)
            self._responses[command_id] = payload

    @asyncio.coroutine
    def command(self, message):
        """
        Send new command to process.

        :param message: Payload
        """
        command_id = self._get_new_command_id()
        self._command_ids.add(command_id)
        self._tx_queue.put_nowait(ProcessCommand(command_id, message))
        start_time = time.time()
        while True:
            if self._timeout is not None and (time.time()-start_time)>self._timeout:
                self._command_ids.remove(command_id)
                raise TimeoutError("Process did not respond command in specified time.")
            self._tick()
            if command_id not in self._responses:
                yield
            else:
                response = self._responses[command_id]
                del self._responses[command_id]
                return response


    def get_command_context(self)->CommandContext:
        """
        Gathers command context object of this handler.
        This context should be initialized in the process/thread which will be communicated via using obj.initialize method.

        :return: CommandContext object.
        """

        return self._command_context