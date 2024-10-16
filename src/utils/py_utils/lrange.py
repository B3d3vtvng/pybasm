def lrange(*args):
    if len(args) > 2:
        raise Exception("lrange only takes 2 arguments")
    
    for arg in args:
        if not isinstance(arg, int):
            raise Exception("Argument must be of type Integer")
        
    if len(args) == 1:
        start = 0
    else:
        start = args[0]
        args.pop(0)

    end = args[0]

    new_range = []
    for i in range(start, end):
        new_range.append(i)

    return new_range
