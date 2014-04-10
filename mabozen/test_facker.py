

from faker import Factory


def main():
    fake = Factory.create()

    print fake.word()

if __name__ == "__main__":
    
    main()