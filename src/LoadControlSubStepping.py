import openseespy.opensees as ops

def LoadControlSubStep(Nsteps, Lincr, LoadConstandTimeZero=False):
    LoadCounter = 0
    committedSteps = 1
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
                if (AnalOk != 0 and Nk == 1) or (AnalOk == 0 and Nk == 4):
                    Nk = 2
                    continueFlag = 1
                    print('Initial Step is Devided by 2')
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
                if (AnalOk != 0 and Nk == 2) or (AnalOk == 0 and Nk == 8):
                    Nk = 4
                    continueFlag = 1
                    print('Initial Step is Devided by 4')
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
                if (AnalOk != 0 and Nk == 4) or (AnalOk == 0 and Nk == 16):
                    Nk = 8
                    continueFlag = 1
                    print('Initial Step is Devided by 8')
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
                if (AnalOk != 0 and Nk == 8):
                    Nk = 16
                    continueFlag = 1
                    print('Initial Step is Devided by 16')
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