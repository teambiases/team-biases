import _path_config

import sys
import json
import string

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 render_template.py template vars.json output')
        print('Given a file which contains template syntax (see python string.Template),')
        print('renders the template with the variables in vars.json, and writes the resulting')
        print('string to output.')
    else:
        _, template_fname, vars_fname, out_fname = sys.argv
        
        with open(template_fname, 'r') as template_file:
            template = string.Template(template_file.read())
            
        with open(vars_fname, 'r') as vars_file:
            vars = json.load(vars_file)
            
        output = template.substitute(vars)
            
        with open(out_fname, 'w') as out_file:
            out_file.write(output)
