while True:
    keys = ["stories", "client", "consult", "sending messages"]
    input_string = input("\n> ")

    if input_string == "0":
        break

    if "?" in input_string:
        print("Idk XD")

    else:
        
        found = False
        for key in keys:
            if key in input_string:
                print(input_string, "`", key, "`")
                found = True

        if not found:
            print("No key in message")
            