# This file is for running code in python that example.xs will match.

# define x int 0

# while x < 3 {
#     out x
#     assign x x + 1
# }

# if (x == 3) {
#     out "done"
# } else {
#     out "error"
# }
# Output:
# 0
# [2, 3]
# ['done']

x = 0
while x < 3:
    print(x)
    x += 1

if x == 3:
    print("done")
else:
    print("error")