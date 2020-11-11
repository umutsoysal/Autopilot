from boat import * 
from util import *

def main():
	print("Single-Handed Sailing")
	#boat.polarDiagram()
	#print(boat.boatSpeed())

	myboat=initial()
	print(myboat.state.showState())


if __name__ == "__main__":
    main()