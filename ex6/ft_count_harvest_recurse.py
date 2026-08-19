def ft_recursive_helper(day, days):
    if day > days:
        return
    print("Day", day)
    ft_recursive_helper(day + 1, days)


def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))
    ft_recursive_helper(1, days)
    print("Harvest time!")


if __name__ == "__main__":
    ft_count_harvest_recursive()
