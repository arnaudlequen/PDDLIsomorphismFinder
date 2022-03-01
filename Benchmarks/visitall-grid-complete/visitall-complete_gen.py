import sys

def main(argv):
    assert len(argv) == 2, "Usage: python3 visitall-complete_gen [Nb cities]"
    n = int(argv[1])
    with open(f"pfile{n}.pddl", 'w') as ifile:
        ifile.write(f"(define (problem grid-{n} )\n")
        ifile.write(f"(:domain grid-visit-all)\n")

        ifile.write(f"(:objects \n")
        for i in range(1, n+1):
            for j in range(1, n+1):
                ifile.write(f"\tloc-x{i}-y{j}\n")
        ifile.write(f"- place\n)\n")
        ifile.write(f"(:init\n")
        ifile.write(f"\t(at-robot loc-x1-y1)\n")
        ifile.write(f"\t(visited loc-x1-y1)\n")
        for i in range(1, n):
            for j in range(1, n):
                for dx, dy in [(0, 1), (1, 0)]:
                    ifile.write(f"\t(connected loc-x{i}-y{j} loc-x{i+dx}-y{j+dy})\n")
                    ifile.write(f"\t(connected loc-x{i+dx}-y{j+dy} loc-x{i}-y{j})\n")
                    if i + dx == n:
                        ifile.write(f"\t(connected loc-x{i+dx}-y{j} loc-x{i+dx}-y{j+1})\n")
                        ifile.write(f"\t(connected loc-x{i+dx}-y{j+1} loc-x{i+dx}-y{j})\n")
                    if j + dy == n:
                        ifile.write(f"\t(connected loc-x{i}-y{j+dy} loc-x{i+1}-y{j+dy})\n")
                        ifile.write(f"\t(connected loc-x{i+1}-y{j+dy} loc-x{i}-y{j+dy})\n")
                    

        ifile.write(")\n")
        ifile.write("(:goal\n(and \n")

        for i in range(1, n+1):
            for j in range(1, n+1):
                ifile.write(f"\t(visited loc-x{i}-y{j})\n")
        ifile.write(")\n)\n)")

if __name__ == "__main__":
    main(sys.argv)

