from interpreterv4 import Interpreter

test = """
func somefxn(x) {
  var y;
  y = 10;
  x = 8 + y;
}

func main() {
	print("hello world");
	var y;
	if (true) {
	  var x;
	  x = 5; 
	  y = 7 + x;
	}
	/* y is evaluated below so it now looks for x */
	print(y);
	/* for popping scope: */
	var z;
	z = y + 3;
	somefxn(z);
	print(z);
}

/*
*OUT*
hello world
12
15
*OUT*
*/
"""


a = Interpreter(); 
a.run(test)