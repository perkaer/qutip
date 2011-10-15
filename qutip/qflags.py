#This file is part of QuTIP.
#
#    QuTIP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#    QuTIP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with QuTIP.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2011, Paul D. Nation & Robert J. Johansson
#
###########################################################################
import os
def qflags(flag=None,value=None):
    """
    @brief Allows user to view and change the QuTiP flags for graphics
           and multiprocessing.
    """
    
    if flag==None and value==None:
        print 'NUM_THREADS: '+os.environ['NUM_THREADS']+' (Number of threads for multiprocessing.)'
        print 'QUTIP_GRAPHICS: '+os.environ['QUTIP_GRAPHICS']+' (Use QuTiP GUI?)'
        if os.environ['QUTIP_GRAPHICS']=='YES':
            print 'QUTIP_GUI: '+os.environ['QUTIP_GUI']+' (Current GUI backend.)'
