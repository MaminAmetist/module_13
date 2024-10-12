# Асинхронность на практике
# Задача "Асинхронные силачи":
import asyncio


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    for i in range(5):
        await asyncio.sleep(10 / power)
        print(f'Силач {name} поднял {i + 1} шар.')
    print(f'Силач {name} закончил соревнования.')


async def start_tournament():
    print('Соревнования начались.')
    athlete_1 = asyncio.create_task(start_strongman('Pasha', 3))
    athlete_2 = asyncio.create_task(start_strongman('Denis', 4))
    athlete_3 = asyncio.create_task(start_strongman('Apollon', 5))
    await athlete_1
    await athlete_2
    await athlete_3
    print('Конец соревнований.')


asyncio.run(start_tournament())
