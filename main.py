import sys
import re
import pants_graph_view


if __name__ == '__main__':
    input_file_name = sys.argv[1]
    if len(sys.argv) > 2:
        output_file_name = sys.argv[2]
    else:
        if input_file_name.endswith('.dot'):
            output_file_name = re.sub(r'\.dot$', '.html', input_file_name)
        else:
            output_file_name = input_file_name + '.html'

    pants_graph_view.main(input_file_name, output_file_name)
