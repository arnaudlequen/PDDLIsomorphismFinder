from time import time

def measureTime(func, *args):
    start_time = time()
    func(*args)
    return time() - start_time

def progressBar(percentage, width=10):
    charLeft = int(percentage*width)
    if charLeft < percentage * width:
        s = '█'*charLeft + '▓'
    else:
        s = '█'*charLeft
    return f"[{s:░<{width}}] {percentage * 100:.1f}%"
