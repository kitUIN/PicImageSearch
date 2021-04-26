import PicImageSearch
import asyncio

client = PicImageSearch.Search()

async def asd():
    data = await client.ascii2d("https://media.discordapp.net/attachments/434660786581929984/835873479416479764/rPdxLpQ.png")
    # data = await client.google("https://media.discordapp.net/attachments/434660786581929984/835873479416479764/rPdxLpQ.png")
    # data = await client.iqdb("https://media.discordapp.net/attachments/434660786581929984/835873479416479764/rPdxLpQ.png")
    # data = await client.iqdb_3d("https://media.discordapp.net/attachments/434660786581929984/835873479416479764/rPdxLpQ.png")
    # data = await client.saucenao("https://media.discordapp.net/attachments/434660786581929984/835873479416479764/rPdxLpQ.png", api_key="your api key")
    # data = await client.tracemoe("https://media.discordapp.net/attachments/434660786581929984/835873479416479764/rPdxLpQ.png")
    print (data.raw)

loop = asyncio.get_event_loop()
loop.run_until_complete(asd())
loop.close()