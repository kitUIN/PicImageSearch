from PicImageSeach.tracemoe import TraceMoe
tracemoe = TraceMoe()
t = tracemoe.search('https://trace.moe/img/tinted-good.jpg')
print(tracemoe.thumbnail)
print(tracemoe.similarity)
print(type(tracemoe.similarity))
