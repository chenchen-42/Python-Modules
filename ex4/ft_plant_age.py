def ft_plant_age():
    age = int(input("Enter plant age: "))
    if age <= 60:
        print("Plant needs more time to grow.")
    else:
        print("Plant is ready to harvest!")


if __name__ == "__main__":
    ft_plant_age()
