paths = ["./inputs/silesia/dickens", "./inputs/silesia/mozilla", "./inputs/silesia/mr", "./inputs/silesia/nci", "./inputs/silesia/ooffice", "./inputs/silesia/reymont", "./inputs/silesia/samba", "./inputs/silesia/sao", "./inputs/silesia/webster", "./inputs/silesia/x-ray", "./inputs/silesia/xml"]


with open("silesiafull", "wb") as output:
    for path in paths:
        with open(path, "rb") as file:
            output.write(file.read())

    

