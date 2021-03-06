# This file is part of QuTiP.
#
#    QuTiP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    QuTiP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with QuTiP.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2011 and later, Paul D. Nation & Robert J. Johansson
#
###########################################################################

import numpy as np
import scipy
import scipy.sparse as sp

from qutip.qobj import Qobj


#
# Spin operators
#
def jmat(j, *args):
    """Higher-order spin operators:

    Parameters
    ----------
    j : float
        Spin of operator

    args : str
        Which operator to return 'x','y','z','+','-'.
        If no args given, then output is ['x','y','z']

    Returns
    -------
    jmat : qobj/list
        ``qobj`` for requested spin operator(s).


    Examples
    --------
    >>> jmat(1)
    [ Quantum object: dims = [[3], [3]], \
shape = [3, 3], type = oper, isHerm = True
    Qobj data =
    [[ 0.          0.70710678  0.        ]
     [ 0.70710678  0.          0.70710678]
     [ 0.          0.70710678  0.        ]]
     Quantum object: dims = [[3], [3]], \
shape = [3, 3], type = oper, isHerm = True
    Qobj data =
    [[ 0.+0.j          0.+0.70710678j  0.+0.j        ]
     [ 0.-0.70710678j  0.+0.j          0.+0.70710678j]
     [ 0.+0.j          0.-0.70710678j  0.+0.j        ]]
     Quantum object: dims = [[3], [3]], \
shape = [3, 3], type = oper, isHerm = True
    Qobj data =
    [[ 1.  0.  0.]
     [ 0.  0.  0.]
     [ 0.  0. -1.]]]


    Notes
    -----
    If no 'args' input, then returns array of ['x','y','z'] operators.

    """
    if (scipy.fix(2 * j) != 2 * j) or (j < 0):
        raise TypeError('j must be a non-negative integer or half-integer')
    if not args:
        a1 = Qobj(0.5 * (jplus(j) + jplus(j).conj().T))
        a2 = Qobj(0.5 * 1j * (jplus(j) - jplus(j).conj().T))
        a3 = Qobj(jz(j))
        return np.array([a1, a2, a3])
    if args[0] == '+':
        A = jplus(j)
    elif args[0] == '-':
        A = jplus(j).conj().T
    elif args[0] == 'x':
        A = 0.5 * (jplus(j) + jplus(j).conj().T)
    elif args[0] == 'y':
        A = -0.5 * 1j * (jplus(j) - jplus(j).conj().T)
    elif args[0] == 'z':
        A = jz(j)
    else:
        raise TypeError('Invlaid type')
    return Qobj(A.tocsr())


def jplus(j):
    m = np.arange(j, -j - 1, -1)
    N = len(m)
    return sp.spdiags(np.sqrt(j * (j + 1.0) - (m + 1.0) * m),
                      1, N, N, format='csr')


def jz(j):
    m = np.arange(j, -j - 1, -1)
    N = len(m)
    return sp.spdiags(m, 0, N, N, format='csr')

#
# Pauli spin 1/2 operators:
#


def sigmap():
    """Creation operator for Pauli spins.

    Examples
    --------
    >>> sigmam()
    Quantum object: dims = [[2], [2]], \
shape = [2, 2], type = oper, isHerm = False
    Qobj data =
    [[ 0.  1.]
     [ 0.  0.]]

    """
    return jmat(1 / 2., '+')


def sigmam():
    """Annihilation operator for Pauli spins.

    Examples
    --------
    >>> sigmam()
    Quantum object: dims = [[2], [2]], \
shape = [2, 2], type = oper, isHerm = False
    Qobj data =
    [[ 0.  0.]
     [ 1.  0.]]

    """
    return jmat(1 / 2., '-')


def sigmax():
    """Pauli spin 1/2 sigma-x operator

    Examples
    --------
    >>> sigmax()
    Quantum object: dims = [[2], [2]], \
shape = [2, 2], type = oper, isHerm = False
    Qobj data =
    [[ 0.  1.]
     [ 1.  0.]]

    """
    return 2.0 * jmat(1.0 / 2, 'x')


