from NewInstance import new_instance

def instance_inputs():
    area = float(input("Area: "))
    perimeter = float(input("Perimeter: "))
    majorAxisLength = float(input("MajorAxisLength: "))
    minorAxisLength = float(input("MinorAxisLength: "))
    aspectRation = float(input("AspectRation: "))
    eccentricity = float(input("Eccentricity: "))
    convexArea = float(input("ConvexArea: "))
    equivDiameter = float(input("EquivDiameter: "))
    extent = float(input("Extent: "))
    solidity = float(input("Solidity: "))
    roundness = float(input("Roundness: "))
    compactness = float(input("Compactness: "))
    shapeFactor1 = float(input("ShapeFactor1: "))
    shapeFactor2 = float(input("ShapeFactor2: "))
    shapeFactor3 = float(input("ShapeFactor3: "))
    shapeFactor4 = float(input("ShapeFactor4: "))
    return area, perimeter, majorAxisLength, minorAxisLength, aspectRation, eccentricity, convexArea, equivDiameter, extent, solidity, roundness, compactness, shapeFactor1, shapeFactor2, shapeFactor3, shapeFactor4

while True:
    try:
        print("\n### Dry Bean RF ###")
        print("\n1.Insert a new Instance\n2.Exit\n")
        match int(input("Select an option above: ")):
            case 1:
                area, perimeter, majorAxisLength, minorAxisLength, aspectRation, eccentricity, convexArea, equivDiameter, extent, solidity, roundness, compactness, shapeFactor1, shapeFactor2, shapeFactor3, shapeFactor4 = instance_inputs()
                new_instance(area, perimeter, majorAxisLength, minorAxisLength, aspectRation, eccentricity, convexArea, equivDiameter, extent, solidity, roundness, compactness, shapeFactor1, shapeFactor2, shapeFactor3, shapeFactor4)
            case 2:
                break
    except:
        print("ERROR!")