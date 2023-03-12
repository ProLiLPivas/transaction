from threading import Thread

import pika

import config
from cmd import Console
from server_requests import get_user


def run_mq_listener(cmd: Console):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.HOST))
    channel = connection.channel()
    channel.basic_consume(
        queue=str(config.CLIENT_ID),
        on_message_callback=cmd.on_mq_message,
        auto_ack=True
    )
    channel.start_consuming()


def run_console_listener(cmd: Console):
    while True:
        cmd.on_cmd_input(input())


def main():
    print(f'WELCOME {get_user(config.CLIENT_ID)["username"]}')
    cmd = Console(client_id=config.CLIENT_ID)
    console_listener = Thread(target=run_console_listener, args=(cmd,))
    rabbit_listener = Thread(target=run_mq_listener, args=(cmd,))
    console_listener.start()
    rabbit_listener.start()


if __name__ == '__main__':
    main()
