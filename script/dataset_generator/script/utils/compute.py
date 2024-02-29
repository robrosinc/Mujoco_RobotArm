import numpy as np
rmass = [4, 0.32, 2.2, 0.2, 1.65, 0.35, 0.04, 0]

def compute_xc(q_list):
    S = np.sin(q_list)
    C = np.cos(q_list)
    xc = [0 for i in range(3)]

    xc[0]= S[0]*(S[1]*(C[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) + S[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50)) - C[1]*(C[3]*((C[5]*C[6])/10 + 1483/5000) - S[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + 61/200)) - C[0]*(S[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) - C[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50))
    xc[1] = C[1]*(C[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) + S[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50)) + S[1]*(C[3]*((C[5]*C[6])/10 + 1483/5000) - S[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + 61/200) - 1073/5000
    xc[2] = S[0]*(S[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) - C[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50)) + C[0]*(S[1]*(C[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) + S[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50)) - C[1]*(C[3]*((C[5]*C[6])/10 + 1483/5000) - S[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + 61/200))
    
    return np.array(xc)    

def compute_jacobian(q_list, rows, cols):
    S = np.sin(q_list)
    C = np.cos(q_list)

    Jv = [[0 for j in range(cols)] for i in range(rows)]

    Jv[0][0] = S[0]*(S[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) - C[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50)) + C[0]*(S[1]*(C[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) + S[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50)) - C[1]*(C[3]*((C[5]*C[6])/10 + 1483/5000) - S[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + 61/200))
    Jv[0][1] = S[0]*(C[1]*(C[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) + S[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50)) + S[1]*(C[3]*((C[5]*C[6])/10 + 1483/5000) - S[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + 61/200))
    Jv[0][2] = - C[0]*(C[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) + S[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50)) - S[0]*S[1]*(S[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) - C[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50))
    Jv[0][3] = S[0]*(C[1]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000)) + S[1]*S[2]*(C[3]*((C[5]*C[6])/10 + 1483/5000) - S[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50))) + C[0]*C[2]*(C[3]*((C[5]*C[6])/10 + 1483/5000) - S[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50))
    Jv[0][4] = S[0]*(S[1]*(C[2]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10) - C[3]*S[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10)) - C[1]*S[3]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10)) - C[0]*(S[2]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10) + C[2]*C[3]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10))
    Jv[0][5] = S[0]*(C[1]*((C[3]*C[6]*S[5])/10 + (C[5]*C[6]*S[3]*S[4])/10) - S[1]*(S[2]*((C[6]*S[3]*S[5])/10 - (C[3]*C[5]*C[6]*S[4])/10) + (C[2]*C[4]*C[5]*C[6])/10)) - C[0]*(C[2]*((C[6]*S[3]*S[5])/10 - (C[3]*C[5]*C[6]*S[4])/10) - (C[4]*C[5]*C[6]*S[2])/10)
    Jv[0][6] = S[0]*(C[1]*(S[3]*((C[4]*C[6])/10 - (S[4]*S[5]*S[6])/10) + (C[3]*C[5]*S[6])/10) + S[1]*(S[2]*(C[3]*((C[4]*C[6])/10 - (S[4]*S[5]*S[6])/10) - (C[5]*S[3]*S[6])/10) + C[2]*((C[6]*S[4])/10 + (C[4]*S[5]*S[6])/10))) + C[0]*(C[2]*(C[3]*((C[4]*C[6])/10 - (S[4]*S[5]*S[6])/10) - (C[5]*S[3]*S[6])/10) - S[2]*((C[6]*S[4])/10 + (C[4]*S[5]*S[6])/10))
    Jv[1][0] = 0
    Jv[1][1] = C[1]*(C[3]*((C[5]*C[6])/10 + 1483/5000) - S[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + 61/200) - S[1]*(C[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) + S[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50))
    Jv[1][2] = -C[1]*(S[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) - C[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50))
    Jv[1][3] = C[1]*S[2]*(C[3]*((C[5]*C[6])/10 + 1483/5000) - S[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50)) - S[1]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000))
    Jv[1][4] = C[1]*(C[2]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10) - C[3]*S[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10)) + S[1]*S[3]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10)
    Jv[1][5] = - S[1]*((C[3]*C[6]*S[5])/10 + (C[5]*C[6]*S[3]*S[4])/10) - C[1]*(S[2]*((C[6]*S[3]*S[5])/10 - (C[3]*C[5]*C[6]*S[4])/10) + (C[2]*C[4]*C[5]*C[6])/10)
    Jv[1][6] = C[1]*(S[2]*(C[3]*((C[4]*C[6])/10 - (S[4]*S[5]*S[6])/10) - (C[5]*S[3]*S[6])/10) + C[2]*((C[6]*S[4])/10 + (C[4]*S[5]*S[6])/10)) - S[1]*(S[3]*((C[4]*C[6])/10 - (S[4]*S[5]*S[6])/10) + (C[3]*C[5]*S[6])/10)
    Jv[2][0] = C[0]*(S[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) - C[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50)) - S[0]*(S[1]*(C[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) + S[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50)) - C[1]*(C[3]*((C[5]*C[6])/10 + 1483/5000) - S[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + 61/200))
    Jv[2][1] = C[0]*(C[1]*(C[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) + S[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50)) + S[1]*(C[3]*((C[5]*C[6])/10 + 1483/5000) - S[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + 61/200))
    Jv[2][2] = S[0]*(C[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) + S[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50)) - C[0]*S[1]*(S[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10) - C[2]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000) + 1/50))
    Jv[2][3] = C[0]*(C[1]*(C[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50) + S[3]*((C[5]*C[6])/10 + 1483/5000)) + S[1]*S[2]*(C[3]*((C[5]*C[6])/10 + 1483/5000) - S[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50))) - C[2]*S[0]*(C[3]*((C[5]*C[6])/10 + 1483/5000) - S[3]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10 - 1/50))
    Jv[2][4] = C[0]*(S[1]*(C[2]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10) - C[3]*S[2]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10)) - C[1]*S[3]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10)) + S[0]*(S[2]*((C[4]*S[6])/10 + (C[6]*S[4]*S[5])/10) + C[2]*C[3]*((S[4]*S[6])/10 - (C[4]*C[6]*S[5])/10))
    Jv[2][5] = C[0]*(C[1]*((C[3]*C[6]*S[5])/10 + (C[5]*C[6]*S[3]*S[4])/10) - S[1]*(S[2]*((C[6]*S[3]*S[5])/10 - (C[3]*C[5]*C[6]*S[4])/10) + (C[2]*C[4]*C[5]*C[6])/10)) + S[0]*(C[2]*((C[6]*S[3]*S[5])/10 - (C[3]*C[5]*C[6]*S[4])/10) - (C[4]*C[5]*C[6]*S[2])/10)
    Jv[2][6] = C[0]*(C[1]*(S[3]*((C[4]*C[6])/10 - (S[4]*S[5]*S[6])/10) + (C[3]*C[5]*S[6])/10) + S[1]*(S[2]*(C[3]*((C[4]*C[6])/10 - (S[4]*S[5]*S[6])/10) - (C[5]*S[3]*S[6])/10) + C[2]*((C[6]*S[4])/10 + (C[4]*S[5]*S[6])/10))) - S[0]*(C[2]*(C[3]*((C[4]*C[6])/10 - (S[4]*S[5]*S[6])/10) - (C[5]*S[3]*S[6])/10) - S[2]*((C[6]*S[4])/10 + (C[4]*S[5]*S[6])/10))

    return np.array(Jv)

