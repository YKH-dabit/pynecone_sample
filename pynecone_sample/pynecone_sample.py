"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
#from pcconfig import config

import json
import pynecone as pc
import redis.asyncio as aredis
import pynecone_sample.sub.dev # self module that can also reload
import asyncio
import time
options = ["1", "2", "3", "4", "5"]

 
def get_global_dependency():
    global gstate
    return gstate

def increase_counter():
    mod : GlobalState = get_global_dependency()
    mod.counter += 1

async def print_redis_json():
    mod : GlobalState = get_global_dependency()
    dic = json.loads(await mod.redis.get('test'))
    dic["a"] += 1
    await mod.redis.set('test', json.dumps(dic))
    print(await mod.redis.get('test'))


async def get_redis_state_counter() -> int:
    mod : GlobalState = get_global_dependency()
    dic = json.loads(await mod.redis.get('test'))
    return dic["a"]

class SetterState1(pc.State):
    selected: str = "1"
    redis_counter : int = 0

 
    def on_load(self):
        mod : GlobalState = get_global_dependency()
        self.redis_counter = mod.redis_counter
        
    @pc.var
    def global_state_counter(self) -> int:
        mod : GlobalState = get_global_dependency()
        return mod.counter
    
    async def change(self, value):
        self.selected = value
        increase_counter()
        await print_redis_json()
        self.redis_counter = await get_redis_state_counter()

def index():
    return pc.vstack(
        pc.badge(
            SetterState1.selected, color_scheme="green"
        ),
        pc.text("counter: " + SetterState1.global_state_counter),
        pc.text("Redis Counter: " + SetterState1.redis_counter),
        pc.select(
            options,
            on_change=SetterState1.change,
        ),
    )


class GlobalState:
    def __init__(self):
        self.counter = 0
        self.redis_counter = 0
        self.data_dict = {}
        self.redis = aredis.Redis(host='localhost', port=6379, db=0)
        loop = asyncio.get_event_loop()
        t = loop.create_task(self.fetch_test_data())
        t.add_done_callback(print)

    async def fetch_test_data(self):
        dic = json.loads(await self.redis.get('test'))
        self.redis_counter = dic["a"]
        return self.redis_counter

        
# Add state and page to the app.
global gstate
gstate = GlobalState()
app = pc.App(state=SetterState1)
app.add_page(index, on_load=SetterState1.on_load)
app.compile()
