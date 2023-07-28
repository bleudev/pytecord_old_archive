def warning(*args):
    largs = list(args)
    largs.reverse()
    largs.append('Warning:')
    largs.reverse()
    
    print(*largs)
