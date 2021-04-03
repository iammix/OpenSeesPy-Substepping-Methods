import numpy as np
import openseespy.opensees as ops


def DispControlSubStep(Nsteps, IDctrlNode, IDctrlDOF, Dmax, Dincr, LoadConstandTimeZero=False):
    """
    :param Nsteps: Number of Steps for the Analysis
    :param IDctrlNode: ID of the Control Node
    :param IDctrlDOF: DOF for Monitoring
    :param Dmax: Target Displacement
    :param Dincr: Displacement Increment
    :param LoadConstandTimeZero: True if you want to define pseudotime at the end of the analysis. Default is False
    """

    NodeDisplacement = []
    NodeReaction = []
    committedSteps = 0
    for i in range(Nsteps):
        AnalOk = ops.analyze(1)
        NodeDisplacement.append(ops.nodeDisp(IDctrlNode, IDctrlDOF))
        NodeReaction.append(ops.nodeResponse(0, IDctrlDOF, 6))
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
            if (AnalOk != 0 and Nk == 1) or (AnalOk == 0 and Nk == 4):
                Nk = 2
                continueFlag = 1
                DincrReduced = Dincr / Nk
                print("Initial Step id Divided by 2")
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
            if (AnalOk != 0 and Nk == 2) or (AnalOk == 0 and Nk == 8):
                Nk = 4
                continueFlag = 1
                print("Initial Step is Divided by 4")
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
            if (AnalOk != 0 and Nk == 4) or (AnalOk == 0 and Nk == 16):
                Nk = 8
                continueFlag = 1
                print("Initial Step is Divided by 8")
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

            if (AnalOk != 0 and Nk == 8):
                Nk = 16
                continueFlag = 1
                print("Initial Step is Divided by 16")
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
