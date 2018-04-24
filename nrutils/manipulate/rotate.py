
#
from nrutils.core.basics import *


# Calculate Widger D-Matrix Element
def wdelement( ll,         # polar index (eigenvalue) of multipole to be rotated (set of m's for single ll )
               mp,         # member of {all em for |em|<=l} -- potential projection spaceof m
               mm,         # member of {all em for |em|<=l} -- the starting space of m
               alpha,      # -.
               beta,       #  |- Euler angles for rotation
               gamma ):    # -'

    #** James Healy 6/18/2012
    #** wignerDelement
    #*  calculates an element of the wignerD matrix
    # Modified by llondon6 in 2012 and 2014
    # Converted to python by spxll 2016
    #
    # This implementation apparently uses the formula given in:
    # https://en.wikipedia.org/wiki/Wigner_D-matrix
    #
    # Specifically, this the formula located here: https://wikimedia.org/api/rest_v1/media/math/render/svg/53fd7befce1972763f7f53f5bcf4dd158c324b55

    #
    from numpy import sqrt,exp,cos,sin
    from scipy.misc import factorial

    #
    alpha,beta,gamma = float(alpha),float(beta),float(gamma)

    #
    coefficient = sqrt( factorial(ll+mp)*factorial(ll-mp)*factorial(ll+mm)*factorial(ll-mm))*exp( 1j*(mp*alpha+mm*gamma) )

    # NOTE that there may be convention differences where the overall sign of the complex exponential may be negated

    #
    total = 0

    # find smin
    if (mm-mp) >= 0 :
        smin = mm - mp
    else:
        smin = 0

    # find smax
    if (ll+mm) > (ll-mp) :
        smax = ll-mp
    else:
        smax = ll+mm

    #
    if smin <= smax:
        for ss in range(smin,smax+1):
            A = (-1)**(mp-mm+ss)
            A *= cos(beta/2)**(2*ll+mm-mp-2*ss)  *  sin(beta/2)**(mp-mm+2*ss)
            B = factorial(ll+mm-ss) * factorial(ss) * factorial(mp-mm+ss) * factorial(ll-mp-ss)
            total += A/B

    #
    element = coefficient*total
    return element

# Calculate Widner D Matrix
def wdmatrix( l,                # polar l
              mrange,    # range of m values
              alpha,
              beta,
              gamma,
              verbose = None ): # let the people know

    #
    from numpy import arange,array,zeros,complex256

    # Handle the mrange input
    if mrange is None:
        #
        mrange = arange( -l, l+1 )
    else:
        # basic validation
        for m in mrange:
            if abs(m)>l:
                msg = 'values in m range must not be greater than l'
                error(msg,'wdmatrix')

    #
    dim = len(mrange)
    D = zeros( (dim,dim), dtype=complex256 )
    for j,mm in enumerate(mrange):
        for k,mp in enumerate(mrange):
            D[j,k] = wdelement( l, mp, mm, alpha, beta, gamma )

    #
    return D
