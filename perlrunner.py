import subprocess

var1 = "Breaking News! $50 off 4on4 street hockey registration. Register by Feb 9 and enter promo code:"
var2 = "20140129"
pipe = subprocess.Popen(["./testTimex.pl", var1], stdout=subprocess.PIPE)

result = pipe.stdout.read()

print result