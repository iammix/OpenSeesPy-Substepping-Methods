# OpenSeesPy Sub-Stepping Methods
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6886325.svg)](https://doi.org/10.5281/zenodo.6886325)

## Project and Purpose

OpenSeesPy Sub-Stepping is a helpful package when your system is huge.  
There are 4 sequential divisions(/2, /4, /8, /16). From v0.1.2.0  user can define the substepping factors.
```python
DispControlSubStep(Nsteps:int , IDctrlNode:int, IDctrlDOF:int, Dmax:float, fac1=2, fac2=4, fac3=8, fac4=16, LoadConstandTimeZero=False)
LoadControlSubStep(Nsteps:int, Lincr:float, fac1=2, fac2=4, fac3=8, fac4=16, LoadConstandTimeZero=False)
```


## How to use

Download via pip. The only requirement is OpenSeesPy library.  


```bash
pip install OpenSeesPySubStepping
```
[Find the project release @Pypi.org](https://pypi.org/project/OpenSeesPySubStepping/)

## Versions
### v0.1.2.0
- Substepping factors can be modified be the user.  
*Note: Default substepping factors are 1/2, 1/4, 1/8, 1/16*
### v0.1.1.2
- Add description to pypi.org
- Update REAME.md with example
- Example folder
- Add github workflow in order to publish library to pypi.org

## Example
```python
import openseespy.opensees as ops
from OpenSeesPySubStepping import DispControlSubStep
from OpenSeesPySubStepping import LoadControlSubStep


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

```
