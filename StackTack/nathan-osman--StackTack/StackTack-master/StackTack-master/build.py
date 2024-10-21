# JuiceBuilder - A lightweight Python build system for JavaScript and CSS files
# Copyright 2012 - Nathan Osman
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from json import loads
from os import path, mkdir
from re import compile, DOTALL, sub
from sys import argv
from urllib import urlencode
from urllib2 import urlopen

# This class returns 'tokens' from an input stream
class FileStream:
    
    TokenCommand = 1
    TokenContent = 2
    
    # Precompiled regexs that helps find the preprocessor definitions and manipulate them
    command_regex = compile(r'/\*\s+@(\w+)(?:\s+(.+?))?\s+\*/')
    split_regex   = compile(r'\s+')
    
    # Initializes the stream
    def __init__(self, filename):
        f = open(filename, 'r')
        self.contents = f.read()
        f.close()
        self.pos = 0 # our position in the input stream
    
    # Allows this object to be used as an iterator
    def __iter__(self):
        return self
    
    # Returns the next token in the stream
    def next(self):
        if self.pos >= len(self.contents):
            raise StopIteration
        m = self.command_regex.search(self.contents[self.pos:])
        if m and m.start():
            token = { 'type': self.TokenContent, 'content': self.contents[self.pos:self.pos + m.start()], }
            self.pos += m.start()
            return token
        elif m:
            self.pos += m.end()
            p = m.group(2)
            if p:
                p = self.split_regex.split(p)
            return { 'type': self.TokenCommand, 'command': m.group(1), 'parameter': p, }
        else:
            token = { 'type': self.TokenContent, 'content': self.contents[self.pos:], }
            self.pos = len(self.contents)
            return token

# This class loads the project and builds the files
class JuiceBuilder:
    
    # Valid commands
    commands = ['if', 'else', 'endif', 'include',]
    
    # Precompiled regular expressions
    arg_regex     = compile(r'^--(enable|disable)-(.*)$')
    comment_regex = compile(r'\s*/\*.*?\*/\s*', DOTALL)
    ws_regex      = compile(r'\s+')
    
    # Initializes the builder
    def __init__(self):
        self._print_header()
        self._load_project()
        self._parse_command_line()
    
    # Prints copyright information for the program
    def _print_header(self):
        print 'Simple JavaScript / CSS minification and build system'
        print 'Copyright 2012 - Nathan Osman\n'
    
    # Loads the project defaults and help strings from the juice file
    def _load_project(self):
        f = open('juice.json', 'r')
        self.project = loads(f.read())
        f.close()
    
    # Parses the command line arguments, comparing them to the valid options
    def _parse_command_line(self):
        # This regex is used for matching the command line arguments
        for arg in argv[1:]:
            matches = self.arg_regex.match(arg)
            if not matches:
                raise Exception('invalid command line argument "%s"' % arg)
            action = matches.group(1)
            option = matches.group(2)
            # Make sure the option exists
            if not option in self.project['options']:
                raise Exception('unknown option "%s"' % option)
            self.project['options'][option]['value'] = True if action == 'enable' else False
    
    # Determines if the specified option is set
    def _is_option_set(self, option):
        return self.project['options'][option]['value']
    
    # Performs minification of the specified JS source file using Google's Closure compiler
    def _minify_js_file(self, input):
        params = urlencode({ 'js_code':           input,
                             'compilation_level': 'SIMPLE_OPTIMIZATIONS',
                             'output_format':     'json',
                             'output_info':       'compiled_code', })
        json_response = loads(urlopen('http://closure-compiler.appspot.com/compile',
                                      data=params).read())
        return json_response['compiledCode']
    
    # Performs basic RegEx based minification of CSS files
    def _minify_css_file(self, input):
        # Remove comments and unnecessary spaces
        output = self.comment_regex.sub('', input)
        return self.ws_regex.sub(' ', output)
    
    # Minifies the specified source file
    def _minify_file(self, input, filename):
        if filename.endswith('.js'):
            return self._minify_js_file(input)
        elif filename.endswith('.css'):
            return self._minify_css_file(input)
        else:
            return input # Passthru since we don't know the type
    
    # This method combines content tokens in the specified list into a single token
    def _combine_tokens(self, tokens):
        output = ''
        for t in tokens:
            output += t['content']
        return output
    
    # Utility method that pops tokens off the stack until the specified command token is found
    def _pop_until(self, stack, commands):
        tokens = []
        while not (stack[-1]['type'] == FileStream.TokenCommand and stack[-1]['command'] in commands):
            tokens.insert(0, stack.pop())
        stack.append({ 'type': FileStream.TokenContent, 'content': self._combine_tokens(tokens) })
    
    # Tokenizes and parses the specified file using the specified stack
    def _parse_file(self, src_file, stack, nest_level):
        print '%sBuilding "%s".' % ('  ' * nest_level, src_file,)
        input = FileStream(src_file)
        for t in input:
            stack.append(t)
            if stack[-1]['type'] == FileStream.TokenCommand:
                cmd = stack[-1]['command'].lower()
                if not cmd in self.commands:
                    raise Exception('Command "%s" not recognized.' % cmd)
                if cmd == 'endif':
                    stack.pop() # discard the endif
                    self._pop_until(stack, ('if', 'else',))
                    true_output = stack.pop()
                    false_output = None
                    if stack[-1]['type'] == FileStream.TokenCommand and stack[-1]['command'] == 'else':
                        stack.pop() # discard the else
                        self._pop_until(stack, ('if',))
                        false_output = true_output
                        true_output = stack.pop()
                    c = stack.pop()
                    if self._is_option_set(c['parameter'][0]):
                        stack.append(true_output)
                    elif not false_output == None:
                        stack.append(false_output)
                elif cmd == 'include':
                    inc = stack.pop()
                    fn = inc['parameter'][0]
                    minify = 'minify' in inc['parameter'][1:]
                    quote  = 'quote' in inc['parameter'][1:]
                    # Create a new stack for the included file
                    new_stack = []
                    self._parse_file(fn, new_stack, nest_level + 1)
                    if minify or quote:
                        c = self._combine_tokens(new_stack)
                        if minify:
                            c = self._minify_file(c, fn)
                        if quote:
                            c = '"' + c + '"'
                        stack.append({ 'type':  FileStream.TokenContent, 'content': c })
                    else:
                        stack.extend(new_stack)
    
    # Builds the specified file
    def _build_file(self, src_file):
        output_fn = 'out/%s' % (src_file['output'] if 'output' in src_file else src_file['filename'])
        stack = []
        self._parse_file(src_file['filename'], stack, 0)
        # Join and write the minified output
        output = ''
        for t in stack:
            # If this token isn't a content token, it is horribly out of place
            if not t['type'] == FileStream.TokenContent:
                raise Exception('unexpected command "%s" encountered' % t['command'])
            output += t['content']
        print 'Producing "%s".' % output_fn
        f = open(output_fn, 'w')
        f.write(self._minify_file(output, output_fn))
        f.close()
    
    # Builds the project
    def build(self):
        if not path.isdir('out'):
            mkdir('out')
        for src_file in self.project['files']:
            # Check to see if building this file depends on a condition
            if 'condition' in src_file:
                c = src_file['condition']
                if c.startswith('!'):
                    value = not self._is_option_set(c[1:])
                else:
                    value = self._is_option_set(c)
                if value:
                    self._build_file(src_file)
            else:
                self._build_file(src_file)
        print "\nBuild process completed without error."

try:
    # Create the builder and build the project
    builder = JuiceBuilder()
    builder.build()
except Exception as e:
    print 'Fatal error: %s.' % e