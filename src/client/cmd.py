from abc import ABC
from typing import Any

from pydantic import PositiveInt

from server_requests import request_transaction, get_user
from utils import cast_money_string_to_float


class StatesEnum:
    RECEIVE = 'RECEIVE'
    ENTER_RECIPIENT = 'ENTER_RECIPIENT'
    ENTER_PRICE = 'ENTER_PRICE'
    CONFIRM = 'CONFIRM'


class Console:
    def __init__(self, client_id: PositiveInt):
        self.client_id = client_id
        self._history: list[str] = []
        self.inputs: dict[str, Any] = {}
        self._states_dict = self._init_states()
        self._current_state: ClientState = ClientState(self)
        self.switch_state(StatesEnum.RECEIVE)

    # S T A T E S
    def _init_states(self) -> dict[StatesEnum, 'ClientState']:
        return {
            StatesEnum.RECEIVE: ReceivingState(self),
            StatesEnum.ENTER_RECIPIENT: TransactionUserEnteringState(self),
            StatesEnum.ENTER_PRICE: TransactionPriceEnteringState(self),
            StatesEnum.CONFIRM: TransactionConfirmingState(self)
        }

    def switch_state(self, state_key: StatesEnum):
        self._current_state.exit()
        self._current_state = self._states_dict[state_key]
        self._current_state.start()

    # C A L B A C K S
    def on_cmd_input(self, cmd):
        self._current_state.on_cmd_command_entered(cmd)

    def on_mq_message(self, ch, method, properties, body):
        self._current_state.on_get_message(body)

    # O U T P U T
    def write(self, text: str):
        print(text)

    def save_to_history(self, text: str):
        self._history.append(text)

    def write_history(self):
        for line in self._history:
            print(line)
        self._history.clear()


class ClientState(ABC):

    def __init__(self, console: Console):
        self._console = console

    def start(self): ...
    def exit(self): ...
    def on_cmd_command_entered(self, cmd: str): ...
    def on_get_message(self, text: str): ...


class ReceivingState(ClientState):
    def start(self):
        balance = get_user(self._console.client_id)['money_amount']
        self._console.write(f'ur balance is {balance}')
        self._console.write('remittance: \n\n')
        self._console.inputs = {}
        self._console.write_history()

    def on_cmd_command_entered(self, cmd: str):
        match cmd:
            case '$':
                self._console.switch_state(StatesEnum.ENTER_RECIPIENT)

    def on_get_message(self, text):
        self._console.write(text)


class BaseTransactionDialogState(ClientState):

    def on_cmd_command_entered(self, cmd: str):
        if cmd.lower() in ['quit', 'q']:
            self._console.switch_state(StatesEnum.RECEIVE)

    def on_get_message(self, text):
        self._console.save_to_history(text)


class TransactionUserEnteringState(BaseTransactionDialogState):
    def start(self): self._console.write('Enter recipient')

    def on_cmd_command_entered(self, cmd: str):
        super().on_cmd_command_entered(cmd=cmd)
        self._console.inputs.update({'recipient': cmd})
        self._console.switch_state(StatesEnum.ENTER_PRICE)


class TransactionPriceEnteringState(BaseTransactionDialogState):
    def start(self): self._console.write('Enter money amount')

    def on_cmd_command_entered(self, cmd: str):
        super().on_cmd_command_entered(cmd=cmd)

        try:
            money_amount = cast_money_string_to_float(cmd)
            self._console.inputs.update({'money': money_amount})
        except TypeError:
            self._console.write('Invalid money input')
            self._console.switch_state(StatesEnum.RECEIVE)
        else:
            self._console.switch_state(StatesEnum.CONFIRM)


class TransactionConfirmingState(BaseTransactionDialogState):
    def start(self): self._console.write('Write y/yes to confirm transaction')

    def on_cmd_command_entered(self, cmd: str):
        if cmd.lower() in ['y', 'yes', 'yep']:
            request_transaction(user_id=self._console.client_id, **self._console.inputs)

        self._console.switch_state(StatesEnum.RECEIVE)
