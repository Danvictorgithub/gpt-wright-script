import requests
import aiohttp
import asyncio

starterChat:str = "Lets pretend to have a basic conversation like a human, you can also pretend to have emotion, I would like you to limit the length of your response to small paragraphs, I will do the same. I repeat respond with short paragraph"
def chat(chatId, prompt,server):
    
    response = requests.post(f'{server}/conversation', data={"chatId":chatId,"prompt":prompt}).text
    print(f"{response}\n")
    return response

async def startChat(chatOneId:str,chatTwoId:str,serverOne,serverTwo):
    async with aiohttp.ClientSession() as session:
        post_tasks = [
            session.post(f'{serverOne}/conversation', data={"chatId":chatOneId,"prompt":starterChat}),
            session.post(f'{serverTwo}/conversation', data={"chatId":chatTwoId,"prompt":starterChat})
        ]
        responses = await asyncio.gather(*post_tasks)
        chatOneResponse = await responses[0].text()
        chatTwoResponse = await responses[1].text()
        print(chatOneResponse)
        print(chatTwoResponse)
        return chatOneResponse,chatTwoResponse

def startRecursiveChat(chatOneId:str,chatTwoId:str,serverOne,serverTwo,nextResponse:str,noResponse=0,responseLimit=100):
    noResponse +=1
    print("noResponse: ",noResponse)
    chatTwoResponse = chat(chatTwoId,nextResponse,serverTwo)
    if (noResponse < responseLimit):
        startRecursiveChat(chatTwoId,chatOneId,serverTwo,serverOne,chatTwoResponse,noResponse,responseLimit)
    else:
        print("Response limit reached")
    
def recursiveChat(chatOneId:str,chatTwoId:str,serverOne,serverTwo):
    chatOneResponse = chat(chatOneId,"You start the conversation",serverOne)
    startRecursiveChat(chatOneId,chatTwoId,serverOne,serverTwo,chatOneResponse,responseLimit=74)

def stressTest(chatOneId:str,serverOne:str):
    for i in range(1,100):
        chat(chatOneId,f"Test {i}",serverOne)
        print(i)

async def main():
    async with aiohttp.ClientSession() as session:
        serverOne = "http://localhost:8080"
        serverTwo = "http://localhost:8080"

        post_tasks = [
            session.post(f'{serverOne}/start'),
            session.post(f'{serverTwo}/start')
        ]
        checkHealthServerOne = requests.get(serverOne)
        print(checkHealthServerOne.text)
        checkHealthServerTwo = requests.get(serverTwo)
        print(checkHealthServerTwo.text)
        responses = await asyncio.gather(*post_tasks)
        chatOneJSON = await responses[0].json()
        chatOne = chatOneJSON['chatId']
        
        chatTwoJSON = await responses[1].json()
        chatTwo = chatTwoJSON['chatId']
        
        print(chatOne,chatTwo)
        stressTest(chatOne,serverOne)
        # await startChat(chatOne,chatOne,serverOne,serverTwo)
        # recursiveChat(chatOne,chatOne,serverOne,serverTwo)
asyncio.run(main())

