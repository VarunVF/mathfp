import os

from util import try_read_file


class PreprocessorError(Exception):
    pass


class Preprocessor:
    def __init__(self):
        self.lines: list[str] = []
        self.included_files: set[str] = set()

    @staticmethod
    def expect_char(sequence: str, pos: int, char: str, msg: str):
        if sequence[pos] != char:
            raise PreprocessorError(msg)

    def call_macro(self, macro, arguments):
        match macro:
            case 'include':
                self.include(*arguments)
            case _:
                raise PreprocessorError(f"No such macro '{macro}'")

    def expect_macro_format(self, macro_call: str):
        self.expect_char(macro_call, 0, '!', "Expected '!' before macro call")

        macro_name = ''
        idx = 0
        for char in macro_call:
            if char == '(':
                break
            if char != '!':
                macro_name += char
            idx += 1
        self.expect_char(macro_call, idx, '(', "Expected '(' after macro name")

        argument = ''
        for char in macro_call[idx + 1:]:
            if char == ')':
                break
            argument += char
            idx += 1
        self.expect_char(macro_call, idx + 1, ')', "Expected ')' after macro argument")

        return macro_name, argument

    def include(self, copy_to_file: str, copy_from_file: str, copy_pos: int):
        parent_dir = os.path.dirname(copy_to_file)
        abs_copy_from_file = os.path.join(parent_dir, copy_from_file)

        if abs_copy_from_file in self.included_files:
            return  # Avoid double-include

        if os.path.isfile(abs_copy_from_file):
            contents = try_read_file(abs_copy_from_file)
        elif os.path.isdir(abs_copy_from_file):
            print(f"!include: '{copy_from_file}' is a directory")
            return
        else:
            print(f"!include: No such file '{copy_from_file}' found")
            return

        self.lines.insert(copy_pos, contents)
        self.included_files.add(abs_copy_from_file)

    def preprocess(self, source: str, filename: str):
        # TODO: strip line comments here instead of in the tokeniser
        self.lines = source.splitlines(keepends=True)
        line_no = 0
        for line in self.lines:
            stripped = line.strip()
            if stripped.startswith('!') and len(stripped) > 1:
                macro_name, argument = self.expect_macro_format(stripped)
                # replace the macro call with the contents
                self.lines.pop(line_no)
                self.call_macro(macro_name, (filename, argument, line_no))
            line_no += 1

        return ''.join(self.lines)
