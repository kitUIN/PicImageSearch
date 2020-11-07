from PicImageSeach.tracemoe import TraceMoe
tracemoe = TraceMoe()
t = tracemoe.search('https://trace.moe/img/tinted-good.jpg')
print(tracemoe.viedo)
print(tracemoe.similarity)
print(type(tracemoe.similarity))