def sigmay():
    """Pauli spin 1/2 sigma-y operator.

    Examples
    --------
    >>> sigmay()
    Quantum object: dims = [[2], [2]], \
shape = [2, 2], type = oper, isHerm = True
    Qobj data =
    [[ 0.+0.j  0.-1.j]
     [ 0.+1.j  0.+0.j]]

    """
    return 2.0 * jmat(1.0 / 2, 'y')


def sigmaz():
    """Pauli spin 1/2 sigma-z operator.

    Examples
    --------
    >>> sigmaz()
    Quantum object: dims = [[2], [2]], \
shape = [2, 2], type = oper, isHerm = True
    Qobj data =
    [[ 1.  0.]
     [ 0. -1.]]

    """
    return 2.0 * jmat(1.0 / 2, 'z')


#
# DESTROY returns annihilation operator for N dimensional Hilbert space
# out = destroy(N), N is integer value &  N>0
#
def destroy(N):
    '''Destruction (lowering) operator.

    Parameters
    ----------
    N : int
        Dimension of Hilbert space.

    Returns
    -------
    oper : qobj
        Qobj for lowering operator.

    Examples
    --------
    >>> destroy(4)
    Quantum object: dims = [[4], [4]], \
shape = [4, 4], type = oper, isHerm = False
    Qobj data =
    [[ 0.00000000+0.j  1.00000000+0.j  0.00000000+0.j  0.00000000+0.j]
     [ 0.00000000+0.j  0.00000000+0.j  1.41421356+0.j  0.00000000+0.j]
     [ 0.00000000+0.j  0.00000000+0.j  0.00000000+0.j  1.73205081+0.j]
     [ 0.00000000+0.j  0.00000000+0.j  0.00000000+0.j  0.00000000+0.j]]

    '''
    if not isinstance(N, (int,np.integer)):  # raise error if N not integer
        raise ValueError("Hilbert space dimension must be integer value")
    return Qobj(sp.spdiags(np.sqrt(range(0, N)), 1, N, N, format='csr'))

#
# CREATE returns creation operator for N dimensional Hilbert space
# out = create(N), N is integer value &  N>0
#


def create(N):
    '''Creation (raising) operator.

    Parameters
    ----------
    N : int
        Dimension of Hilbert space.

    Returns
    -------
    oper : qobj
        Qobj for raising operator.

    Examples
    --------
    >>> create(4)
    Quantum object: dims = [[4], [4]], \
shape = [4, 4], type = oper, isHerm = False
    Qobj data =
    [[ 0.00000000+0.j  0.00000000+0.j  0.00000000+0.j  0.00000000+0.j]
     [ 1.00000000+0.j  0.00000000+0.j  0.00000000+0.j  0.00000000+0.j]
     [ 0.00000000+0.j  1.41421356+0.j  0.00000000+0.j  0.00000000+0.j]
     [ 0.00000000+0.j  0.00000000+0.j  1.73205081+0.j  0.00000000+0.j]]

    '''
    if not isinstance(N, (int,np.integer)):  # raise error if N not integer
        raise ValueError("Hilbert space dimension must be integer value")
    qo = destroy(N)  # create operator using destroy function
    qo.data = qo.data.T  # transpsoe data in Qobj
    return Qobj(qo)


#
# QEYE returns identity operator for an N dimensional space
# a = qeye(N), N is integer & N>0
#
def qeye(N):
    """Identity operator

    Parameters
    ----------
    N : int
        Dimension of Hilbert space.

    Returns
    -------
    oper : qobj
        Identity operator Qobj.

    Examples
    --------
    >>> qeye(3)
    Quantum object: dims = [[3], [3]], \
shape = [3, 3], type = oper, isHerm = True
    Qobj data =
    [[ 1.  0.  0.]
     [ 0.  1.  0.]
     [ 0.  0.  1.]]

    """
    N = int(N)
    if (not isinstance(N, (int,np.integer))) or N < 0:  # check if N is int and N>0
        raise ValueError("N must be integer N>=0")
    return Qobj(sp.eye(N, N, dtype=complex, format='csr'))


