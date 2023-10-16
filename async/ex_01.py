import asyncio
async def say(what, when): # 코루틴은 함수 앞에 async를 붙임
    await asyncio.sleep(when) # 코루틴은 await로 완료 대기
    print(what)

loop = asyncio.get_event_loop() # 이벤트 루프를 가져옴
loop.run_until_complete(say('Hello world', 1)) # 코루틴을 등록하고 실행
loop.close()