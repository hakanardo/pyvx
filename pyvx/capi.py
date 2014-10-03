from codegen import PythonApi, export


class OpenVxApi(PythonApi):

    @export("int()")
    def vxCreateContext():
        return 42


if __name__ == '__main__':
    import sys
    api = OpenVxApi(True)
    api.build(sys.argv[1])
