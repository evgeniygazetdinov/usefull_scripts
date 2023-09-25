
def main():

    ids="""
"""
    with open("my_file.py", "w+") as file:
        lines= ids.split("\n")
        lines = ",".join(lines)
        file.writelines(lines)
        file.close()

main()
