from registry import Registry

def main():
    registry = Registry()
    
    #create objects
    registry.add_student("Thatoe", 20, "CS", 3.5)
    registry.add_student("Ray", 21, "CS", 3.6)
    registry.add_student("Tyler", 22, "CS", 3.7)
    registry.add_student("Nyan", 23, "DIT", 3.8)

    #read
    registry.show_students()
    print(f"Average age: {registry.get_average_age()}")

    #update
    registry.update_by_name("Ray", 22)
    registry.update_by_name("Tyler", 27)
    registry.update_by_name("David", 24)


    #delete
    registry.delete_by_name("Ray")
    registry.delete_by_name("Tyler")

    registry.show_students()






if __name__ == "__main__":
    main()