def compute_jacobian_omega(q_list, rows, cols):
    S = np.sin(q_list)
    C = np.cos(q_list)
    # qr1, qr2, qr3, qr4, qr5, qr6, qr7 = q_list

    Jw = [[0 for j in range(cols)] for i in range(rows)]

    Jw[0][0] = 0
    Jw[0][1] = C[0]
    Jw[0][2] = C[1]*S[0]
    Jw[0][3] = C[0]*S[2] - C[2]*S[0]*S[1]
    Jw[0][4] = C[1]*C[3]*S[0] - S[3]*(C[0]*C[2] + S[0]*S[1]*S[2])
    Jw[0][5] = S[4]*(C[0]*S[2] - C[2]*S[0]*S[1]) - C[4]*(C[3]*(C[0]*C[2] + S[0]*S[1]*S[2]) + C[1]*S[0]*S[3])
    Jw[0][6] = C[6]*(C[4]*(C[3]*(C[0]*C[2] + S[0]*S[1]*S[2]) + C[1]*S[0]*S[3]) - S[4]*(C[0]*S[2] - C[2]*S[0]*S[1])) - S[6]*(C[5]*(S[3]*(C[0]*C[2] + S[0]*S[1]*S[2]) - C[1]*C[3]*S[0]) + S[5]*(S[4]*(C[3]*(C[0]*C[2] + S[0]*S[1]*S[2]) + C[1]*S[0]*S[3]) + C[4]*(C[0]*S[2] - C[2]*S[0]*S[1])))
    Jw[1][0] = 1
    Jw[1][1] = 0
    Jw[1][2] = -S[1]
    Jw[1][3] = -C[1]*C[2]
    Jw[1][4] = - C[3]*S[1] - C[1]*S[2]*S[3]
    Jw[1][5] = C[4]*(S[1]*S[3] - C[1]*C[3]*S[2]) - C[1]*C[2]*S[4]
    Jw[1][6] = S[6]*(S[5]*(S[4]*(S[1]*S[3] - C[1]*C[3]*S[2]) + C[1]*C[2]*C[4]) - C[5]*(C[3]*S[1] + C[1]*S[2]*S[3])) - C[6]*(C[4]*(S[1]*S[3] - C[1]*C[3]*S[2]) - C[1]*C[2]*S[4])
    Jw[2][0] = 0
    Jw[2][1] = -S[0]
    Jw[2][2] = C[0]*C[1]
    Jw[2][3] = - S[0]*S[2] - C[0]*C[2]*S[1]
    Jw[2][4] = S[3]*(C[2]*S[0] - C[0]*S[1]*S[2]) + C[0]*C[1]*C[3]
    Jw[2][5] = C[4]*(C[3]*(C[2]*S[0] - C[0]*S[1]*S[2]) - C[0]*C[1]*S[3]) - S[4]*(S[0]*S[2] + C[0]*C[2]*S[1])
    Jw[2][6] = S[6]*(C[5]*(S[3]*(C[2]*S[0] - C[0]*S[1]*S[2]) + C[0]*C[1]*C[3]) + S[5]*(S[4]*(C[3]*(C[2]*S[0] - C[0]*S[1]*S[2]) - C[0]*C[1]*S[3]) + C[4]*(S[0]*S[2] + C[0]*C[2]*S[1]))) - C[6]*(C[4]*(C[3]*(C[2]*S[0] - C[0]*S[1]*S[2]) - C[0]*C[1]*S[3]) - S[4]*(S[0]*S[2] + C[0]*C[2]*S[1]))

    return np.array(Jw)

