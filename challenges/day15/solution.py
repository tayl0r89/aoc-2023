def hash(value: str) -> int:
    current_value = 0
    for val in value:
        current_value = current_value + ord(val)
        current_value = current_value * 17
        current_value = current_value % 256

    return current_value


if __name__ == "__main__":
    total = 0
    with open("input.txt", "r", encoding="utf-8") as file:
        for l in file.readlines():
            for value in l.strip().split(","):
                total = total + hash(value)

    print("======= PART 1 =========")
    print(total)

    instructions = None
    with open("input.txt", "r", encoding="utf-8") as file:
        for l in file.readlines():
            instructions = [ins.strip() for ins in l.strip().split(",")]

    print(instructions)

    boxes = {}
    for instruction in instructions:
        if instruction.endswith("-"):
            print("Removing " + instruction)
            label = instruction[:-1]
            location = hash(label)

            contents = boxes.get(location, None)
            if contents:
                boxes[location] = list(filter(lambda x: x[0] != label, contents))

        elif instruction[len(instruction) - 2] == "=":
            print("Putting in " + instruction)
            label, lens = instruction.split("=")
            lens = int(lens)
            location = hash(label)
            print(f"{label} is {location}")
            contents = boxes.get(location, None)
            if contents:
                result = []
                replaced = False
                for cont in contents:
                    if cont[0] == label:
                        print(f"Replacing {cont[0]} for {label}")
                        replaced = True
                        result.append((label, lens))
                    else:
                        result.append(cont)

                if not replaced:
                    print("Item to be appended")
                    result.append((label, lens))

                boxes[location] = result
                print(f"After {instruction} is {boxes[location]}")
            else:
                boxes[location] = [(label, lens)]
        else:
            raise ValueError(instruction)

    total = 0
    print(boxes)
    for key, value in boxes.items():
        for box_ind, content in enumerate(value):
            print(f"{content[0]}: Box {key + 1} * {box_ind + 1} * {content[1]}")
            lens_value = (1 + key) * (box_ind + 1) * content[1]
            total = total + lens_value

    print("===== PART 2 =========")
    print(total)