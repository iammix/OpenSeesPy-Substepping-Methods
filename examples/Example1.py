import openseespy.opensees as ops


def main():
    """
    Create a Cantilever Problem
    """

    ops.wipe()
    ops.model('basic', '-ndm', 2, '-ndf', 3)




if __name__ == '__main__':
    main()