def identity(N):
    """Identity operator. Alternative name to :func:`qeye`.

    Parameters
    ----------
    N : int
        Dimension of Hilbert space.

    Returns
    -------
    oper : qobj
        Identity operator Qobj.
    """
    return qeye(N)


def position(N):
    """
    Position operator x=1\sqrt(2)*(a+a.dag())

    Parameters
    ----------
    N : int
        Number of Fock states in Hilbert space.

    """
    a = destroy(N)
    return 1.0 / np.sqrt(2.0) * (a + a.dag())


def momentum(N):
    """
    Momentum operator p=1\sqrt(2)*(a-1.0j*a.dag())

    Parameters
    ----------
    N : int
        Number of Fock states in Hilbert space.

    """
    a = destroy(N)
    return 1.0 / np.sqrt(2.0) * (a - 1.0j * a.dag())


def num(N):
    """Quantum object for number operator.

    Parameters
    ----------
    N : int
        The dimension of the Hilbert space.

    Returns
    -------
    oper: qobj
        Qobj for number operator.

    Examples
    --------
    >>> num(4)
    Quantum object: dims = [[4], [4]], \
shape = [4, 4], type = oper, isHerm = True
    Qobj data =
    [[0 0 0 0]
     [0 1 0 0]
     [0 0 2 0]
     [0 0 0 3]]

    """
    data = sp.spdiags(np.arange(N), 0, N, N, format='csr')
    return Qobj(data)


def squeez(N, sp):
    """Single-mode Squeezing operator.


    Parameters
    ----------
    N : int
        Dimension of hilbert space.

    sp : float/complex
        Squeezing parameter.

    Returns
    -------
    oper : :class:`qutip.qobj.Qobj`
        Squeezing operator.


    Examples
    --------
    >>> squeez(4,0.25)
    Quantum object: dims = [[4], [4]], \
shape = [4, 4], type = oper, isHerm = False
    Qobj data =
    [[ 0.98441565+0.j  0.00000000+0.j  0.17585742+0.j  0.00000000+0.j]
     [ 0.00000000+0.j  0.95349007+0.j  0.00000000+0.j  0.30142443+0.j]
     [-0.17585742+0.j  0.00000000+0.j  0.98441565+0.j  0.00000000+0.j]
     [ 0.00000000+0.j -0.30142443+0.j  0.00000000+0.j  0.95349007+0.j]]


    .. important::

        There is no ending 'e' for the squeezing operator!

    """
    a = destroy(N)
    op = (1 / 2.0) * np.conj(sp) * (a ** 2) - (1 / 2.0) * sp * (a.dag()) ** 2
    return op.expm()


def squeezing(a1, a2, z):
    """Generalized squeezing operator.

    .. math::

        S(z) = \\exp\\left(\\frac{1}{2}\\left(z^*a_1a_2
        - za_1^\dagger a_2^\dagger\\right)\\right)

    Parameters
    ----------
    a1 : :class:`qutip.qobj.Qobj`
        Operator 1.

    a2 : :class:`qutip.qobj.Qobj`
        Operator 2.

    z : float/complex
        Squeezing parameter.

    Returns
    -------
    oper : :class:`qutip.qobj.Qobj`
        Squeezing operator.

    """
    b = 0.5 * (np.conj(z) * (a1 * a2) - z * (a1.dag() * a2.dag()))
    return b.expm()


