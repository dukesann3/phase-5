

def testing():
    try:
        try:
            raise ValueError("a")
        except:
            raise ValueError("hi")
        
    except ValueError as e:
        print("poo", e)

testing()

