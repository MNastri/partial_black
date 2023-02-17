"""
It is partial black in python to be utilized in windows PyCharm.
- To see partial black here (https://blog.godatadriven.com/black-formatting-selection)
- This code is conversion of this shell script (https://gist.github.com/BasPH/5e665273d5e4cb8a8eefb6f9d43b0b6d)

If you want to use in windows, you should first complie this python to exe.
- To do that, see (https://pypi.org/project/auto-py-to-exe/)
"""
import os
import re
import sys
import tempfile

# get the system argv
print("The arguments are: ", str(sys.argv))
_partial_black = sys.argv[0]
black = sys.argv[1]
input_file = sys.argv[2]
start_line = int(sys.argv[3]) - 1
end_line = int(sys.argv[4])


# read input_file
with open(input_file, "rt", encoding="utf-8") as src_file:
    src_contents = [line for line in src_file]
# remove shared indentation
indent_spaces = min([len(re.findall(r"^ *", l)[0]) for l in src_contents])
selection = [l[indent_spaces:] for l in src_contents[start_line:end_line]]
# # fix mixed indentation in selection
# updated_lines = []
# for line in src_contents:
#     updated_lines += (re.sub(r"^( {3}\t| {2}\t| \t|\t)", "    ", line),)
# print(updated_lines)
print("Total file len: ", len(src_contents), ". selected lines: ", len(selection))


# it is a workaround for escaping windows os permission problem.
tmp_dir = tempfile.TemporaryDirectory()
tmp_file_name = os.path.join(tmp_dir.name, "tmp_file_for_black")


# write selection on tmp_file
with open(tmp_file_name, "wt", encoding="utf-8") as f:
    f.writelines(selection)


# run black on tmp_file
cmd = black + " " + tmp_file_name
print("Run cmd:", cmd)
os.system(cmd)


# apply reformatted selection to origianl source file
with open(tmp_file_name, "rt", encoding="utf-8") as f:
    del src_contents[start_line:end_line]
    for i, line in enumerate(f):
        # include indentation
        ident_line = " " * indent_spaces + line
        src_contents.insert(start_line + i, line)


# overwrite it to input_file
with open(input_file, "wt", encoding="utf-8") as f:
    f.writelines(src_contents)
