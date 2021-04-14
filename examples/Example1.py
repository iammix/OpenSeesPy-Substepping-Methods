import openseespy.opensees as ops
from src.DisplControlSubStepping import DispControlSubStep
from src.LoadControlSubStepping import LoadControlSubStep


def main():
    """
    Create a Cantilever Problem
    """

    ops.wipe()
    ops.model('basic', '-ndm', 2, '-ndf', 3)
    height = 5.0
    nElem = 20

    ElemLength = height / nElem
    nodeID = []
    Ycoord = 0
    for i in range(nElem + 1):
        nodeID.append(i)
        ops.node(i, 0.0, Ycoord)
        Ycoord += ElemLength
    IDctrlNode = i

    ops.fix(0, 1, 1, 1)
    ops.geomTransf('Linear', 1)

    concrete = 'Concrete04'
    steel = 'Steel02'

    matTAGConc = 319
    matTAGSteel = 312
    fcc = -20000
    ec2c = -0.002
    ecu2c = -0.0035
    Ec = 30000000
    fct = 2200
    et = 0.001
    fy = 500000
    E0 = 200000000
    b = 0.01
    ops.uniaxialMaterial(concrete, matTAGConc, fcc, ec2c, ecu2c, Ec, fct, et)
    ops.uniaxialMaterial(steel, matTAGSteel, fy, E0, b, 20, 0.925, 0.15, 0, 1, 0, 1, 0)

    # Core Fibers
    ops.section('Fiber', 105)
    ops.patch('rect', 319, 11, 11, -0.20, -0.20, 0.20, 0.20)
    # Cover Fibers
    ops.patch('rect', 319, 15, 2, 0.250000, 0.200000, -0.250000, 0.250000)
    ops.patch('rect', 319, 15, 2, 0.250000, -0.250000, -0.250000, -0.200000)
    ops.patch('rect', 319, 2, 11, -0.250000, -0.200000, -0.200000, 0.200000)
    ops.patch('rect', 319, 2, 11, 0.200000, -0.200000, 0.250000, 0.200000)
    # create corner bars
    ops.layer('straight', 312, 4, 0.00025450, 0.200000, 0.200000, -0.200000, 0.200000)
    ops.layer('straight', 312, 4, 0.00025450, 0.200000, -0.200000, -0.200000, -0.200000)
    ops.beamIntegration('Lobatto', 100, 105, 3)

    for i in range(len(nodeID) - 1):
        ops.element('forceBeamColumn', i, nodeID[i], nodeID[i + 1], 1, 100, '-iter', 10, 1e-6)

    # Add Vertical Load at Top
    ops.timeSeries('Linear', 101)
    ops.pattern('Plain', 100, 101)
    ops.load(IDctrlNode, 0, -500, 0)

    # Solve Gravity First
    ops.system('UmfPack')
    ops.numberer('Plain')
    ops.constraints('Transformation')
    ops.integrator('LoadControl', 0.1)
    ops.test('RelativeTotalNormDispIncr', 0.001, 100, 2)
    ops.algorithm('Newton')
    ops.analysis('Static')
    LoadControlSubStep(10, 0.1, True)

    # Displacement Control Analysis(Pushover)
    ops.pattern('Plain', 200, 101)
    ops.load(IDctrlNode, 1, 0, 0)
    ops.system('UmfPack')
    ops.numberer('Plain')
    ops.constraints('Transformation')
    ops.test('RelativeTotalNormDispIncr', 1e-2, 500, 2)
    ops.algorithm('Newton')
    ops.analysis('Static')
    DispControlSubStep(100, IDctrlNode, 1, 1.0)


if __name__ == '__main__':
    main()
