from program import SingleProgram


def callback(raw):
    pass


program = SingleProgram(callback)
print(program.get_effects())
program.start()
