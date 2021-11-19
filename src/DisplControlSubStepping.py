import numpy as np
import openseespy.opensees as ops


def DispControlSubStep(Nsteps:int , IDctrlNode:int, IDctrlDOF:int, Dmax:float, fac1=2, fac2=4, fac3=8, fac4=16, LoadConstandTimeZero=False):
    """
    :param Nsteps: Number of Steps for the Analysis
    :param IDctrlNode: ID of the Control Node
    :param IDctrlDOF: DOF for Monitoring
    :param Dmax: Target Displacement
    :param LoadConstandTimeZero: True if you want to define pseudotime at the end of the analysis. Default is False
    """

    if not fac1 < fac2:
        raise ValueError("fac1 must be smaller than fac2")
    if not fac2 < fac3:
        raise ValueError("fac2 must be smaller than fac3")
    if not fac3 < fac4:
        raise ValueError("fac3 must be smaller than fac4")

    NodeDisplacement = []
    NodeReaction = []
    committedSteps = 0
    Dincr = Dmax / Nsteps
    for i in range(Nsteps):
        ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
        AnalOk = ops.analyze(1)
        #NodeDisplacement.append(ops.nodeDisp(IDctrlNode, IDctrlDOF))
        #NodeReaction.append(ops.nodeResponse(0, IDctrlDOF, 6))
        if AnalOk != 0:
            break
        else:
            committedSteps += 1

    # Start SubStepping

    if AnalOk != 0:
        firstFail = 1
        Dstep = 0.0
        Nk = 1
        AnalOk = 0
        retrunToInitStepFlag = False
        while Dstep <= 1.0 and AnalOk == 0:
            controlDisp = ops.nodeDisp(IDctrlNode, IDctrlDOF)
            Dstep = controlDisp / Dmax
            if (Nk == 2 and AnalOk == 0) or (Nk == 1 and AnalOk == 0):
                Nk = 1
                if retrunToInitStepFlag:
                    print("Back to Initial Step")
                    retrunToInitStepFlag = False
                if firstFail == 0:
                    ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
                    AnalOk = ops.analyze(1)
                else:
                    AnalOk = 1
                    firstFail = 0
                if AnalOk == 0:
                    committedSteps += 1
            # substepping /2
            if (AnalOk != 0 and Nk == 1) or (AnalOk == 0 and Nk == fac2):
                Nk = fac1
                continueFlag = 1
                DincrReduced = Dincr / Nk
                print(f"Initial Step id Divided by {fac1}")
                ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, DincrReduced)
                for ik in range(Nk - 1):
                    if continueFlag == 0:
                        break
                    AnalOk = ops.analyze(1)
                    if AnalOk == 0:
                        committedSteps += 1
                    else:
                        continueFlag = 0
                if AnalOk == 0:
                    retrunToInitStepFlag = True
            # substepping /4
            if (AnalOk != 0 and Nk == fac1) or (AnalOk == 0 and Nk == fac3):
                Nk = fac2
                continueFlag = 1
                print(f"Initial Step is Divided by {fac2}")
                DincrReduced = Dincr / Nk
                ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, DincrReduced)
                for i in range(Nk - 1):
                    if continueFlag == 0:
                        break
                    AnalOk = ops.analyze(1)
                    if AnalOk == 0:
                        committedSteps += 1
                    else:
                        continueFlag = 0
                if AnalOk == 0:
                    retrunToInitStepFlag = True
            # substepping / 8
            if (AnalOk != 0 and Nk == fac2) or (AnalOk == 0 and Nk == fac4):
                Nk = fac3
                continueFlag = 1
                print(f"Initial Step is Divided by {fac3}")
                DincrReduced = Dincr / Nk
                ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, DincrReduced)
                for i in range(Nk - 1):
                    if continueFlag == 0:
                        break
                    AnalOk = ops.analyze(1)
                    if AnalOk == 0:
                        committedSteps += 1
                    else:
                        continueFlag = 0
                if AnalOk == 0:
                    retrunToInitStepFlag = True

            if (AnalOk != 0 and Nk == fac3):
                Nk = fac4
                continueFlag = 1
                print(f"Initial Step is Divided by {fac4}")
                DincrReduced = Dincr / Nk
                ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, DincrReduced)
                for i in range(Nk - 1):
                    if continueFlag == 0:
                        break
                    AnalOk = ops.analyze(1)
                    if AnalOk == 0:
                        committedSteps += 1
                    else:
                        continueFlag = 0
                if AnalOk == 0:
                    retrunToInitStepFlag = True
            controlDisp = ops.nodeDisp(IDctrlNode, IDctrlDOF)
            Dstep = controlDisp / Dmax
    # Analysis Status
    if AnalOk == 0:
        print("Analysis Completed SUCCESSFULLY")
        print("Commited Steps {}".format(committedSteps))
    else:
        print("Analysis FAILED")
        print("Commited Steps {}".format(committedSteps))
    if LoadConstandTimeZero == True:
        ops.loadConst('-time', 0.0)
        ops.setTime(0.0)