def displace(N, alpha):
    """Single-mode displacement operator.

    Parameters
    ----------
    N : int
        Dimension of Hilbert space.

    alpha : float/complex
        Displacement amplitude.

    Returns
    -------
    oper : qobj
        Displacement operator.

    Examples
    ---------
    >>> displace(4,0.25)
    Quantum object: dims = [[4], [4]], \
shape = [4, 4], type = oper, isHerm = False
    Qobj data =
    [[ 0.96923323+0.j -0.24230859+0.j  0.04282883+0.j -0.00626025+0.j]
     [ 0.24230859+0.j  0.90866411+0.j -0.33183303+0.j  0.07418172+0.j]
     [ 0.04282883+0.j  0.33183303+0.j  0.84809499+0.j -0.41083747+0.j]
     [ 0.00626025+0.j  0.07418172+0.j  0.41083747+0.j  0.90866411+0.j]]

    """
    a = destroy(N)
    D = (alpha * a.dag() - np.conj(alpha) * a).expm()
    return D


def commutator(A, B, kind="normal"):
    """
    Return the commutator of kind `kind` (normal, anti) of the
    two operators A and B.
    """
    if kind == 'normal':
        return A * B - B * A

    elif kind == 'anti':
        return A * B + B * A

    else:
        raise TypeError("Unknown commutator kind '%s'" % kind)


#
# Three-level operators (qutrits)
#
def qutrit_ops():
    """
    Operators for a three level system (qutrit).

    Returns
    -------
    opers: array
        `array` of qutrit operators.

    """
    from qutip.states import qutrit_basis

    one, two, three = qutrit_basis()
    sig11 = one * one.dag()
    sig22 = two * two.dag()
    sig33 = three * three.dag()
    sig12 = one * two.dag()
    sig23 = two * three.dag()
    sig31 = three * one.dag()
    return np.array([sig11, sig22, sig33, sig12, sig23, sig31])

#
# Generate operator from diagonals
#


def qdiags(diagonals, offsets, dims=None, shape=None):
    """
    Constructs an operator from an array of diagonals.

    Parameters
    ----------
    diagonals : sequence of array_like
        Array of elements to place along the selected diagonals.
    offsets : sequence of ints
        Sequence for diagonals to be set:
            - k=0 main diagonal
            - k>0 kth upper diagonal
            - k<0 kth lower diagonal
    dims : list, optional
        Dimensions for operator
    shape : list, tuple, optional
        Shape of operator.  If omitted, a square operator large enough
        to contain the diagonals is generated.

    See Also
    --------
    scipy.sparse.diags for useage information.

    Notes
    -----
    This function requires SciPy 0.11+.

    Examples
    --------
    >>> qdiag(sqrt(range(1,4)),1)
    Quantum object: dims = [[4], [4]], \
shape = [4, 4], type = oper, isherm = False
    Qobj data =
    [[ 0.          1.          0.          0.        ]
     [ 0.          0.          1.41421356  0.        ]
     [ 0.          0.          0.          1.73205081]
     [ 0.          0.          0.          0.        ]]

    """
    try:
        data = sp.diags(diagonals, offsets, shape, format='csr', dtype=complex)
    except:
        raise NotImplemented("This function required SciPy 0.11+.")
    if not dims:
        dims = [[], []]
    if not shape:
        shape = []
    return Qobj(data, dims, list(shape))


def phase(N, phi0=0):
    """
    Single-mode Pegg-Barnett phase operator.

    Parameters
    ----------
    N : int
        Number of basis states in Hilbert space.
    phi0 : float
        Reference phase.

    Returns
    -------
    oper : qobj
        Phase operator with respect to reference phase.

    Notes
    -----
    The Pegg-Barnett phase operator is Hermitian on a truncated Hilbert space.

    """
    phim = phi0 + (2.0 * np.pi * np.arange(N)) / N  # discrete phase angles
    n = np.arange(N).reshape((N, 1))
    states = np.array([np.sqrt(kk) / np.sqrt(N) * np.exp(1.0j * n * kk)
                       for kk in phim])
    ops = np.array([np.outer(st, st.conj()) for st in states])
    return Qobj(np.sum(ops, axis=0))
