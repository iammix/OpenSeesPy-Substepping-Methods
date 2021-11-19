import openseespy.opensees as ops


def LoadControlSubStep(Nsteps:int, Lincr:float, fac1=2, fac2=4, fac3=8, fac4=16, LoadConstandTimeZero=False):
    """
    :param Nsteps: Number of Analysis Steps
    :param Lincr: LoadFactor Increment
    :param LoadConstandTimeZero: True if you want to define pseudotime at the end of the analysis. Default is False (optional)
    """

    if not fac1 < fac2:
        raise ValueError("fac1 must be smaller than fac2")
    if not fac2 < fac3:
        raise ValueError("fac2 must be smaller than fac3")
    if not fac3 < fac4:
        raise ValueError("fac3 must be smaller than fac4")

    LoadCounter = 0
    committedSteps = 1
    for i in range(Nsteps):
        AnalOk = ops.analyze(1)
        if AnalOk != 0:
            break
        else:
            LoadCounter += 1
            committedSteps += 1

    if AnalOk != 0:
        firstFail = 1
        AnalOk = 0
        Nk = 1
        retrunToInitStepFlag = False
        while (LoadCounter < Nsteps) and (AnalOk == 0):
            if (Nk == 2 and AnalOk == 0) or (Nk == 1 and AnalOk == 0):
                Nk = 1
                if retrunToInitStepFlag:
                    print("Back to Initial Step")
                    retrunToInitStepFlag = False

                if firstFail == 0:
                    ops.integrator('LoadControl', Lincr)
                    AnalOk = ops.analyze(1)
                else:
                    AnalOk = 1
                    firstFail = 0

                if AnalOk == 0:
                    LoadCounter = LoadCounter + 1 / Nk
                    committedSteps += 1
            # substepping /2
            if (AnalOk != 0 and Nk == 1) or (AnalOk == 0 and Nk == fac2):
                Nk = fac1
                continueFlag = 1
                print(f"Initial Step is Devided by {fac1}")
                LincrReduced = Lincr / Nk
                ops.integrator('LoadControl', LincrReduced)
                for i in range(Nk - 1):
                    if continueFlag == 0:
                        break
                    AnalOk = ops.analyze(1)
                    if AnalOk == 0:
                        LoadCounter = LoadCounter + 1 / Nk
                        committedSteps += 1
                    else:
                        continueFlag = 0
                if AnalOk == 0:
                    retrunToInitStepFlag = True
            # substepping /4
            if (AnalOk != 0 and Nk == fac1) or (AnalOk == 0 and Nk == fac3):
                Nk = fac2
                continueFlag = 1
                print(f'Initial Step is Devided by {fac2}')
                LincrReduced = Lincr / Nk
                ops.integrator('LoadControl', LincrReduced)
                for i in range(Nk - 1):
                    if continueFlag == 0:
                        break
                    AnalOk = ops.analyze(1)
                    if AnalOk == 0:
                        LoadCounter = LoadCounter + 1 / Nk
                        committedSteps += 1
                    else:
                        continueFlag = 0
                if AnalOk == 0:
                    retrunToInitStepFlag = True
            # substepping /8
            if (AnalOk != 0 and Nk == fac2) or (AnalOk == 0 and Nk == fac4):
                Nk = fac3
                continueFlag = 1
                print(f'Initial Step is Devided by {fac3}')
                LincrReduced = Lincr / Nk
                ops.integrator('LoadControl', LincrReduced)
                for i in range(Nk - 1):
                    if continueFlag == 0:
                        break
                    AnalOk = ops.analyze(1)
                    if AnalOk == 0:
                        LoadCounter = LoadCounter + 1 / Nk
                        committedSteps += 1
                    else:
                        continueFlag = 0
                if AnalOk == 0:
                    retrunToInitStepFlag = True
            # substepping /16
            if (AnalOk != 0 and Nk == fac3):
                Nk = fac4
                continueFlag = 1
                print(f'Initial Step is Devided by {fac4}')
                LincrReduced = Lincr / Nk
                ops.integrator('LoadControl', LincrReduced)
                for i in range(Nk - 1):
                    if continueFlag == 0:
                        break
                    AnalOk = ops.analyze(1)
                    if AnalOk == 0:
                        LoadCounter = LoadCounter + 1 / Nk
                        committedSteps += 1
                    else:
                        continueFlag = 0
                if AnalOk == 0:
                    retrunToInitStepFlag = True
        # Analysis Status
    if AnalOk == 0:
        print("Analysis Completed SUCCESSFULLY")
        print("Committed Steps {}".format(committedSteps))
    else:
        print("Analysis FAILED")
        print("Committed Steps {}".format(committedSteps))
    if LoadConstandTimeZero == True:
        ops.loadConst('-time', 0.0)
        ops.setTime(0.0)
