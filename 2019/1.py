with open("1.txt", "r") as file:
    content = file.readlines()

numbers = [int(number.strip()) for number in content]

print("step 1 : %s" % sum([number // 3 - 2 for number in numbers]))

total = 0
while len(numbers) > 0:
    numbers = [number // 3 - 2 for number in numbers]
    numbers = [number for number in numbers if number > 0]
    total += sum(numbers)

print("step 2 : %s" % total)