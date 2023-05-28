import asyncio
from datetime import datetime
from typing import List

from aio_pika import DeliveryMode, IncomingMessage, Message, connect
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket

from app import crud, schemas
from loguru import logger



class Notifier:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.is_ready = False

    async def setup(self, queue_name: str, is_consumer: bool):
        self.rmq_conn = await connect(
            # "amqp://guest:guest@rabbitmq/",
            host="rabbitmq-container",
            loop=asyncio.get_running_loop(),
        )
        self.channel = await self.rmq_conn.channel()
        self.exchange = await self.channel.declare_exchange(
            name="sdm-direct", type="direct", durable=True, auto_delete=False
        )
        self.queue_name = queue_name
        self.queue = await self.channel.declare_queue(
            self.queue_name, durable=True, auto_delete=False
        )
        await self.queue.bind(exchange="sdm-direct", routing_key=queue_name)
        # 是consumer才consume
        if is_consumer:
            await self.queue.consume(self._notify, no_ack=True)
        self.is_ready = True

    async def push(self, msg: str):
        print("ready to push notification into rabbitmq")
        await self.exchange.publish(
            Message(msg.encode("utf-8"), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=self.queue_name,
        )
        print("after publish msg into queue")

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def _notify(self, message: IncomingMessage):
        print("in _notify!!!!!!")
        living_connections = []
        while len(self.connections) > 0:
            websocket = self.connections.pop()
            new_message = message.body.decode("utf-8")
            print("incomingMessage >>> ", new_message)
            await websocket.send_text(f"{new_message}")
            living_connections.append(websocket)
        self.connections = living_connections


# 寄送通知
async def notify(
    db: Session, notification_obj: schemas.notification.NotificationSendObjectModel
):
    """
    Send notification. Insert notification data into DB first and publish notification into message queue.
    """
    logger.info(notification_obj)
    # insert notification data into db
    insert_obj = schemas.notification.NotificationCreate(
        receiver_uuid=notification_obj.receiver_uuid,
        # sender_uuid=notification_obj.sender_uuid,
        send_time=datetime.now(),
        template_uuid=notification_obj.template_uuid,
        f_string=notification_obj.f_string,
        is_read=False,
    )
    crud.notification.create(db=db, obj_in=insert_obj)
    await send_notification_to_message_queue(db, insert_obj)


# 將通知push到rabbitmq裡
async def send_notification_to_message_queue(db, notification_obj):
    # declare queue and send notification into queue
    # notification_text is composed of notification_template's text and notifications's f_string
    # check if specific notification_template exists
    notification_template = crud.notification_template.get_by_template_id(
        db=db, template_id="matching_result"
    )
    if notification_template is None:
        raise ValueError(
            "Fail to retrieve notification_template with template_uuid = matching_result"
        )
    else:
        notification_text = notification_template.text
        # loop to replace
        for idx, f in enumerate(notification_obj.f_string.split(";")):
            notification_text = notification_text.replace("{" + str(idx) + "}", f)
        print("msg ready to push into rabbitmq >>> ", notification_text)

        # estabilish connection with RabbitMQ server
        user = crud.user.get_by_user_uuid(
            db=db, user_uuid=notification_obj.receiver_uuid
        )
        user_email = ""
        if user is not None:
            user_email = user.email
        else:
            raise ValueError(
                f"Fail to retrieve user with user_uuid={notification_obj.receiver_uuid}"
            )
        print("user email >>> ", user_email)
        notifier = Notifier()
        await notifier.setup(queue_name=user_email, is_consumer=False)
        await notifier.push(f"{notification_text}")
        print(f"sucessfuly push notification into queue-{user_email}")
