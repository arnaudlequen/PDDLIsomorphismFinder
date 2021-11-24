from time import time


def measure_time(func, *args):
    start_time = time()
    func(*args)
    return time() - start_time


def progress_bar(percentage, width=10):
    char_left = int(percentage*width)
    if char_left < percentage * width:
        s = '█'*char_left + '▓'
    else:
        s = '█'*char_left
    return f"[{s:░<{width}}] {percentage * 100:.1f}%"
